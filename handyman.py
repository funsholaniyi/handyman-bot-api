# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Module that defines the Forecast class and defines helper functions to
process and validate date related to the weather forecast class

This is meant to be used with the sample weather agent for Dialogflow, located at
https://console.dialogflow.com/api-client/#/agent//prebuiltAgents/Weather

This sample uses the WWO Weather Forecast API and requires an WWO API key
Get a WWO API key here: https://developer.worldweatheronline.com/api/
"""
import json

import requests

url = 'https://cryptic-dusk-24156.herokuapp.com/'
headers = {'content-type': 'application/json',
           'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Y2Q1Njg4NGM4Zjc2YjAwMTczMjQ1ODUiLCJpYXQiOjE1NTc1MjY4MzAsImV4cCI6MTU4OTA2MjgzMH0.OBNyMhr6RBso0YeM1CWYXznW3Tx5P85hal8p0GEJkC8'}


class HandyMan(object):

    def __init__(self, params):
        self.service = params['handyman-service'].lower()
        self.city = params['geo-city'].lower()

    def get_list(self):
        # payload = {'occupation': self.service, 'location': self.city}
        # r = requests.post(url + endpoint, data=json.dumps(payload), headers=headers)
        r = requests.get(url+'handyman/filter?location={0}&occupation={1}'.format(self.city, self.service), headers=headers)
        print(r)
        return r.json
