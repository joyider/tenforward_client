# -*- coding: utf-8 -*-
# tenforward_client(c) 2017 by Andre Karlsson<andre.karlsson@protractus.se>
#
# This file is part of tenforward_client.
#
#    tenforward_client is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    tenforward_client is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with tenforward_client.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Filename: chronometer by: andrek
# Timesamp:2018-01-18 :: 00:03 using PyCharm

from time import time
from datetime import datetime

# Global list to manage the elapsed time
last_update_times = {}




def getTimeSinceLastUpdate(monitortype):
	"""
	Get time delta since last time monitor update
	:param monitortype: Monitor Type list on ['cpu','mem','disk]
	:return: actual time since last update for requested Monitor type
	"""
	#TODO Remove global
	global last_update_times
	current_time = time()
	last_time = last_update_times.get(monitortype)
	if not last_time:
		time_since_update = 1
	else:
		time_since_update = current_time - last_time
	last_update_times[monitortype] = current_time
	return time_since_update


class Chronometer:
	"""

	"""

	def __init__(self, duration):
		self.duration = duration
		self.start()

	def start(self):
		self.target = time() + self.duration

	def reset(self):
		self.start()

	def get(self):
		return self.duration - (self.target - time())

	def set(self, duration):
		self.duration = duration

	def finished(self):
		return time() > self.target


class Counter:
	"""

	"""

	def __init__(self, autostart=True):
		if autostart:
			self.start()

	def start(self):
		self.target = datetime.now()

	def reset(self):
		self.start()

	def get(self):
		return (datetime.now() - self.target).total_seconds()