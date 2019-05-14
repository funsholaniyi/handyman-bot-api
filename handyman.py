# -*- coding:utf8 -*-
# !/usr/bin/env python
"""

import requests

url = 'https://cryptic-dusk-24156.herokuapp.com/'
headers = {'content-type': 'application/json',
           'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Y2Q1Njg4NGM4Zjc2YjAwMTczMjQ1ODUiLCJpYXQiOjE1NTc1MjY4MzAsImV4cCI6MTU4OTA2MjgzMH0.OBNyMhr6RBso0YeM1CWYXznW3Tx5P85hal8p0GEJkC8'}


class HandyMan(object):

    def __init__(self, params):
        self.service = params['handyman-service'].casefold()
        self.city = params['geo-city'].casefold()

    def get_list(self):
        # payload = {'occupation': self.service, 'location': self.city}
        # r = requests.post(url + endpoint, data=json.dumps(payload), headers=headers)
        r = requests.get(url + 'handyman/filter?location={0}&occupation={1}'.format(self.city, self.service),
                         headers=headers)
        return r.json()
