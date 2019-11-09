
import sys

import config
from logging import Logging

def Main():
	logger = Logging(config.CLIENTLOG, config.LOGLEVEL)
	logger.logDebug("test print, are you seeing this?")
	logger.logMsg("Connection established successfully")
	logger.logError("Something went seriously wrong")
	logger.closeFile()


Main()
