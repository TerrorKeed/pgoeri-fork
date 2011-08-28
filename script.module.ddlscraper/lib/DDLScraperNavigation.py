import sys, urllib, os
import xbmc, xbmcgui, xbmcplugin
	
class DDLScraperNavigation:	 
	__addon__		= sys.modules[ "__main__" ].__addon__
	__language__	= sys.modules[ "__main__" ].__language__
	__plugin__		= sys.modules[ "__main__" ].__plugin__
	__dbg__			= sys.modules[ "__main__" ].__dbg__
	__JDaddonID__	= sys.modules[ "__main__" ].__JDaddonID__
	
	plugin_thumbnail_path = os.path.join( __addon__.getAddonInfo('path'), "thumbnails" )

	#==================================== Main Entry Points===========================================
	def listMenu(self, params = {}):
		get = params.get

		# if there is a link in feeds dictionary, this means this is a real category
		if ( get("feed") in self.feeds):
			self.listCategoryFolder(params)
			return
		
		# otherwhise it has to be the root or some meta directory
		path = get("path", "/root")
		
		# hide subcategories, open 'all' immediatly
		if ( path!="/root" and self.__addon__.getSetting("subcat") == "true" ):
			# search for subcategory 'all'
			for menuitem in self.menuitems:
				if ( menuitem.get("path") == (path+"/all") ):
					# the following function expects a dictionary with the keys: feed & path -> so just use the menuitem
					self.listCategoryFolder(menuitem)
					return
			
		# add all items that belong to this path (root or meta directory)
		for menuitem in self.menuitems:
			item_get = menuitem.get 
			if (item_get("path").find(path +"/") > -1 ):
				if (item_get("path").rfind("/") <= len(path +"/")):
					# Hide entries in main menu according to the settings
					if ( path!="/root" or self.__addon__.getSetting( item_get("path").replace("/root/", "") ) != "true"):
						self.addListItem(params, menuitem)
		
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True, cacheToDisc=True )

	def executeAction(self, params = {}):
		get = params.get
		if (get("action") == "add_link"):
			self.addLink(params)
		elif (get("action") == "open_settings"):
			self.__addon__.openSettings()
			xbmc.executebuiltin("XBMC.Container.Refresh")

	def listCategoryFolder(self, params = {}):
		get = params.get

		feed = get("feed")
		link = self.feeds[feed]
		
		# special handling for search
		if (feed == "search"):
			if (not get("searchstr")):
				kb = xbmc.Keyboard();
				kb.setHeading("Search...")
				kb.doModal()
				if (kb.isConfirmed()):
					params["searchstr"] = kb.getText();
				else:
					return False
				
			if (get("searchstr")):
				link += get("searchstr")
		
		( result, status ) = self._core.scrapePosts(link, int(get("page", "0")) )
		if status != 200:
			feed_label = ""
			for menuitem in self.menuitems:
				item_get = menuitem.get
				if (item_get("action") == get("feed")):
					feed_label = item_get("label")
					break
				
			if (feed_label != ""):
				self.errorHandling(feed_label, result, status)
			else:
				self.errorHandling(get("feed"), result, status)
				
			return False
		
		self.parsePostList(get("path"), params, result);
	
	#================================== Plugin Actions =========================================

	def addLink(self, params = {}):
		get = params.get
		if (get("url")):
			( file_links , status ) = self._core.scrapeFilehosterLinks( get("url") )
			if status != 200:
				self.errorHandling(self.__language__(30801), file_links, status)
				return False
			
			try:
				for link in file_links:
					xbmc.executebuiltin('XBMC.RunPlugin(plugin://%s/?action=addlink&url=%s)' % ( self.__JDaddonID__, link ) )
				self.showMessage(self.__language__(30802),self.__language__(30800) % len(file_links))
			except jdownloader.JDError, error:
				(type, e, traceback) = sys.exc_info()
				self.showMessage(self.__language__(30803), e.message)
	
	#================================== List Item manipulation =========================================	
	def addDefaultContextMenu(self, cm):
		# always add 'addon settings' to context menu
		cm.append( (self.__language__(30502), 'XBMC.RunPlugin(%s?&action=open_settings&)' % ( sys.argv[0] ) ) )
		cm.append( (self.__language__(30503), 'XBMC.ActivateWindow(programs,plugin://%s/)' % (self.__JDaddonID__, ) ) )
	
	# is only used by List Menu
	def addListItem(self, params = {}, item_params = {}):
		get = params.get
		item = item_params.get
		
		if (not item("action")):
			self.addFolderListItem(params, item_params)
		else :
			self.addActionListItem(params, item_params)
 
	# common function for adding folder items
	def addFolderListItem(self, params = {}, item_params = {}, size = 0):
		get = params.get
		item = item_params.get
		
		icon = "DefaultFolder.png"
		thumbnail = item("thumbnail")
		cm = []
		
		if (item("thumbnail", "DefaultFolder.png").find("http://") == -1):
			thumbnail = self.getThumbnail(item("thumbnail"))
			
		listitem=xbmcgui.ListItem( item("label"), iconImage=icon, thumbnailImage=thumbnail )
		
		# create plugin link for this folder item
		url = '%s?path=%s&' % ( sys.argv[0], item("path") )
		
		if (item("action")):
			url += "action=" + item("action") + "&"
		
		if (item("feed")):   
			url += "feed=" + item("feed") + "&"
		
		if (item("page")):
			url += "page=" + item("page") + "&"
		
		if (item("searchstr")):
			url += "searchstr=" + item("searchstr") + "&"
			
		self.addDefaultContextMenu(cm)

		if len(cm) > 0:
			listitem.addContextMenuItems( cm, replaceItems=True )
		listitem.setProperty( "Folder", "true" )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=True, totalItems=size)
	
	# common function for adding action items
	def addActionListItem(self, params = {}, item_params = {}, size = 0):
		get = params.get
		item = item_params.get
		folder = False
		icon = "DefaultFolder.png"
		thumbnail = self.getThumbnail(item("thumbnail"))
		listitem=xbmcgui.ListItem( item("label"), iconImage=icon, thumbnailImage=thumbnail )
		
		if (item("action") == "search" or item("action") == "settings"):
			folder = True
		else:
			listitem.setProperty('IsPlayable', 'true');
			
		url = '%s?path=%s&' % ( sys.argv[0], item("path") )
		url += 'action=' + item("action") + '&'
			
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=folder, totalItems=size)
	
	# common function for adding post items
	def addPostListItem(self, params = {}, item_params = {}, listSize = 0): 
		get = params.get
		item = item_params.get
		
		icon = item("img", "DefaultFolder.png")
		listitem=xbmcgui.ListItem(item("Title"), iconImage=icon, thumbnailImage=item("img") )

		url = '%s?path=%s&action=add_link&url=%s' % ( sys.argv[0], item("path"), item("url"));
			
		cm = []
		
		# add 'video info' to context menu
		cm.append( ( self.__language__( 30500 ), "XBMC.Action(Info)", ) )
		
		self.addDefaultContextMenu(cm)
		
		listitem.addContextMenuItems( cm, replaceItems=True )

		listitem.setInfo(type='Video', infoLabels=item_params)
		
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=False, totalItems=listSize + 1)
		
	#==================================== Core Output Parsing Functions ===========================================

	#parses a folder list consisting of a tuple of dictionaries
	def parseFolderList(self, path, params, results):
		listSize = len(results)
		get = params.get
		
		next = False;
		for result_params in results:
			result = result_params.get
			next = result("next") == "true"
			
			feed = result("playlistId", "")
			
			if ( feed == "" ):
				feed = result("Title", "")
				
			result_params["label"] = result("Title")
			
			result_params["feed"] = feed
			result_params["action"] = feed
			
			result_params["path"] = path
			
			self.addFolderListItem( params, result_params, listSize + 1)
			
		if next:
			# prepare a special map with values that are needed for a new folder item
			item = {"path":get("path"), "label":self.__language__( 30501 ), "thumbnail":"next", "page":str(int(get("page", "0")) + 1)} 
			if (get("feed")):
				item["feed"] = get("feed")
			if (get("action")):
				item["action"] = get("action")
			if (get("searchstr")):
				item["searchstr"] = get("searchstr")
			
			self.addFolderListItem(params, item, listSize)
		
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True, cacheToDisc=False )
	
	#parses a post list consisting of a list of dictionaries 
	def parsePostList(self, path, params, results):
		listSize = len(results)
		get = params.get
		
		next = False
		for result_params in results:
			result = result_params.get
			next = result("next") == "true"
			
			result_params["label"] = result("Title")
			result_params["path"] = path
			self.addPostListItem( params, result_params, listSize)
		
		if next:
			# add all needed params for next page to the item representig the next page
			item = {"path":get("path"), "label":self.__language__( 30501 ), "thumbnail":"next", "page":str(int(get("page", "0")) + 1)} 
			if (get("feed")):
				item["feed"] = get("feed")
			if (get("action")):
				item["action"] = get("action")
			if (get("searchstr")):
				item["searchstr"] = get("searchstr")
			
			self.addFolderListItem(params, item)
		
		# change to videoview if set in settings
		video_view = self.__addon__.getSetting("video_view")
		
		if (video_view):
			xbmc.executebuiltin("Container.SetViewMode(500)")
		
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True, cacheToDisc=True )
		
	#=================================== Testing ======================================= 
	def testFeeds(self):
		self._core.testLinks(self.feeds.values())
			
		
	#=================================== Tool Box ======================================= 
	# shows a more userfriendly notification
	def showMessage(self, heading, message):
		duration = ([5, 10, 15, 20, 25, 30][int(self.__addon__.getSetting( 'notification_length' ))]) * 1000
		xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s)' % ( heading, message, duration) )

	# create the full thumbnail path for skins directory
	def getThumbnail( self, title ):
		if (not title):
			title = "DefaultFolder.png"
			
		thumbnail = os.path.join( sys.modules[ "__main__" ].__plugin__, title + ".png" )
		
		if ( not xbmc.skinHasImage( thumbnail ) ):
			thumbnail = os.path.join( self.plugin_thumbnail_path, title + ".png" )
			if ( not os.path.isfile( thumbnail ) ):
				thumbnail = "DefaultFolder.png"	
		
		return thumbnail

	# converts the request url passed on by xbmc to our plugin into a dict  
	def getParameters(self, parameterString):
		commands = {}
		splitCommands = parameterString[parameterString.find('?')+1:].split('&')
		
		for command in splitCommands: 
			if (len(command) > 0):
				splitCommand = command.split('=')
				name = splitCommand[0]
				value = splitCommand[1]
				commands[name] = value
		
		return commands

	def errorHandling(self, title = "", result = "", status = 500):
		if title == "":
			title = self.__language__(30600)
		if result == "":
			result = self.__language__(30602)
		
		if ( status == 303):
			self.showMessage(title, result)
		elif ( status == 500):
			self.showMessage(title, self.__language__(30601))
		else:
			self.showMessage(title, self.__language__(30602))
