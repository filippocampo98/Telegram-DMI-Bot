# -*- coding: utf-8 -*-
import re
class StringParser(object):
	@staticmethod
	def remove_cfu(string_to_parse):
		updated_string = re.sub('\s?[0-9] CFU.*', '', string_to_parse)
		return updated_string
	@staticmethod
	def starts_with_upper(string_to_parse):
		string_to_parse = string_to_parse[0].upper()+string_to_parse[1:]
		return string_to_parse
