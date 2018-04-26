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
# Filename: updateinterface by: andrek
# Timesamp:2018-01-15 :: 15:30 using PyCharm

import json
from abc import abstractmethod

import tenforward_client.utils.three2two as three2two
from tenforward_client import logger
import tenforward_client.core.reporter as reporter


class UpdateInterface:
	"""
	Interface for our Monitor UPDATE behaviour
	"""

	def __init__(self, *args, **kwargs):
		"""

		:param args: Tuple of Monitor Updates to instanciate
		:param kwargs: Optional List of KeyWord args.
		"""
		self.monitor = {}
		self.metrics = []
		self.reports = []

		self.reporter = reporter.Reporter()
		# Update behaviours as a tuple from the client
		if args:
			for i in args:
				monitor = i()
				self.monitor[monitor.__class__.__name__] = monitor

	@abstractmethod
	def update(self, *args, **kwargs):
		"""
		Abstract class that needs to be implemented in all Monitors
		:param args: Optional list of Monitors to update
		:param kwargs: Optional list of KeyWord args
		:return: List of stats from all updated monitors
		"""

		self.metrics = []

		logger.info("Do something before real update")
		# IF no args then update all update behaviours in list
		if not args:
			for (classname, instance) in three2two.iteritems(self.monitor):
				# Return data from monitor (classname)
				stat = instance.update(*args, **kwargs)
				logger.info("Do something with THIS update metrics for monitor {}".format(classname))
				# This is now a list of dicts, probably not OK, need dict
				self.metrics.append(stat)

		# We have args and only update those behaviours
		else:
			for inst in args:
				cname = inst.__class__.__name__
				if cname in self.monitor:
					stat = inst.update(**kwargs)
					logger.info("Do something with THIS update metrics for monitor {}").format(cname)
					# This is now a list of dicts, probably not OK, need dict
					self.metrics.append(stat)

		logger.info("Do something with all update metrics")
		print(self.metrics)
		return self.metrics

	@abstractmethod
	def report(self, *args, **kwargs):
		"""
		Abstract class that needs to be implemented in all Monitors
		:param args: Optional list of Monitors to update
		:param kwargs: Optional list of KeyWord args
		:return: List of stats from all updated monitors
		"""

		self.reports = []

		logger.info("Do something before real update")
		# IF no args then update all update behaviours in list
		if not args:
			for (classname, instance) in three2two.iteritems(self.monitor):
				# Return data from monitor (classname)
				stat = instance.report(*args, **kwargs)
				logger.info("Do something with THIS update metrics for monitor {}".format(classname))
				# This is now a list of dicts, probably not OK, need dict
				self.reports.append(stat)

		# We have args and only update those behaviours
		else:
			for inst in args:
				cname = inst.__class__.__name__
				if cname in self.monitor:
					stat = inst.report(**kwargs)
					logger.info("Do something with THIS update metrics for monitor {}").format(cname)
					# This is now a list of dicts, probably not OK, need dict
					self.reports.append(stat)

		logger.info("Do something with all update metrics")
		for adict in self.reports:
			self.reporter.send_data(adict)
		return self.reports

	@staticmethod
	def log_result_decorator(fct):
		"""Log (DEBUG) the result of the function fct."""

		def wrapper(*args, **kw):
			ret = fct(*args, **kw)
			logger.debug("%s %s %s return %s" % (
				args[0].__class__.__name__,
				args[0].__class__.__module__[len('metric_'):],
				fct.__name__, ret))
			return ret

		return wrapper