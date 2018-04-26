# -*- coding: utf-8 -*-
# tenforward_client(c) 2017-2018 by Andre Karlsson<andre.karlsson@protractus.se>
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
# Filename: reporter by: andrek
# Timesamp:2018-01-21 :: 23:46 using PyCharm

import json

from tenforward_client import config
from tenforward_client.utils.helpers import singleton
from  tenforward_client.utils.three2two import iteritems
import tenforward_client.core.restconsumer as restclient


@singleton
class Reporter:

	def __init__(self, *args, **kwargs):

		self.restclient = restclient.APIClient()

	def send_data(self, report_data):

		url = '%s/metric_cpu' % (config.reporting.url)
		print(url)
		resp = self.restclient.send_data(url, report_data)

		print(json.dumps(report_data))
		print(resp)
		#headers = {'Authorization': 'Bearer %s' % config.auth.jwt_token, 'Content-Type': 'application/json'}
		#print(headers)
		#for key, value in iteritems(report_data):
		#	this_check = '%s' % (self.identifer)
		#	self.restclient.metric_cpu.POST(params=json.dumps(report_data), headers={'Authorization': 'Bearer %s' % config.auth.jwt_token, 'Content-Type': 'application/json'})
		#	#resp = getattr(self.restclient, this_check).POST(json.dumps(report_data), headers={'Authorization': 'Bearer %s' % config.auth.jwt_token})
		#	print(json.dumps(report_data))
		#	#print(resp)


