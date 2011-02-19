import sys, urllib, os
import xbmc, xbmcgui, xbmcplugin
import IRFreeCore

core = IRFreeCore.IRFreeCore();
	
class IRFreeNavigation:	 
	__addon__		= sys.modules[ "__main__" ].__addon__
	__language__	= sys.modules[ "__main__" ].__language__
	__plugin__		= sys.modules[ "__main__"].__plugin__
	__dbg__			= sys.modules[ "__main__" ].__dbg__
	__JDaddonID__	= sys.modules[ "__main__" ].__JDaddonID__
	
	plugin_thumbnail_path = os.path.join( __addon__.getAddonInfo('path'), "thumbnails" )

	#===============================================================================
	# dictonary 'feeds' stores the links for all categories
	#===============================================================================
	feeds = {};
	feeds['all']			= "http://www.irfree.com"
	feeds['apps']			= "http://www.irfree.com/applications/"
	feeds['ebooks']			= "http://www.irfree.com/e-books"
	feeds['magazines']		= "http://www.irfree.com/e-books/magazines"
	feeds['games']			= "http://www.irfree.com/gamez"
	feeds['congames']		= "http://www.irfree.com/gamez/console-games"
	feeds['ps2']			= "http://www.irfree.com/gamez/console-games/ps2"
	feeds['ps3']			= "http://www.irfree.com/gamez/console-games/ps3"
	feeds['psp']			= "http://www.irfree.com/gamez/console-games/psp"
	feeds['wii']			= "http://www.irfree.com/gamez/console-games/wii-console-games"
	feeds['xbox360']		= "http://www.irfree.com/gamez/console-games/xbox360"
	feeds['iphone']			= "http://www.irfree.com/iphoneiopd-apps-games"
	feeds['movies']			= "http://www.irfree.com/moviez"
	feeds['anime']			= "http://www.irfree.com/moviez/anime"
	feeds['hdrip']			= "http://www.irfree.com/moviez/bdripbbrip"
	feeds['cam']			= "http://www.irfree.com/moviez/cam"
	feeds['dvdr']			= "http://www.irfree.com/moviez/dvd-r"
	feeds['dvdrip']			= "http://www.irfree.com/moviez/dvdrip-moviez"
	feeds['dvdscr']			= "http://www.irfree.com/moviez/dvdscr"
	feeds['x264']			= "http://www.irfree.com/moviez/moviesx264"
	feeds['r5']				= "http://www.irfree.com/moviez/r5"
	feeds['ts']				= "http://www.irfree.com/moviez/telesyncts"
	feeds['music']			= "http://www.irfree.com/music"
	feeds['musicvideos']	= "http://www.irfree.com/music/music-videos"
	#feeds['off-topic']		= "http://www.irfree.com/off-topic" news, announcements, no downloads
	feeds['other']			= "http://www.irfree.com/other"
	feeds['retro']			= "http://www.irfree.com/retro"
	feeds['templates']		= "http://www.irfree.com/templates"
	feeds['tutorials']		= "http://www.irfree.com/tutorials"
	feeds['tvshows']		= "http://www.irfree.com/tv-shows"
	feeds['tv_x264']		= "http://www.irfree.com/tv-shows/tv-showx264"
	feeds['boxsets']		= "http://www.irfree.com/tv-shows/tv-showsboxsets"
	feeds['vectors']		= "http://www.irfree.com/vectors"
	feeds['wallpapers']		= "http://www.irfree.com/wallpapers"

	# we fill the list with menuitems, with labels from the appropriate language file
	#	label							,path							, thumbnail						feed
	menuitems = (
		{'label':__language__( 30001 )	,'path':"/root/all"				, 'thumbnail':"all"				, 'feed':"all" },
		# main categories
		{'label':__language__( 30002 )	,'path':"/root/tvshows"			, 'thumbnail':"tvshows"			, 'feed':"" },
		{'label':__language__( 30001 )	,'path':"/root/tvshows/all"		, 'thumbnail':"tvshows"			, 'feed':"tvshows" },
		{'label':__language__( 30020 )	,'path':"/root/tvshows/x264"	, 'thumbnail':"tvshows"			, 'feed':"tv_x264" },
		{'label':__language__( 30003 )	,'path':"/root/tvshows/boxsets"	, 'thumbnail':"tvshows"			, 'feed':"boxsets" },
		{'label':__language__( 30004 )	,'path':"/root/movies"			, 'thumbnail':"movies"			, 'feed':"" },
		{'label':__language__( 30001 )	,'path':"/root/movies/all"		, 'thumbnail':"movies"			, 'feed':"movies" },
		{'label':__language__( 30005 )	,'path':"/root/movies/anime"	, 'thumbnail':"movies"			, 'feed':"anime" },
		{'label':__language__( 30007 )	,'path':"/root/movies/hdrip"	, 'thumbnail':"movies"			, 'feed':"hdrip" },
		{'label':__language__( 30021 )	,'path':"/root/movies/cam"		, 'thumbnail':"movies"			, 'feed':"cam" },
		{'label':__language__( 30006 )	,'path':"/root/movies/dvdr"		, 'thumbnail':"movies"			, 'feed':"dvdr" },
		{'label':__language__( 30022 )	,'path':"/root/movies/dvdrip"	, 'thumbnail':"movies"			, 'feed':"dvdrip" },
		{'label':__language__( 30023 )	,'path':"/root/movies/dvdrscr"	, 'thumbnail':"movies"			, 'feed':"dvdscr" },
		{'label':__language__( 30020 )	,'path':"/root/movies/x246"		, 'thumbnail':"movies"			, 'feed':"x264" },
		{'label':__language__( 30024 )	,'path':"/root/movies/r5"		, 'thumbnail':"movies"			, 'feed':"r5" },
		{'label':__language__( 30025 )	,'path':"/root/movies/ts"		, 'thumbnail':"movies"			, 'feed':"ts" },
		{'label':__language__( 30008 )	,'path':"/root/music"			, 'thumbnail':"music"			, 'feed':"" },
		{'label':__language__( 30001 )	,'path':"/root/music/all"		, 'thumbnail':"music"			, 'feed':"music" },
		{'label':__language__( 30009 )	,'path':"/root/music/mvideos"	, 'thumbnail':"music"			, 'feed':"musicvideos" },
		{'label':__language__( 30010 )	,'path':"/root/games"			, 'thumbnail':"games"			, 'feed':"" },
		{'label':__language__( 30001 )	,'path':"/root/games/all"		, 'thumbnail':"games"			, 'feed':"games" },
		{'label':__language__( 30011 )	,'path':"/root/games/con"		, 'thumbnail':"games"			, 'feed':"" },
		{'label':__language__( 30001 )	,'path':"/root/games/con/all"	, 'thumbnail':"games"			, 'feed':"congames" },
		{'label':__language__( 30012 )	,'path':"/root/games/con/ps2"	, 'thumbnail':"games"			, 'feed':"ps2" },
		{'label':__language__( 30013 )	,'path':"/root/games/con/ps3"	, 'thumbnail':"games"			, 'feed':"ps3" },
		{'label':__language__( 30014 )	,'path':"/root/games/con/psp"	, 'thumbnail':"games"			, 'feed':"psp" },
		{'label':__language__( 30015 )	,'path':"/root/games/con/wii"	, 'thumbnail':"games"			, 'feed':"wii" },
		{'label':__language__( 30016 )	,'path':"/root/games/con/x360"	, 'thumbnail':"games"			, 'feed':"xbox360" },
		{'label':__language__( 30017 )	,'path':"/root/ebooks"			, 'thumbnail':"ebooks"			, 'feed':"" },
		{'label':__language__( 30001 )	,'path':"/root/ebooks/all"		, 'thumbnail':"ebooks"			, 'feed':"ebooks" },
		{'label':__language__( 30018 )	,'path':"/root/ebooks/mags"		, 'thumbnail':"ebooks"			, 'feed':"magazines" },
		{'label':__language__( 30019 )	,'path':"/root/apps"			, 'thumbnail':"apps"			, 'feed':"apps" },
		# miscellaneous
		{'label':__language__( 30031 )	,'path':"/root/misc"			, 'thumbnail':"misc"			, 'feed':"" },
		{'label':__language__( 30032 )	,'path':"/root/misc/iphone"		, 'thumbnail':"iphone"			, 'feed':"iphone" },
		{'label':__language__( 30033 )	,'path':"/root/misc/other"		, 'thumbnail':"misc"			, 'feed':"other" },
		{'label':__language__( 30034 )	,'path':"/root/misc/retro"		, 'thumbnail':"misc"			, 'feed':"retro" },
		{'label':__language__( 30035 )	,'path':"/root/misc/templates"	, 'thumbnail':"misc"			, 'feed':"templates" },
		{'label':__language__( 30036 )	,'path':"/root/misc/tutorials"	, 'thumbnail':"misc"			, 'feed':"tutorials" },
		{'label':__language__( 30037 )	,'path':"/root/misc/vectors"	, 'thumbnail':"misc"			, 'feed':"vectors" },
		{'label':__language__( 30038 )	,'path':"/root/misc/wallpapers"	, 'thumbnail':"misc"			, 'feed':"wallpapers" },
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
