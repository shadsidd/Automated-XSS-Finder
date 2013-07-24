#!/usr/bin/env python


import ConfigParser

# -------------------------------------
class ConfigHelper:
# -------------------------------------

	_configObj = None
	
	# -------------------------------------
	def __init__(self, configFile=None, debug=False):
	# -------------------------------------

		self._configObj = ConfigParser.SafeConfigParser()
		self._configObj.read(configFile)
	
		if debug == True:
			for section in self._configObj.sections():
				for option in self._configObj.options(section):
					print '[%s] %s = %s' % (section,option,self._configObj.get(section,option))
	
	# -------------------------------------
	def getSections(self):
	# -------------------------------------
	
		return self._configObj.sections()
		
	# -------------------------------------
	def getOptions(self,section):
	# -------------------------------------
	
		if section not in self._configObj.sections():
			return None
		else:
			return self._configObj.options(section)
	
	# -------------------------------------
	def get(self,section,option):
	# -------------------------------------
		
		if section not in self._configObj.sections() or option not in self._configObj.options(section):
			return None
		else:
			return self._configObj.get(section,option)
