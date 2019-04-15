# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging
import gspread
import pandas
import location
from oauth2client.service_account import ServiceAccountCredentials
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
Bootstrap(app)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('config/appspot.json', scope)

gc = gspread.authorize(credentials)

# worksheet = gc.open("p3database").sheet1
# dataframe = pandas.DataFrame(worksheet.get_all_records())

#Init the extension
GoogleMaps(app, key="AIzaSyAqfM5olFncI21ahLPniscGdZVXPt4kpc8")


@app.route('/')
def main():
    worksheet = gc.open("p3database").sheet1
    dataFrame = pandas.DataFrame(worksheet.get_all_records())

    latList = pandas.Series(dataFrame["latitude"]).tolist()
    lngtList = pandas.Series(dataFrame["longitude"]).tolist()
    nameList = pandas.Series(dataFrame["name"]).tolist()
    idList = pandas.Series(dataFrame["id"]).tolist()
    
    locationDic = []
    for i in range(len(latList)):
        locationDic.append(location.location(latList[i],lngtList[i],nameList[i],idList[i]).hotspot)

    locations = Map(
        identifier="locations",
        lat=32.7157,
        lng=-117.1611,
        zoom=13,
        style="height:100%;width:100%;margin:0;",
        markers= locationDic
    )
    return render_template('index.html', places = locationDic, locations = locations)

@app.route('/locations/')
def locations():
    # API Call to Dataframe
    # Parse Data frame if need
    # Return data to template

    worksheet = gc.open("p3database").sheet1
    dataFrame = pandas.DataFrame(worksheet.get_all_records())

    latList = pandas.Series(dataFrame["latitude"]).tolist()
    lngtList = pandas.Series(dataFrame["longitude"]).tolist()
    nameList = pandas.Series(dataFrame["name"]).tolist()
    idList = pandas.Series(dataFrame["id"]).tolist()

    locationDic = []
    for i in range(len(latList)):
        locationDic.append(location.location(latList[i],lngtList[i],nameList[i],idList[i]).hotspot)

    locations = Map(
        identifier="locations",
        lat=32.7157,
        lng=-117.1611,
        zoom=13,
        style="height:300px;width:600px;margin:0;",
        markers= locationDic
    )

    return render_template('locations.html', locations = locations)

@app.route('/luis')
def luis():
    return {"name": "Hi Luis"}

@app.route('/location/<idNum>/')
def artVote(idNum):
    worksheet = gc.open("p3database").sheet1
    dataFrame = pandas.DataFrame(worksheet.get_all_records())
    nameList = pandas.Series(dataFrame["name"]).tolist()
    idList = pandas.Series(dataFrame["id"]).tolist()
    name = ''
    for i in range(len(idList)):
        if idList[i] == int(idNum):
            name = nameList[i]
    nums = [1, 2, 3]
    artistNames = {"1":"David Choe", "2":"Jacoby Ellsbury", "3":"Luis Galaxy Brain"}

    return render_template("artpage.html", nums=nums, name=name, artist=artistNames)    

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)