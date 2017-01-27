#### Find Distance between user's location and a Zip Code
Getting distance between zip code and user's location based on IP address. User need to provide list of zip codes as JSON object. Script will go through each zip code, get latitude/longitude for each zip code, calculate distance between user lat/lng and zip code lat/lng.<br/>
Response will be a JSON object where the key is the zip code and the value is the distance in miles between that zip code and the user.

<br/>
#####Tested Environment
```
Ubuntu 14.04
Python 2.7
Flask 0.12
Flask RESTful 0.3.5
geocoder 1.20.0
geopy 1.11.0
pyzipcode 1.0
```

<br/>
#####Install dependencies
Create a virtualenv, switch to project root directory and execute command

```
pip install -r requirements.txt
```

<br/>
#####Update settings and messages
settings.py

```
ZIP_CODE_DISTANCE_ENDPOINT = '/api/zip_code_distance/'

INVALID_JSON = 'Please provide a JSON object including a list of zip codes...'
INVALID_ZIP_CODE = 'Invalid zip code. Make sure zip code exist in US'
CONNECTION_ERROR = 'Something went wrong. Make sure you have internet connection'
```

<br/>
#####Run project
Switch to `flask_assessment/flask_assessment` directory and execute command
```
python api.py
```

<br/>
#####Test API
execute command from terminal
```
curl http://localhost:5000/api/zip_code_distance/ -d '{"zip_codes": ["10008", "10009", "21061"]}' -H "Content-Type: application/json"  -X POST
```

<br/>
#####Validation and Errors
 * POST data must be JSON and not form-data or x-www-form-urlencoded
 * A Valid JSON object having list of zip codes must be provided. e.g {"zip_codes": ["21061", "10008"]}
 * If a zip code is invalid, a message will return in response for that zip code instead of distance

<br/>
#####fatal error: sqlite3.h: No such file or directory
If you are getting this error on Ubuntu or any other *nix, execute below command
```
sudo apt-get install libsqlite3-dev
```
