import geocoder
from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.contrib.fixers import ProxyFix
from pyzipcode import ZipCodeDatabase
from geopy.distance import vincenty
from urllib2 import urlopen
import settings

app = Flask(__name__)
api = Api(app)

# this will make sure request.remote_addr has IP address
app.wsgi_app = ProxyFix(app.wsgi_app)


class ZipcodeDistance(Resource):
    def post(self):

        # force to accept only JSON posted data
        try:
            data = request.get_json(force=True)
        except Exception as err:
            print(err)
            return {'error': settings.INVALID_JSON}, 400

        # make sure user has submitted JSON data i.e list of zip codes. Format: {"zip_codes": ["44000", "10008"]}
        if data and data.get('zip_codes') and isinstance(data.get('zip_codes'), list):

            try:
                g = geocoder.ip(request.remote_addr)
            except Exception as err:
                return {'error': settings.CONNECTION_ERROR}, 400

            # if user is from local machine instead of a real IP (server machine) then get user's real IP address
            if g.ip == '127.0.0.1':
                user_ip = urlopen('http://ip.42.pl/raw').read()

                # get user's Geo Data from user's IP address
                g = geocoder.ip(user_ip)
                user_lat_lng = g.lat, g.lng

            result = dict()

            # iterate through each zip code and calculate distance relative to user's lat, long
            for zip_code in data.get('zip_codes', []):

                # This package contains geo data for US zip codes only.
                zcdb = ZipCodeDatabase()
                try:

                    # get zip code's Geo Data for lat, long
                    zip_code_data = zcdb[zip_code]
                    zip_code_lat_lng = zip_code_data.latitude, zip_code_data.longitude

                    """
                    Calculate the geodesic distance between two points using the formula devised by Thaddeus Vincenty,
                    with an accurate ellipsoidal model of the earth. using geopy package
                    """
                    distance = round(vincenty(zip_code_lat_lng, user_lat_lng).miles, 2)
                    result[zip_code] = '{0} Miles'.format(distance)

                except IndexError as err:
                    result[zip_code] = settings.INVALID_ZIP_CODE

            return result, 200
        else:
            return {'error': settings.INVALID_JSON}, 400

api.add_resource(ZipcodeDistance, settings.ZIP_CODE_DISTANCE_ENDPOINT)

if __name__ == '__main__':
    app.run(debug=True)
