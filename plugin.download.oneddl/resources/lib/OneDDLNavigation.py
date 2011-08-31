import sys
from OneDDLCore import OneDDLCore
from DDLScraperNavigation import DDLScraperNavigation
	
class OneDDLNavigation(DDLScraperNavigation):
	__language__	= sys.modules[ "__main__" ].__language__
	
	#===============================================================================
	# dictonary 'feeds' stores the links for all categories
	#===============================================================================
	feeds = {};
	feeds['all']			= "http://www.oneddl.com"
	feeds['1click']			= "http://www.oneddl.com/category/1-click" # NOT_USED
	feeds['apps']			= "http://www.oneddl.com/category/apps"
	feeds['mac_apps']		= "http://www.oneddl.com/category/apps/mac-apps"
	feeds['win_apps']		= "http://www.oneddl.com/category/apps/windows"
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
	feeds['sitenews']		= "http://www.oneddl.com/category/site-news" # NOT_USED: news, announcements, no downloads
	feeds['staffpicks']		= "http://www.oneddl.com/category/staff-picks"
	feeds['trailers']		= "http://www.oneddl.com/category/trailers"
	feeds['tvshows']		= "http://www.oneddl.com/category/tv-shows"
	feeds['tv720p']			= "http://www.oneddl.com/category/tv-shows/hd-720p"
	feeds['tvppv']			= "http://www.oneddl.com/category/tv-shows/ppv"
	feeds['tvsport']		= "http://www.oneddl.com/category/tv-shows/sport"
	feeds['tvdvdrip']		= "http://www.oneddl.com/category/tv-shows/tv-dvdrip"
	feeds['uncat']			= "http://www.oneddl.com/category/uncategorized"
	feeds['vodo']			= "http://www.oneddl.com/category/vodo"
	feeds['search']			= "http://www.oneddl.com/?s="

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
		{'label':__language__( 30055 )	,'path':"/root/apps"			, 'thumbnail':"apps"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/apps/all"		, 'thumbnail':"apps"			, 'feed':"apps" },
		{'label':__language__( 30056 )	,'path':"/root/apps/mac"		, 'thumbnail':"apps"			, 'feed':"mac_apps" },
		{'label':__language__( 30057 )	,'path':"/root/apps/win"		, 'thumbnail':"apps"			, 'feed':"win_apps" },
		# miscellaneous
		{'label':__language__( 30060 )	,'path':"/root/misc"			, 'thumbnail':"misc"			, 'feed':"" },
		{'label':__language__( 30061 )	,'path':"/root/misc/iphone"		, 'thumbnail':"iphone"			, 'feed':"iphone" },
		{'label':__language__( 30062 )	,'path':"/root/misc/staffpicks"	, 'thumbnail':"misc"			, 'feed':"staffpicks" },
		{'label':__language__( 30063 )	,'path':"/root/misc/trailers"	, 'thumbnail':"misc"			, 'feed':"trailers" },
		{'label':__language__( 30064 )	,'path':"/root/misc/uncat"		, 'thumbnail':"misc"			, 'feed':"uncat" },
		{'label':__language__( 30065 )	,'path':"/root/misc/vodo"		, 'thumbnail':"misc"			, 'feed':"vodo" },
		# search
		{'label':__language__( 30080 )	,'path':"/root/search"			, 'thumbnail':"search"			, 'feed':"search" },
	)

	 
	def __init__(self):
		self._core = OneDDLCore()