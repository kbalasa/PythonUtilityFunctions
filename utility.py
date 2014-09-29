#!/bin/env python
__author__ = "Krishna Balasa"
'''
This program has the following:
	1. Commonly used functions 
'''
from datetime import datetime
from datetime import timedelta


def sendEmail(fromAddress, toAddress, subject, msg):
	import smtplib
	from email.mime.text import MIMEText

	emailMsg = MIMEText(msg)
	emailMsg['Subject'] = subject 
	emailMsg['From'] = fromAddress 
	emailMsg['To'] = toAddress 

	smtpObj = smtplib.SMTP('localhost')
	smtpObj.sendmail(fromAddress, toAddress, emailMsg.as_string())
	smtpObj.quit()

def logProgramCompletion(programName):
	import config
	import os, json
	
	processLogFile = os.path.join(config.BOLETL_HOME, 'monitoring/programs_succeeded.data')

	# update the processes	
	pLogFile = open(processLogFile, 'r')
	processes = json.loads(pLogFile.read())
	pLogFile.close()
	pLogFile = open(processLogFile, 'w')
	processes[programName] = 1
	pLogFile.write(json.dumps(processes))
	pLogFile.close()

def checkProgramCompletion():
	import config
	import os, json
	
	processLogFile = os.path.join(config.BOLETL_HOME, 'monitoring/programs_succeeded.data')
	processListFile = os.path.join(config.BOLETL_HOME, 'monitoring/programs_to_monitor.data')
	
	pLogFile = open(processLogFile, 'r')
	pLog = json.loads(pLogFile.read())
	pLogFile.close()

	pMasterFile = open(processListFile, 'r')
	pMaster = json.loads(pMasterFile.read())
	pMasterFile.close()
	
	emailMsg = ""
	for p in pMaster:
		if p not in pLog:
			emailMsg += "Failed program : " + p + "\n"

	if len(emailMsg) > 0:
		sendEmail(config.EMAIL_NOTIFICATION['fromAddress'], config.EMAIL_NOTIFICATION['toAddress'], 'Failed Processes', emailMsg)
	else:
		print "All good"

	pLogFile = open(processLogFile, 'w')
	t = {}
	pLogFile.write(json.dumps(t))
	pLogFile.close()

def getCurrentLocalDateTime():
	"""
	Return current local date & time object
	"""
	return datetime.today()

def addDaysToGivenDate(dateVar, daysVar):
	"""
	Adds days to given date and retuns date object
	"""
	return dateVar + timedelta(days=daysVar)

def convertStrToDate(dateStr):
	"""
	Converts date string to date object and returns date object
	"""
	return datetime.strptime(dateStr, '%Y-%m-%d')

def convertDateToStr(dateVar):
	"""
	Converts date object to date string and returns date string
	"""
	return dateVar.strftime('%Y-%m-%d')

def getDaysInBetweenDates(dateEnd, dateStart):
	return abs((dateEnd -dateStart).days)

def getMD5Hash(strVar):
	import hashlib 
	return hashlib.md5(strVar).hexdigest()

def getCurrentDate():
	return str((datetime.now()).strftime('%Y-%m-%d'))

def getCurrentTime():
	return str((datetime.now()).strftime('%H:%M:%S'))

def getLogger(fileName, module, loggingLevel='DEBUG'):
	"""
	Configures and returns logger object.
	"""	
	import logging
	import logging.handlers

	if loggingLevel == 'DEBUG':
		logLevel = logging.DEBUG
	elif loggingLevel == 'WARNING':
		logLevel = logging.WARNING
	elif loggingLevel == 'INFO':
		logLevel = logging.INFO
	elif loggingLevel == 'CRITICAL':
		logLevel = logging.CRITICAL
	
	formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')		
	h = logging.handlers.RotatingFileHandler(fileName, \
			maxBytes=1000000, backupCount=10)
	h.setFormatter(formatter)
		
	logger = logging.getLogger(module)
	if logger.handlers:
		return logger
	logger.setLevel(logLevel)
	logger.addHandler(h)
	return logger

if __name__ == '__main__':
	#print convertDateToStr(addDaysToGivenDate(getCurrentLocalDateTime(), -1))
	print convertDateToStr( addDaysToGivenDate( convertStrToDate('2618-03-22'), 1))
