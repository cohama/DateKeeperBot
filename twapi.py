import tweepy
from google.appengine.ext import db

class Keys(db.Model):
	appli_name = db.StringProperty()
	consum_key = db.StringProperty()
	consum_sec = db.StringProperty()
	access_key = db.StringProperty()
	access_sec = db.StringProperty()

class TwitterApi:
	api = None
	
	def __init__(self):
		if( TwitterApi.api == None ):
			TwitterApi.api = self._get_twitter_api();
	
	def _get_twitter_api(self):
		query = Keys.all()
		query.filter('appli_name =', 'DateKeeperBot')
		keys = query.fetch(limit=1)[0]
	
		auth = tweepy.OAuthHandler(keys.consum_key, keys.consum_sec)
		auth.set_access_token(keys.access_key, keys.access_sec)
	
		return tweepy.API(auth)
		
api = TwitterApi()