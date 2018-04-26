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
# Filename: client by: andrek
# Timesamp:2017-10-03 :: 00:24 using PyCharm Community Edition

import sched
import time
import os

import tenforward_client.utils.scheduler as scheduler

from tenforward_client import config, logger
from tenforward_client.core.monitors import Monitors


class Client:

	def __init__(self, *args, **kwargs):
		self.check_time = int(config.checks.freq)
		self.report_time = int(config.reporting.freq)
		self.sched_checks = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
		self.sched_reports = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
		self.monitors = Monitors()

	def loop(self):
		"""
		This is a wrapper for __loop function,
		:return: Nothing
		"""

		scheduler.every(self.check_time).seconds.do(self.monitors.update)
		scheduler.every(self.report_time).seconds.do(self.monitors.report)

		while True:
			scheduler.run_pending()
			time.sleep(1)

	def end(self):
		"""
		End Resources
		:return: Nothing

		"""
		pass

if __name__ == "__main__":
	config.add_config_ini('./config.ini')
	logger.info('Starting')
	print('%s %s' % (config.auth.jwt_token, config.auth.identifier))
	config.kalle.kula = 'test'
	print('%s %s %s' % (config.auth.jwt_token, config.auth.identifier, config.kalle.kula))
	Client().loop()
