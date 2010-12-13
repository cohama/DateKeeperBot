from datetime import datetime, timedelta
from google.appengine.ext import webapp
from google.appengine.ext import db
import tweepy
from twapi import TwitterApi
from dkbot import Schedule
from index import doRender

class DatePostHandler(webapp.RequestHandler):

	def get(self):
		self._post_scheduled_tweet()
		
	def _post_scheduled_tweet(self):
		today = self._to_Tokyo_timezone( datetime.now() )
		
		query = Schedule.all()
		query.filter( 'month =', today.month )
		query.filter( 'day =', today.day )
		
		test_list = []
		
		for sch in query:
			tweet = u'@' + sch.user + u' 今日は' + sch.todo
			test_list.append(tweet)
			TwitterApi.api.update_status(tweet)
			sch.delete()
			
		doRender(handler=self, values={'test_list':test_list})
		
	def _to_Tokyo_timezone(self, date):
		return date + timedelta(hours=9)