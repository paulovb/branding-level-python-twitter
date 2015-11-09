from TwitterAPI import TwitterAPI
from TwitterAPI.TwitterError import TwitterRequestError, TwitterConnectionError
import settings

TRACK_TERM = str('dilma')
LANGUAGE = 'pt'

#Quando tiver mais de uma marca no mesmo tweet, ele devera ser neutro.

api = TwitterAPI(
    settings.TWITTER_CONSUMER_KEY,
    settings.TWITTER_CONSUMER_SECRET,
    settings.TWITTER_ACCESS_TOKEN_KEY,
    settings.TWITTER_ACCESS_TOKEN_SECRET)

while True:
    try:
        iterator = api.request('statuses/filter', {'track': TRACK_TERM, 'language': LANGUAGE})
        for item in iterator:
            if 'text' in item:
                tweet = item['text'] if 'text' in item else item

                afinn = {}

                for line in open("./../AFINN/AFINN-111-pt.txt"):
                    item = line.split('\t')
                    afinn[item[0]] = int(item[1])

                tweet = tweet.encode('utf-8').lower()

                tweet = tweet.replace('\n', ' ')

                value = sum(map(lambda word: afinn.get(word, 0), tweet.split()))

                with open('../temp/dilma.txt', 'a') as f:
                    f.write(str(value) + '\t' + tweet)
                    f.write('\n')
                    f.close()

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
