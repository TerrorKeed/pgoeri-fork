import sys, urllib, os
import xbmc, xbmcgui, xbmcplugin
import OneDDLCore

core = OneDDLCore.OneDDLCore();
	
class OneDDLNavigation:	 
	__addon__		= sys.modules[ "__main__" ].__addon__
	__language__	= sys.modules[ "__main__" ].__language__
	__plugin__		= sys.modules[ "__main__" ].__plugin__
	__dbg__			= sys.modules[ "__main__" ].__dbg__
	__JDaddonID__	= sys.modules[ "__main__" ].__JDaddonID__
	
	plugin_thumbnail_path = os.path.join( __addon__.getAddonInfo('path'), "thumbnails" )

	#===============================================================================
	# dictonary 'feeds' stores the links for all categories
	#===============================================================================
	feeds = {};
	feeds['all']			= "http://www.oneddl.com"
	#feeds['1click']			= "http://www.oneddl.com/category/1-click/"
	feeds['apps']			= "http://www.oneddl.com/category/apps/"
	feeds['ebooks']			= "http://www.oneddl.com/category/ebooks"
	feeds['comics']			= "http://www.oneddl.com/category/ebooks/comics"
	feeds['games']			= "http://www.oneddl.com/category/games"
	feeds['pc']				= "http://www.oneddl.com/category/games/pc"
	feeds['ps3']			= "http://www.oneddl.com/category/games/ps3"
	feeds['psp']			= "http://www.oneddl.com/category/games/psp"
	feeds['wii']			= "http://www.oneddl.com/category/games/wii"
	feeds['xbox360']		= "http://www.oneddl.com/category/games/xbox360"
	feeds['iphone']			= "http://www.oneddl.com/category/iphone"
	feeds['movies']			= "http://www.oneddl.com/category/movies"
	feeds['1080p']			= "http://www.oneddl.com/category/movies/1080p"
	feeds['720p']			= "http://www.oneddl.com/category/movies/720p"
	feeds['bdrip']			= "http://www.oneddl.com/category/movies/bdrip"
	feeds['bdscr']			= "http://www.oneddl.com/category/movies/bdscr-movies"
	feeds['brrip']			= "http://www.oneddl.com/category/movies/brrip"
	feeds['cam']			= "http://www.oneddl.com/category/movies/cam"
	feeds['dvdr']			= "http://www.oneddl.com/category/movies/dvdr"
	feeds['dvdrip']			= "http://www.oneddl.com/category/movies/dvdrip"
	feeds['dvdscr']			= "http://www.oneddl.com/category/movies/dvdscr"
	feeds['r5']				= "http://www.oneddl.com/category/movies/r5"
	feeds['scr']			= "http://www.oneddl.com/category/movies/scr"
	feeds['telecine']		= "http://www.oneddl.com/category/movies/telecine"
	feeds['telesync']		= "http://www.oneddl.com/category/movies/telesync"
	feeds['music']			= "http://www.oneddl.com/category/music"
	feeds['mp3']			= "http://www.oneddl.com/category/music/mp3"
	feeds['mvid']			= "http://www.oneddl.com/category/music/mvid"
	#feeds['sitenews']		= "http://www.oneddl.com/category/site-new" news, announcements, no downloads
	feeds['staffpicks']		= "http://www.oneddl.com/category/staff-picks"
	feeds['trailers']		= "http://www.oneddl.com/category/trailers"
	feeds['tvshows']		= "http://www.oneddl.com/category/tv-shows"
	feeds['tv720p']			= "http://www.oneddl.com/category/tv-shows/hd-720p"
	feeds['tvppv']			= "http://www.oneddl.com/category/tv-shows/ppv"
	feeds['tvsport']		= "http://www.oneddl.com/category/tv-shows/sport"
	feeds['tvdvdrip']		= "http://www.oneddl.com/category/tv-shows/tv-dvdrip"
	feeds['uncat']			= "http://www.oneddl.com/category/uncategorized"
	feeds['vodo']			= "http://www.oneddl.com/category/vodo"

	# we fill the list with menuitems, with labels from the appropriate language file
	#	label							,path							, thumbnail						feed
	menuitems = (
		{'label':__language__( 30000 )	,'path':"/root/all"				, 'thumbnail':"all"				, 'feed':"all" },
		# main categories
		{'label':__language__( 30001 )	,'path':"/root/tvshows"			, 'thumbnail':"tvshows"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/tvshows/all"		, 'thumbnail':"tvshows"			, 'feed':"tvshows" },
		{'label':__language__( 30002 )	,'path':"/root/tvshows/720p"	, 'thumbnail':"tvshows"			, 'feed':"tv720p" },
		{'label':__language__( 30003 )	,'path':"/root/tvshows/ppv"		, 'thumbnail':"tvshows"			, 'feed':"tvppv" },
		{'label':__language__( 30004 )	,'path':"/root/tvshows/sport"	, 'thumbnail':"tvshows"			, 'feed':"tvsport" },
		{'label':__language__( 30005 )	,'path':"/root/tvshows/dvdrip"	, 'thumbnail':"tvshows"			, 'feed':"tvdvdrip" },
		{'label':__language__( 30010 )	,'path':"/root/movies"			, 'thumbnail':"movies"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/movies/all"		, 'thumbnail':"movies"			, 'feed':"movies" },
		{'label':__language__( 30011)	,'path':"/root/movies/1080p"	, 'thumbnail':"movies"			, 'feed':"1080p" },
		{'label':__language__( 30012)	,'path':"/root/movies/720p"		, 'thumbnail':"movies"			, 'feed':"720p" },
		{'label':__language__( 30013)	,'path':"/root/movies/bdrip"	, 'thumbnail':"movies"			, 'feed':"bdrip" },
		{'label':__language__( 30014)	,'path':"/root/movies/bdscr"	, 'thumbnail':"movies"			, 'feed':"bdscr" },
		{'label':__language__( 30015)	,'path':"/root/movies/brrip"	, 'thumbnail':"movies"			, 'feed':"brrip" },
		{'label':__language__( 30016)	,'path':"/root/movies/cam"		, 'thumbnail':"movies"			, 'feed':"cam" },
		{'label':__language__( 30017)	,'path':"/root/movies/dvdr"		, 'thumbnail':"movies"			, 'feed':"dvdr" },
		{'label':__language__( 30018)	,'path':"/root/movies/dvdrip"	, 'thumbnail':"movies"			, 'feed':"dvdrip" },
		{'label':__language__( 30019)	,'path':"/root/movies/dvdscr"	, 'thumbnail':"movies"			, 'feed':"dvdscr" },
		{'label':__language__( 30020)	,'path':"/root/movies/r5"		, 'thumbnail':"movies"			, 'feed':"r5" },
		{'label':__language__( 30021)	,'path':"/root/movies/scr"		, 'thumbnail':"movies"			, 'feed':"scr" },
		{'label':__language__( 30022)	,'path':"/root/movies/telecine"	, 'thumbnail':"movies"			, 'feed':"telecine" },
		{'label':__language__( 30023)	,'path':"/root/movies/telesync"	, 'thumbnail':"movies"			, 'feed':"telesync" },
		{'label':__language__( 30030 )	,'path':"/root/music"			, 'thumbnail':"music"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/music/all"		, 'thumbnail':"music"			, 'feed':"music" },
		{'label':__language__( 30031 )	,'path':"/root/music/mp3"		, 'thumbnail':"music"			, 'feed':"mp3" },
		{'label':__language__( 30032 )	,'path':"/root/music/mvid"		, 'thumbnail':"music"			, 'feed':"mvid" },
		{'label':__language__( 30040 )	,'path':"/root/games"			, 'thumbnail':"games"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/games/all"		, 'thumbnail':"games"			, 'feed':"games" },
		{'label':__language__( 30041 )	,'path':"/root/games/pc"		, 'thumbnail':"games"			, 'feed':"pc" },
		{'label':__language__( 30042 )	,'path':"/root/games/ps3"		, 'thumbnail':"games"			, 'feed':"ps3" },
		{'label':__language__( 30043 )	,'path':"/root/games/psp"		, 'thumbnail':"games"			, 'feed':"psp" },
		{'label':__language__( 30044 )	,'path':"/root/games/wii"		, 'thumbnail':"games"			, 'feed':"wii" },
		{'label':__language__( 30045 )	,'path':"/root/games/x360"		, 'thumbnail':"games"			, 'feed':"xbox360" },
		{'label':__language__( 30050 )	,'path':"/root/ebooks"			, 'thumbnail':"ebooks"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/ebooks/all"		, 'thumbnail':"ebooks"			, 'feed':"ebooks" },
		{'label':__language__( 30051 )	,'path':"/root/ebooks/comics"	, 'thumbnail':"ebooks"			, 'feed':"comics" },
		{'label':__language__( 30055 )	,'path':"/root/apps"			, 'thumbnail':"apps"			, 'feed':"apps" },
		# miscellaneous
		{'label':__language__( 30060 )	,'path':"/root/misc"			, 'thumbnail':"misc"			, 'feed':"" },
		{'label':__language__( 30061 )	,'path':"/root/misc/iphone"		, 'thumbnail':"iphone"			, 'feed':"iphone" },
		{'label':__language__( 30062 )	,'path':"/root/misc/staffpicks"	, 'thumbnail':"misc"			, 'feed':"staffpicks" },
		{'label':__language__( 30063 )	,'path':"/root/misc/trailers"	, 'thumbnail':"misc"			, 'feed':"trailers" },
		{'label':__language__( 30064 )	,'path':"/root/misc/uncat"		, 'thumbnail':"misc"			, 'feed':"uncat" },
		{'label':__language__( 30065 )	,'path':"/root/misc/vodo"		, 'thumbnail':"misc"			, 'feed':"vodo" },
	)

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
		if (get("action") == "open_settings"):
			self.__addon__.openSettings()
			xbmc.executebuiltin("XBMC.Container.Refresh")

	def listCategoryFolder(self, params = {}):
		get = params.get

		( result, status ) = core.scrapePosts(self.feeds[get("feed")], int(get("page", "0")) )
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
			( file_links , status ) = core.scrapeFilehosterLinks( get("url") )
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
		url = '%s?path=%s&' % ( sys.argv[0], item("path") )
		
		if (item("action")):
			url += "action=" + item("action") + "&"
		
		if (item("feed")):   
			url += "feed=" + item("feed") + "&"
		
		if (item("page")):
			url += "page=" + item("page") + "&"
		
		# always add 'addon settings' to context menu
		cm.append( (self.__language__(30502), 'XBMC.RunPlugin(%s?path=%s&action=open_settings&)' % ( sys.argv[0], item("path" ) ) ) )
		cm.append( (self.__language__(30503), 'XBMC.ActivateWindow(programs,plugin://%s/)' % (self.__JDaddonID__, ) ) )

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
		# always add 'addon settings' to context menu
		cm.append( (self.__language__(30502), 'XBMC.RunPlugin(%s?path=%s&action=open_settings&)' % ( sys.argv[0], item("path") ) ) )
		
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
			item = {"path":get("path"), "label":self.__language__( 30501 ), "thumbnail":"next", "page":str(int(get("page", "0")) + 1)} 
			if (get("feed")):
				item["feed"] = get("feed")
			if (get("action")):
				item["action"] = get("action")
								 
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
			
			self.addFolderListItem(params, item)
		
		# change to videoview if set in settings
		video_view = self.__addon__.getSetting("video_view")
		
		if (video_view):
			xbmc.executebuiltin("Container.SetViewMode(500)")
		
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True, cacheToDisc=True )
		
	#=================================== Testing ======================================= 
	def testFeeds(self):
		core.testLinks(self.feeds.values())
			
		
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
