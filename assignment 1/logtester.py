
import sys

import config
from logger import Logger

def Main():
	logger = Logger(config.CLIENTLOG, config.LOGLEVEL)
	logger.logDebug("test print, are you seeing this?")
	logger.logMsg("Connection established successfully")
	logger.logError("Something went seriously wrong")
	logger.closeFile()


Main()
