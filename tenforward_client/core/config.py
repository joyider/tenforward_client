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
# Filename: config by: andrek
# Timesamp:2018-01-17 :: 11:13 using PyCharm

from tenforward_client.utils.three2two import ConfigParser
import sys


class Config:
	class Section:
		def __init__(self, section_name, config):
			self.__section_name = section_name
			self.__config = config

		def __str__(self):
			return '%s: %s' % (self.__section_name, self.__config)

		def __getattr__(self, name):
			try:
				return self.__config.get(self.__section_name, name)
			except Exception as n_exp:
				print(('Can not find value for %s in config: %s\n' % (name, n_exp)))
				return None

		def set_attr(self, key, value):
			try:
				self.__config.set(self.__section_name, key, str(value))
			except Exception as n_exp:
				print(('Can not set value %s for %s to config: %s\n' % (value, key, n_exp)))

	def __init__(self, *args):
		self.__sections = dict()
		self.__config = ConfigParser()
		self.add_config_ini(*args)

	def __getattr__(self, name):
		if name not in self.__sections:
			self.__sections[name] = self.Section(name, self.__config)
		return self.__sections[name]

	def add_config_ini(self, *args):
		list(map(lambda config_file_path: self.__config.read(config_file_path), args))
		self.__sections = dict(
			[(section, self.Section(section, self.__config)) for section in self.__config.sections()])


sys.modules[__name__] = Config()


def add_config_ini(*args):
	sys.modules[__name__].add_config_ini(*args)
