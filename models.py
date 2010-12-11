from google.appengine.ext import db
from google.appengine.tools import bulkloader

class Keys(db.Model):
	appli_name = db.StringProperty()
	consum_key = db.StringProperty()
	consum_sec = db.StringProperty()
	access_key = db.StringProperty()
	access_sec = db.StringProperty()
	
class KeysLoader(bulkloader.Loader):
	""" read twitter keys and secrets from a csv file
	"""
	def __init__(self):
		bulkloader.Loader.__init__(self, 'Keys',
							[('appli_name', str),
							 ('consum_key', str),
							 ('consum_sec', str),
							 ('access_key', str),
							 ('access_sec', str)
							])

loaders = [KeysLoader]