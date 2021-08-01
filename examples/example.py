import pycronometer

email = 'YOUR_CRONOMETER_LOGIN_EMAIL'
password = 'YOUR_CRONOMETER_PASSWORD'
from_date = '2021-02-01'
to_date = '2021-02-28'

client = pycronometer.Cronometer()
client.login(email, password)
     
dailyNutrition = client.export_daily_nutirtion(from_date, to_date)
dilayNutririonFile = open('dailyNutrition-' + from_date + '-' +  to_date + '.csv', 'wb')
dilayNutririonFile.write(dailyNutrition)
dilayNutririonFile.close()

servings = client.export_servings(from_date, to_date)
servingsFile = open('servings-' + from_date + '-' + to_date + '.csv', 'wb')
servingsFile.write(servings)
servingsFile.close()
    
exercise = client.export_exercise(from_date, to_date)
exerciseFile = open('exercise-' + from_date + '-' + to_date + '.csv', 'wb')
exerciseFile.write(exercise)
exerciseFile.close()
    
biometrics = client.export_biometrics(from_date, to_date)
biometricsFile = open('biometrics-' + from_date + '-' + to_date + '.csv', 'wb')
biometricsFile.write(biometrics)
biometricsFile.close()

notes = client.export_notes(from_date,to_date)
notesFile = open('notes-' + from_date + '-' + to_date + '.csv', 'wb')
notesFile.write(notes)
notesFile.close()

client.logout()