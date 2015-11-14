# -*- coding: utf-8 -*-
from TwitterAPI import TwitterAPI
from TwitterAPI.TwitterError import TwitterRequestError, TwitterConnectionError
from api.brand import Brand
from api.mention import Mention
from core.feeling_calculate import FeelingCalculate
import settings


class BrandTracking:

    api = TwitterAPI(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        settings.TWITTER_ACCESS_TOKEN_KEY,
        settings.TWITTER_ACCESS_TOKEN_SECRET)

    brands = {}
    brands_name = []
    feeling_calculate = FeelingCalculate()
    tracking = ''

    def __init__(self):
        self.load_brands()
        self._load_tweets()

    def load_brands(self):
        self.brands = Brand().get_all()

        for brand in self.brands:
            self.brands_name.append(brand['name'])

        self.tracking = ','.join(self.brands_name)

    def get_brand_id(self, mention_text):
        for brand in self.brands:
            if brand['name'].encode('utf-8').lower() in mention_text.lower():
                return brand['id']

    def _load_tweets(self):
        while True:
            try:

                iterator = self.api.request('statuses/filter', {'track': self.tracking, 'language': 'pt'})

                for item in iterator:

                    if 'text' in item:

                        mention_text = item['text'] if 'text' in item else item

                        mention_text = mention_text.encode('utf-8').lower()
                        mention_text = mention_text.replace('\n', ' ')

                        feeling_value = self.feeling_calculate.calculate(mention_text)

                        print 'Brand: ' + str(self.get_brand_id(mention_text)) + '\t' + str(feeling_value) + '\t' + mention_text

                        Mention().save(self.get_brand_id(mention_text), mention_text, feeling_value)

                    elif 'disconnect' in item:
                        event = item['disconnect']

                        if event['code'] in [2, 5, 6, 7]:
                            raise Exception(event['reason'])

            except TwitterRequestError as e:
                if e.status_code < 500:
                    print(e)
                    raise
                else:
                    print(e)
                    pass
            except TwitterConnectionError as e:
                print(e)
                pass

BrandTracking()
