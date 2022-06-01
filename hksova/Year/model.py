import time
from flask import current_app
import re

from ..Settings.model import *

def get_current_year():
	cursor = current_app.mysql.connection.cursor()	
	cursor.execute('''SELECT max(idYear) as idYear FROM year''')
	data = cursor.fetchall()
	return data[0]['idYear']

def get_year(blueprint_year):
	pattern = re.compile(r'.+?(\d+)$')
	if (pattern.match(blueprint_year)):
		return pattern.search(blueprint_year).groups()[0]
	else:
		return get_current_year()