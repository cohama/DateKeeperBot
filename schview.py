from datetime import datetime, timedelta
from google.appengine.ext import webapp
from google.appengine.ext import db
from index import doRender
from dkbot import Schedule

class ScheduleViewerHandler(webapp.RequestHandler):

	def get(self):
		""" show specified user's schedule
		    (not imprelemented yet)
			(now all user's schedule shown)
		""" 
		query = Schedule.all()
		query.order('date')
		schedule_list = query.fetch(limit=100)
		
		doRender(self, 'schedule_view.html', {'schedule_list':schedule_list})

