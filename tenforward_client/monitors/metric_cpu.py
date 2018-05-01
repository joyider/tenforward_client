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
# Filename: metric_cpu by: andrek
# Timesamp:2018-01-18 :: 00:04 using PyCharm

import collections
import os

from tenforward_client.utils.chronometer import getTimeSinceLastUpdate
from tenforward_client.core.interfaces.updateinterface import UpdateInterface
from tenforward_client import config
from tenforward_client.utils.three2two import iteritems


from tenforward_client import logger
from tenforward_client import cpumeter

import psutil


class CpuUpdate(UpdateInterface):

	"""TenForward CPU plugin.
	'stats' is a dictionary that contains the system-wide CPU utilization as a
	percentage.
	"""

	'''
	Default Alert levels custom made levels can be set from GUI
	Possible LEVELS are FATAL, CRITICAL, ERROR, WARNING, INFO
	'''
	ALERT_LEVELS = {'total':
		                {'CRITICAL': 90, 'WARNING': 75}
	                }

	# Checks to send to remote DB
	NAMED_CHECKS = ['total', 'iowait', 'softirq', 'ctx_switches', 'interrupts', 'soft_interrupts']



	def __init__(self, *args, **kwargs):
		"""
		Do we need to call the superclass? i would prefer not to
		:param args: Optional args tuple
		:param kwargs: Optional KeyWord args dict
		"""
		# super(CpuUpdate, self).__init__(*args, **kwargs)
		self.prefix = self.__class__.__name__[:-6].lower()
		self.fn_for_db = os.path.basename(__file__)[:-3].lower()

		# Init stats
		self.reset()

		# Set initial value for CPU avarage
		self.cpu_queue_len = int(int(config.reporting.freq)/int(config.checks.freq))
		self.cpu_average = collections.deque(maxlen=self.cpu_queue_len)


		# Counter for alert triggers
		self.tot_crit_counter = 0
		self.tot_warn_counter = 0

		# Try to get the CPU Core count
		try:
			_, self.nb_core = cpumeter.get()
			self.nb_log_core = self.nb_core["logical"]
		except Exception:
			self.nb_log_core = 1

	def reset(self):
		"""Reset/init the stats."""
		self.stats = {}

	@UpdateInterface.log_result_decorator
	def update(self):
		"""Update CPU stats using the input method."""

		# Reset stats
		self.reset()

		# Grab stats into self.stats
		"""Update CPU stats using PSUtil."""
		# Grab CPU stats using psutil's cpu_percent and cpu_times_percent
		# Get all possible values for CPU stats: user, system, idle,
		# nice (UNIX), iowait (Linux), irq (Linux, FreeBSD), steal (Linux 2.6.11+)
		# The following stats are returned by the API but not displayed in the UI:
		# softirq (Linux), guest (Linux 2.6.24+), guest_nice (Linux 3.2.0+)
		self.stats['total'], _ = cpumeter.get()
		cpu_times_percent = psutil.cpu_times_percent(interval=0.0)
		for stat in ['user', 'system', 'idle', 'nice', 'iowait',
		             'irq', 'softirq', 'steal', 'guest', 'guest_nice']:
			if hasattr(cpu_times_percent, stat):
				self.stats[stat] = getattr(cpu_times_percent, stat)

		# Additionnal CPU stats (number of events / not as a %)
		# ctx_switches: number of context switches (voluntary + involuntary) per second
		# interrupts: number of interrupts per second
		# soft_interrupts: number of software interrupts per second. Always set to 0 on Windows and SunOS.
		# syscalls: number of system calls since boot. Always set to 0 on Linux.
		try:
			cpu_stats = psutil.cpu_stats()
		except AttributeError:
			logger.error('cpu_stats only available with PSUtil 4.1and above')
		else:
			# By storing time data we enable Rx/s and Tx/s calculations in the
			# XML/RPC API, which would otherwise be overly difficult work
			# for users of the API
			time_since_update = getTimeSinceLastUpdate('cpu')

			# Previous CPU stats are stored in the cpu_stats_old variable
			if not hasattr(self, 'cpu_stats_old'):
				# First call, we init the cpu_stats_old var
				self.cpu_stats_old = cpu_stats
			else:
				for stat in cpu_stats._fields:
					if getattr(cpu_stats, stat) is not None:
						self.stats[stat] = getattr(cpu_stats, stat) - getattr(self.cpu_stats_old, stat)

				self.stats['time_since_update'] = time_since_update

				# Core number is needed to compute the CTX switch limit
				self.stats['cpucore'] = self.nb_log_core

				# Save stats to compute next step
				self.cpu_stats_old = cpu_stats

			# Append to average FILO
			self.cpu_average.append(self.stats)

		return self.stats

	def report(self):
		"""
		report check vaules ro be saved in remote DB
		:return: Dictionary with items to report
		{'CPU':
			{'total': 35,
			'user': 22,
			'system': 13
			...
			...
			}
		}
		"""
		report_dict = collections.defaultdict(float)
		r_dict = collections.defaultdict(float)
		count = 1

		for mydict in self.cpu_average:
			for key, value in iteritems(mydict):
				if key in CpuUpdate.NAMED_CHECKS:
					report_dict[key] += value

		for key, value in iteritems(report_dict):
			r_dict[key] = value/self.cpu_queue_len

		#r_dict[]


		# Return the dict with CHECK Prefix
		return {'table_name': self.fn_for_db, self.prefix:  r_dict}
