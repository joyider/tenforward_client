# -*- coding: utf-8 -*-
# tenforward_client(c) 2018 by Andre Karlsson<andre.karlsson@protractus.se>
#
# --.--          ,---.                             |
#   |  ,---.,---.|__. ,---.,---.. . .,---.,---.,---|
#   |  |---'|   ||    |   ||    | | |,---||    |   |
#   `  `---'`   '`    `---'`    `-'-'`---^`    `---'
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
# Filename: alertmanager by: andrek
# Timesamp:2018-05-01 :: 11:11 using PyCharm

from tenforward_client.utils.helpers import singleton
import  inspect

@singleton
class AlertManager:
	registered_monitores = {}
	counter = {}

	def __init__(self, name):
		self.registered_monitores.append(name)

	def check(self, parameter, value):
		stack = inspect.stack()
		monitor = stack[1][0].f_locals["self"].__class__.__name__
		print(self.registered_monitores[monitor].get(parameter))

		#if value >= self.registered_monitores[monitor].get(parameter):
		#	print("Got alert")
