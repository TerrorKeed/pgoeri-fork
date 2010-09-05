import socket,urllib2 , os
from xml.dom import minidom
from traceback import print_exc
import xbmcplugin
import sys

#defines
GET_SPEED			= "downloadspeed"
GET_SPEEDLIMIT		= "speedlimit"
GET_STATUS			= "status"
GET_CURRENTFILECNT	= "currentfilecount"

STATE_RUNNING		= "RUNNING"
STATE_NOTRUNNING	= "NOT_RUNNING"
STATE_STOPPING		= "STOPPING"

ACTION_START	= "1 start"
ACTION_STOP		= "2 stop"
ACTION_PAUSE	= "3 pause"
ACTION_TOGGLE	= "4 toggle"

ACTION_SPEEDLIMIT	= "5 speed limit"
ACTION_MAXDOWNLOADS	= "6 max downloads"

ACTION_JD_UPDATE	= "7 update JDownloader"
ACTION_JD_RESTART	= "8 restart JDownloader"
ACTION_JD_SHUTDOWN	= "9 shutdown JDownloader"

ALL_ACTIONS = {
	ACTION_START:		30060,
	ACTION_STOP:		30061,
	ACTION_PAUSE:		30062,
	ACTION_TOGGLE:		30063,
	ACTION_SPEEDLIMIT:	30064,
	ACTION_MAXDOWNLOADS:30065,
	ACTION_JD_UPDATE:	30066,
	ACTION_JD_RESTART:	30067,
	ACTION_JD_SHUTDOWN:	30068
}

BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )

# Handle settings
pluginhandle = int(sys.argv[1])
ip_adress = str(xbmcplugin.getSetting(pluginhandle,"ip_adress"))
ip_port = str(xbmcplugin.getSetting(pluginhandle,"ip_port"))

urlPrefix = 'http://' + ip_adress + ':' + ip_port

from convert import set_entity_or_charref
from convert import translate_string

# Get Info #

# As long as only the package info gets parsed, it doesn't matter which list gets loaded (currentlist,alllist,finishedlist)
# These three only differ in means of listed files, the package information is always the same.
# Due to that, the smallest will be used: currentlist
def get_downloadlist(x):
	xmlfile = os.path.join( BASE_RESOURCE_PATH , "dlist.xml" )
	#urlStr = urlPrefix + '/get/downloads/%s % x
	urlStr = urlPrefix + '/get/downloads/currentlist'
	print "url: %s" % urlStr
	try:
		fileHandle = urllib2.urlopen(urlStr)
		str1 = fileHandle.read()
		fileHandle.close()
		
		fileObj = open(xmlfile,"w")
		fileObj.write(str1)
		fileObj.close()
		
		xmldoc = minidom.parseString(str1)
		itemlist = xmldoc.getElementsByTagName('package')
		filelist = []
		for s in itemlist :
			package = {}
			package["Name"] = s.attributes['package_name'].value + " "
			package["Eta"] = s.attributes['package_ETA'].value+ " "
			package["Size"] = s.attributes['package_size'].value+ " "
			package["Percentage"] = s.attributes['package_percent'].value
			filelist.append(package)
			return filelist
			#return(packageName, packageEta, packageSize, packagePercentage) debug
			
	except IOError:
		print_exc()
		return 'error'


def get(x):
	if x == GET_SPEED:
		getStr = '/get/speed'
	if x == GET_SPEEDLIMIT:
		getStr = '/get/speedlimit'
	if x == GET_STATUS:
		getStr = '/get/downloadstatus'
	if x == GET_CURRENTFILECNT:
		getStr = '/get/downloads/currentcount'
	
	fileHandle = urllib2.urlopen(urlPrefix+getStr)
	str1 = fileHandle.read()
	fileHandle.close()
	if str1.startswith("0"): str1 = 'none'
	return str1

# Actions #

def getAvailableActions():
	actions = ALL_ACTIONS.keys();
	
	actions.sort();
	
	status = get(GET_STATUS)
	if STATE_NOTRUNNING in status: 
		for i in [ACTION_STOP,ACTION_PAUSE,ACTION_SPEEDLIMIT,ACTION_MAXDOWNLOADS]:
			actions.remove(i)
	elif STATE_RUNNING in status:
		actions.remove(ACTION_START)
	elif STATE_STOPPING in status: # no status changes possible 
		for i in [ACTION_START,ACTION_STOP,ACTION_PAUSE,ACTION_TOGGLE,ACTION_SPEEDLIMIT,ACTION_MAXDOWNLOADS]:
			actions.remove(i)
	return actions

def action( x , limit = "0" ):
	if x == ACTION_START:
		actionStr = '/action/start'
	if x == ACTION_STOP:
		actionStr = '/action/stop'
	if x == ACTION_PAUSE:
		actionStr = '/action/pause'
	if x == ACTION_TOGGLE:
		actionStr = '/action/toggle'
	if x == ACTION_SPEEDLIMIT:
		actionStr = '/action/set/download/limit/' + str(limit)
	if x == ACTION_MAXDOWNLOADS:
		actionStr = '/action/set/download/max/' + str(limit)
	if x == ACTION_JD_UPDATE:
		actionStr = '/action/update/force%s/' % str(limit)
	if x == ACTION_JD_RESTART:
		actionStr = '/action/restart'
	if x == ACTION_JD_SHUTDOWN:
		actionStr = '/action/shutdown'

	urlStr = urlPrefix+actionStr
	print "url: %s" % urlStr
	fileHandle = urllib2.urlopen(urlStr)
	result = fileHandle.read()
	fileHandle.close()
	return result

def action_addcontainer(grabber,start,link):
	urlStr = urlPrefix + '/action/add/container/grabber' + str(grabber) + '/start' + str(start) + '/' + str(link)
	fileHandle = urllib2.urlopen(urlStr)
	fileHandle.close()

# Links must be seperated by spaces
def action_addlinks(grabber,start,link):
	urlStr = urlPrefix + '/action/add/links/grabber' + str(grabber) + '/start' + str(start) + '/' + str(link)
	fileHandle = urllib2.urlopen(urlStr)
	str1 = fileHandle.read()
	fileHandle.close()
