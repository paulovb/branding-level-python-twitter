# -*- coding: utf-8 -*-

import requests
import settings

class Mention:

    def __init__(self, app_host=settings.HOST_CLIENT):
        self.host = app_host

    def get_all(self):

        response = requests.get(self.host + '/mention')

        brands = {}

        if response.status_code == 200:
            brands = response.json()

        return brands

    def save(self, brand_id, mention, value):

        value_type = 'Neutro'

        if value > 0:
            value_type = 'Positivo'
        elif value < 0:
            value_type = 'Negativo'

        mention = {'brand': brand_id, 'content': mention, 'value': value, 'type': value_type}

        requests.post(self.host + '/mention', data=mention)
