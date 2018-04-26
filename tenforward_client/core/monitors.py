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
# Filename: monitors.py by: andrek
# Timesamp:2017-10-03 :: 00:33 using PyCharm Community Edition

import collections
import os
import sys
import threading
import traceback

from tenforward_client import logger, metrics_path, sys_path
from tenforward_client import metrics_path as exports_path

from tenforward_client.core.interfaces.updateinterface import UpdateInterface


class Monitors:

	"""This class stores, updates and gives stats."""

	# Script header constant
	header = "metric_"

	def __init__(self, config=None, args=None):
		# Set the config instance
		self.config = config

		# Set the argument instance
		self.args = args

		# Instance of UpdateInterface
		#Will contain all update methods for all monitors
		self.updates = None

		# Load metrics and exports modules
		self.load_modules(self.args)

		# Load the limits (for metrics)
		# self.load_confines(self.config)

	def __getattr__(self, item):
		"""Overwrite the getattr method in case of attribute is not found.
		The goal is to dynamically generate the following methods:
		- getmetricname(): return metricname stat in JSON format
		- getViewsmetricname(): return views of the metricname stat in JSON format
		"""
		# Check if the attribute starts with 'get'
		if item.startswith('getViews'):
			# Get the metric name
			metricname = item[len('getViews'):].lower()
			# Get the metric instance
			metric = self._metrics[metricname]
			if hasattr(metric, 'get_json_views'):
				# The method get_views exist, return it
				return getattr(metric, 'get_json_views')
			else:
				# The method get_views is not found for the metric
				raise AttributeError(item)
		elif item.startswith('get'):
			# Get the metric name
			metricname = item[len('get'):].lower()
			# Get the metric instance
			metric = self._metrics[metricname]
			if hasattr(metric, 'get_stats'):
				# The method get_stats exist, return it
				return getattr(metric, 'get_stats')
			else:
				# The method get_stats is not found for the metric
				raise AttributeError(item)
		else:
			# Default behavior
			raise AttributeError(item)

	def load_modules(self, args):
		"""Wrapper to load: metrics and export modules."""

		# Init the metrics dict
		self._metrics = collections.defaultdict(dict)

		# Load the metrics
		self.load_metrics(args=args)

		# Init the export modules dict
		#self._exports = collections.defaultdict(dict)

		# Load the export modules
		#self.load_exports(args=args)

		# Restoring system path
		sys.path = sys_path

	def _load_metric(self, metric_script, args=None, config=None):
		"""Load the metric (script), init it and add to the _metric dict"""
		# The key is the metric name
		# for example, the file metrics_xxx.py
		# generate self._metrics_list["xxx"] = ...
		name_full = metric_script[len(self.header):-3].lower()
		# This will break if the file name is messed up
		name = "%s%s" % (name_full[0].upper(), name_full[1:])+"Update"
		try:
			# Import the metric
			metric = __import__(metric_script[:-3])
			# Init and add the metric to the dictionary
			cls = getattr(metric, name)
			return cls
			#self._metrics[name] = cls(args=args)
		except Exception as e:
			# If a metric can not be log, display a critical message
			# on the console but do not crash
			logger.error("Error while initializing the {} metric ({})".format(name, e))
			logger.error(traceback.format_exc())

	def load_metrics(self, args=None):
		"""Load all metrics in the 'metrics' folder."""
		update = []
		for item in os.listdir(metrics_path):
			if not item.startswith('_') and "__pycache__" not in item:
				update.append(self._load_metric(os.path.basename(item),
				                  args=args, config=self.config))
		self.updates = UpdateInterface(*update)

		# Log metrics list
		# logger.debug("Available metrics list: {}".format(self.getAllmetrics()))

	def load_exports(self, args=None):
		"""Load all export modules in the 'exports' folder."""
		if args is None:
			return False
		header = "metrics_"
		# Transform the arguments list into a dict
		# The aim is to chec if the export module should be loaded
		args_var = vars(locals()['args'])
		for item in os.listdir(exports_path):
			export_name = os.path.basename(item)[len(header):-3].lower()
			if (item.startswith(header) and
				    item.endswith(".py") and
					    item != (header + "export.py") and
					    item != (header + "history.py") and
					    args_var['export_' + export_name] is not None and
					    args_var['export_' + export_name] is not False):
				# Import the export module
				export_module = __import__(os.path.basename(item)[:-3])
				# Add the export to the dictionary
				# The key is the module name
				# for example, the file glances_xxx.py
				# generate self._exports_list["xxx"] = ...
				self._exports[export_name] = export_module.Export(args=args, config=self.config)
		# Log metrics list
		logger.debug("Available exports modules list: {}".format(self.getExportList()))
		return True

	def getAllmetrics(self, enable=True):
		"""Return the enable metrics list.
		if enable is False, return the list of all the metrics"""
		if enable:
			return [p for p in self._metrics if self._metrics[p].is_enabled]
		else:
			return [p for p in self._metrics]

	def getExportList(self):
		"""Return the exports modules list."""
		return [e for e in self._exports]

	def load_confines(self, config=None):
		"""Load the stats limits (except the one in the exclude list)."""
		# For each metrics, call the load_confines method
		for p in self._metrics:
			self._metrics[p].load_confines(config)

	def update(self):
		"""Wrapper method to update the metrics."""
		self.updates.update()

	def report(self):
		"""Wrapper for the check reporting"""
		self.updates.report()

	def export(self, input_stats=None):
		"""Export all the stats.
		Each export module is ran in a dedicated thread.
		"""
		# threads = []
		input_stats = input_stats or {}

		for e in self._exports:
			logger.debug("Export stats using the %s module" % e)
			thread = threading.Thread(target=self._exports[e].update,
			                          args=(input_stats,))
			# threads.append(thread)
			thread.start()

	def getAll(self):
		"""Return all the stats (list)."""
		return [self._metrics[p].get_raw() for p in self._metrics]

	def getAllAsDict(self):
		"""Return all the stats (dict)."""
		return {p: self._metrics[p].get_raw() for p in self._metrics}

	def getAllExports(self):
		"""
		Return all the stats to be exported (list).
		Default behavor is to export all the stat
		"""
		return [self._metrics[p].get_export() for p in self._metrics]

	def getAllExportsAsDict(self, metric_list=None):
		"""
		Return all the stats to be exported (list).
		Default behavor is to export all the stat
		if metric_list is provided, only export stats of given metric (list)
		"""
		if metric_list is None:
			# All metrics should be exported
			metric_list = self._metrics
		return {p: self._metrics[p].get_export() for p in metric_list}

	def getAllLimits(self):
		"""Return the metrics limits list."""
		return [self._metrics[p].limits for p in self._metrics]

	def getAllLimitsAsDict(self, metric_list=None):
		"""
		Return all the stats limits (dict).
		Default behavor is to export all the limits
		if metric_list is provided, only export limits of given metric (list)
		"""
		if metric_list is None:
			# All metrics should be exported
			metric_list = self._metrics
		return {p: self._metrics[p].limits for p in metric_list}

	def getAllViews(self):
		"""Return the metrics views."""
		return [self._metrics[p].get_views() for p in self._metrics]

	def getAllViewsAsDict(self):
		"""Return all the stats views (dict)."""
		return {p: self._metrics[p].get_views() for p in self._metrics}

	def get_metric_list(self):
		"""Return the metric list."""
		return self._metrics

	def get_metric(self, metric_name):
		"""Return the metric name."""
		if metric_name in self._metrics:
			return self._metrics[metric_name]
		else:
			return None

	def end(self):
		"""End of the Glances stats."""
		# Close export modules
		for e in self._exports:
			self._exports[e].exit()
		# Close metrics
		for p in self._metrics:
			self._metrics[p].exit()