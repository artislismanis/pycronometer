import json;
import sys;
import datetime;
from lxml import html;
import requests;

class Cronometer:
    
    CRONOMETER_URL = "https://cronometer.com"
    API_LOGIN_URL = CRONOMETER_URL + "/login"
    LOGIN_PAGE_URL = API_LOGIN_URL + "/"
    GWT_MODULE_BASE = CRONOMETER_URL + "/cronometer/"
    GWT_BASE_URL = GWT_MODULE_BASE + "app"
    GWT_CONTENT_TYPE = "text/x-gwt-rpc; charset=UTF-8"
    GWT_PERMUTATION = "83E204985B83358456BA51A6F8FC5B5E"
    GWT_HEADER = "0DC85D54E7772402C7AA34F8F9193902"
    API_EXPORT_URL = CRONOMETER_URL + "/export"

    def __init__(self):
      self.nonce = None
      self.userId = None
      self.session = requests.Session()
      self.request_headers = {}
      self.request_headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
      self.gwt_request_headers = self.request_headers.copy()
      self.gwt_request_headers['content-type'] = self.GWT_CONTENT_TYPE
      self.gwt_request_headers['x-gwt-module-base'] = self.GWT_MODULE_BASE
      self.gwt_request_headers['x-gwt-permutation'] = self.GWT_PERMUTATION
    
    def login(self, email, password):
        self._authenticate_app(email, password)
        self._authenticate_api()

    def _get_anticsrf(self):
        response = self.session.get(self.LOGIN_PAGE_URL, headers=self.request_headers)
        antiCSRF = html.fromstring(response.content).xpath('//input[@name="anticsrf"]/@value')
        return antiCSRF

    def _update_nonce(self):
        self.nonce = self.session.cookies['sesnonce']

    def _authenticate_app(self, email, password):
        payload = {}
        payload['anticsrf'] = self._get_anticsrf()
        payload['username'] = email
        payload['password'] = password    
        response = self.session.post(self.API_LOGIN_URL, data=payload, headers=self.request_headers)
        self._update_nonce()

    def _authenticate_api(self):
        payload = '7|0|5|'+ self.GWT_MODULE_BASE +'|' + self.GWT_HEADER + '|com.cronometer.client.CronometerService|authenticate|java.lang.Integer/3438268394|1|2|3|4|1|5|5|60|'
        response = self.session.post(self.GWT_BASE_URL, data=payload, headers=self.gwt_request_headers)
        self.userId = str(json.loads(response.text[4:])[0])
        self._update_nonce()
    
    def _get_gwt_token(self):
        payload = '7|0|8|' + self.GWT_MODULE_BASE + '|' + self.GWT_HEADER + '|com.cronometer.client.CronometerService|generateAuthorizationToken|java.lang.String/2004016611|I|com.cronometer.client.data.AuthScope/3337242207|'+ self.nonce +'|1|2|3|4|4|5|6|6|7|8|' + self.userId +'|3600|7|2|'
        response = self.session.post(self.GWT_BASE_URL, data=payload, headers=self.gwt_request_headers)
        gwt_token = json.loads(response.text[4:])[1][0]
        self._update_nonce()
        return gwt_token

    def logout(self):
        payload = '7|0|6|'+ self.GWT_MODULE_BASE +'|' + self.GWT_HEADER + '|com.cronometer.client.CronometerService|logout|java.lang.String/2004016611|'+ self.nonce + '|1|2|3|4|1|5|6|'
        response = self.session.post(self.GWT_BASE_URL, data=payload, headers=self.gwt_request_headers)
        self.session.close()

    def _validate_date(self, date, date_format = '%Y-%m-%d'):
        try:
            datetime.datetime.strptime(date, date_format)
            return date
        except ValueError:
            print("Incorrect date format encountered. Expecting date to be specified as YYYY-MM-DD")
            sys.exit()

    def _export_data(self, export_type, from_date=None, to_date=None):
        params = {}
        params['nonce'] = self._get_gwt_token()
        params['generate'] = export_type
        if from_date is not None and to_date is not None:
            params['start'] = self._validate_date(from_date)
            params['end'] = self._validate_date(to_date)
      
        response = self.session.get(self.API_EXPORT_URL, headers=self.request_headers, params=params)
        return response.content
    
    def export_daily_nutirtion(self, from_date = None, to_date = None):
        dailyNutirtion = self._export_data('dailySummary', from_date, to_date)
        return dailyNutirtion
    
    def export_servings(self, from_date = None, to_date = None):
        servings = self._export_data('servings', from_date, to_date)
        return servings
    
    def export_exercise(self, from_date = None, to_date = None):
        exercise = self._export_data('exercises', from_date, to_date)
        return exercise

    def export_biometrics(self, from_date = None, to_date = None):
        biometrics = self._export_data('biometrics', from_date, to_date)
        return biometrics
    
    def export_notes(self, from_date = None, to_date = None):
        notes = self._export_data('notes', from_date, to_date)
        return notes
