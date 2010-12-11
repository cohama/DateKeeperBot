
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
	date = db.DateTimeProperty()
	todo = db.StringProperty()


class DateKeeperBotHandler(webapp.RequestHandler):

	def __init__(self):
		self.api = TwitterApi.api

	def get(self):
		self._get_schedule_from_tweet()
		
	def _get_schedule_from_tweet(self):
		tweet_list = self.api.user_timeline(screen_name='c0hama')
		
		now_year = datetime.now().year

		for tweet in tweet_list:
			tweet.created_at = self._to_Tokyo_timezone(tweet.created_at)
			
			sch = self._create_schedule(tweet)
			if (sch != None):
				if (self._is_new_schedule(sch)):
					sch.put()
					
		
	def _to_Tokyo_timezone(self, date):
		return date + timedelta(hours=9)
		
	def _create_schedule(self, tweet):
		mo = re.match(ur'(\d+)月(\d+)日は(.*)', tweet.text)
		
		if mo:
		
			month = int(mo.group(1))
			day = int(mo.group(2))
			text = mo.group(3)
			posted_date = datetime(year=datetime.now().year, month=month, day=day, hour=8)
			
			return Schedule(id=tweet.id, user=tweet.user.screen_name, date=posted_date, todo=text)
			
		else:
		
			return None
	
	def _is_new_schedule(self, schedule):
		query = Schedule.all()
		query.filter('id =', schedule.id)
		return query.count() == 0

