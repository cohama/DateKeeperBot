import re
from datetime import datetime, timedelta
from google.appengine.ext import webapp
from google.appengine.ext import db
import tweepy
from twapi import TwitterApi
from index import doRender

class Schedule(db.Model):
	id = db.IntegerProperty()
	user = db.StringProperty()
	day = db.IntegerProperty()
	month = db.IntegerProperty()
	todo = db.StringProperty()


class DateKeeperBotHandler(webapp.RequestHandler):

	def __init__(self):
		self.api = TwitterApi.api

	def get(self):
		self._get_schedule_from_tweet()
		
	def _get_schedule_from_tweet(self):
		tweet_list = self.api.user_timeline(screen_name='c0hama')
		
		for tweet in tweet_list:
			if self._is_new_tweet(tweet):
				sch = self._create_schedule(tweet)
				if sch != None:
					sch.put()
	
	def _create_schedule(self, tweet):
		mo = re.match(ur'(\d+)月(\d+)日は(.*)', tweet.text)
		
		if mo:
			month = int(mo.group(1))
			day = int(mo.group(2))
			text = mo.group(3)
			
			return Schedule(id=tweet.id, user=tweet.user.screen_name, day=day, month=month, todo=text)
			
		else:
			return None
	
	def _is_new_tweet(self, schedule):
		query = Schedule.all()
		query.filter('id =', schedule.id)
		return query.count() == 0

