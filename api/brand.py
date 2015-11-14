# -*- coding: utf-8 -*-

import requests
import settings

class Brand:

    def __init__(self, app_host=settings.HOST_CLIENT):
        self.host = app_host

    def get_all(self):

        response = requests.get(self.host + '/brand')

        brands = {}

        if response.status_code == 200:
            brands = response.json()

        return brands
