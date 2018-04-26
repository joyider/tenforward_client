# -*- coding: utf-8 -*-config.reporting.url
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
# Filename: restconsumer by: andrek
# Timesamp:2018-01-18 :: 10:29 using PyCharm

import requests
import json
from tenforward_client.utils.three2two import httplib2
from tenforward_client.utils.helpers import singleton
import copy

from tenforward_client import config


@singleton
class APIClient:
	def __init__(self):
		self.http = httplib2.Http()
		self.header = {'Authorization': 'Bearer %s' % (config.auth.jwt_token), 'Content-Type': 'application/json', 'User-Agent': 'Tenforward_Client'}
		print(self.header)

	def _http(self, url, method, header, body):
		response, content = self.http.request(url, method, headers=header, body=json.dumps(body))

		return response

	def send_data(self, url, body):
		self._http(url, 'POST', self.header, body)
