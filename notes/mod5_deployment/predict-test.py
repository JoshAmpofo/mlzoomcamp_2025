

import requests

host = "churn-serving-env.eba-ftfwmmwp.eu-west-1.elasticbeanstalk.com"
url = f'http://{host}/predict'

customer = {
    'gender': 'female',
    'seniorcitizen': 0,
    'partner': 'yes',
    'dependents': 'yes',
    'phoneservice': 'yes',
    'multiplelines': 'yes',
    'internetservice': 'fiber_optic',
    'onlinesecurity': 'yes',
    'onlinebackup': 'no',
    'deviceprotection': 'yes',
    'techsupport': 'no',
    'streamingtv': 'yes',
    'streamingmovies': 'yes',
    'contract': 'month-to-month',
    'paperlessbilling': 'yes',
    'paymentmethod': 'electronic_check',
    'tenure': 1,
    'monthlycharges': 104.2,
    'totalcharges': (1 * 104.2)
}

response = requests.post(url, json=customer).json()
print(response)

if response['churn'] == True:
    print('Sending promotional email to customer')
else:
    print('No promotional email needed')

# to use a production server (WSGI)
# gunicorn --bind 0.0.0.0:8000 app_name:aspons
