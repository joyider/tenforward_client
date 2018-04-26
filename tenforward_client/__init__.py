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
# Filename: __init__ by: andrek
# Timesamp:2018-01-17 :: 22:12 using PyCharm

import sys
import os
from tenforward_client.core.logger import Logger

import tenforward_client.core.config as config
from tenforward_client.core.cpumeter import CpuMeter
from tenforward_client.core.reporter import Reporter


logger = Logger()
cpumeter = CpuMeter()

# Global name
__version__ = '0.1'
__author__ = 'Andre Karlsson <andre.karlsson@protractus.com>'
__license__ = 'LGPLv3'


platforms = {
	'LINUX': sys.platform.startswith('linux'),
	'SUNOS': sys.platform.startswith('sunos'),
	'MACOS': sys.platform.startswith('darwin'),
	'BSD': sys.platform.find('bsd') != -1,
	'WINDOWS': sys.platform.startswith('win')
}

platform = next((k for k, v in platforms.items() if v), None)

work_path = os.path.realpath(os.path.pardir)
metrics_path = os.path.realpath(os.path.join(work_path, 'tenforward_client/monitors'))
sys_path = sys.path[:]
sys.path.insert(1, metrics_path)