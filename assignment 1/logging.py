# Generic logging functionality

import datetime

class Logging:

	def __init__(self, logpath, loglevel):
		self.loglevel = loglevel
		self.logpath = logpath
		self.logfile = self.openLogfile()

	def setLogpath(self, filename):
		self.logpath = filename

	def openLogfile(self):
		if self.logpath != None:
			fd = open(self.logpath, 'w+')
			if fd != None:
				return fd
			else:
				print("Error: Failed to open log file")
				return None
		else:
			print("Error: Logfile path not specified!")

	def logError(self, msg):
		if self.loglevel > 0:
			self.logfile.write(str(datetime.datetime.now()) + " - " + msg + '\n')

	def logMsg(self, msg):
		if self.loglevel > 1:
			self.logfile.write(str(datetime.datetime.now()) + " - " + msg + '\n')

	def logDebug(self, msg):
		if self.loglevel > 2:
			self.logfile.write(str(datetime.datetime.now()) + " - " + msg + '\n')

	def closeFile(self):
		self.logfile.close()
