import logging
import os
import wsgiref.handlers
from util.sessions import Session
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from twapi import TwitterApi

class MainHandler(webapp.RequestHandler):
	
	def get(self):
		path = self.request.path
		
		if path == '/':
			self.redirect('/index.html', True);
			return;
				
		if not doRender(self, path, {'path':path}):
			self.error(404)


def doRender(handler, templateName='index.html', values={}):
	""" Render a html file with django framework
	"""
	temp = os.path.join(os.path.dirname(__file__), 'templates/' + templateName)
	if not os.path.isfile(temp):
		return False
	
	newval = dict(values)
	if not 'path' in values:
		newval['path'] = handler.request.path
	
	outString = template.render(temp, newval)
	handler.response.out.write(outString)
	
	return True

		
def main():
	from dkbot import DateKeeperBotHandler;
	from schview import ScheduleViewerHandler;
	from datepost import DatePostHandler;
	
	application = webapp.WSGIApplication([
		('/DateKeeperBot/task', DateKeeperBotHandler),
		('/DateKeeperBot/view', ScheduleViewerHandler),
		('/DateKeeperBot/post', DatePostHandler),
		('/.*', MainHandler)],
		debug=True)
	wsgiref.handlers.CGIHandler().run(application)
	
if __name__ == '__main__':
	main()