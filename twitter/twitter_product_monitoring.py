import settings
from multiprocessing import Process
from TwitterAPI import TwitterAPI

api = TwitterAPI(
    settings.TWITTER_CONSUMER_KEY,
    settings.TWITTER_CONSUMER_SECRET,
    settings.TWITTER_ACCESS_TOKEN_KEY,
    settings.TWITTER_ACCESS_TOKEN_SECRET)


def _smart_truncate(content, length=100, suffix=''):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def _save_tweet(brand, tweet):

    tweet = brand + ': ' + tweet['text'] if 'text' in tweet else tweet

    with open("../temp/tweets.txt", "a") as tweets:
        tweets.write(tweet)
        tweets.close()
    print(tweet)


def load_tweets_by_product(product_name, max_count=2000):

    r = api.request('statuses/filter', {'track': product_name, 'language': settings.LANGUAGE})

    count = 1

    for item in r:
        _save_tweet(product_name, item)

        if max_count <= count:
            break
        count += 1


if __name__ == '__main__':

    products = {'Samsung', 'Apple', 'Motorola', 'Asus'}

    for item in products:
        p = Process(target=load_tweets_by_product, args=(_smart_truncate(item, 60), ))
        p.start()
