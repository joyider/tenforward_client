# -*- coding: utf-8 -*-
# tenforward_client(c) 2017 by Andre Karlsson<andre.karlsson@protractus.se>
#
# This file is part of tenforward_client.
#
#    tenforward_client is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    tenforward_client is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with tenforward_client.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Filename: client by: andrek
# Timesamp:2017-10-03 :: 00:24 using PyCharm Community Edition

import sched
import time


class Client:

	def __init__(self, *args, **kwargs):
		self.update_time = 5
		self.sched = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)

	def __loop(self):
		"""
		This is the magic scheduler for the monitoring modules (as for now anyway)
		:return: Nothing
		"""
		self.sched.enter(self.update_time, priority=0, action=self.__loop, argument=())

		print("In Loop")

	def loop(self):
		"""
		This is a wrapper for __loop function,
		:return: Nothing
		"""
		self.__loop()
		try:
			self.sched.run()
		finally:
			self.end()

	def end(self):
		"""
		End Resources
		:return: Nothing

		"""
		pass

if __name__ == "__main__":
	Client().loop()
