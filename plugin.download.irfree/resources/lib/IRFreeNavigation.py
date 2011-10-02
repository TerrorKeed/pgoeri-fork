import sys
from IRFreeCore import IRFreeCore
from DDLScraperNavigation import DDLScraperNavigation


class IRFreeNavigation(DDLScraperNavigation):
	__language__	= sys.modules[ "__main__" ].__language__
	
	#===============================================================================
	# dictonary 'feeds' stores the links for all categories
	#===============================================================================
	feeds = {};
	feeds['all']			= "http://www.irfree.com"
	feeds['apps']			= "http://www.irfree.com/applications"
	feeds['android']		= "http://www.irfree.com/applications/android"
	feeds['iphone']			= "http://www.irfree.com/applications/iphone"
	feeds['mac']			= "http://www.irfree.com/applications/mac"
	feeds['windows']		= "http://www.irfree.com/applications/windows"
	feeds['ebooks']			= "http://www.irfree.com/ebooks"
	feeds['magazines']		= "http://www.irfree.com/ebooks/magazines"
	feeds['games']			= "http://www.irfree.com/games"
	feeds['ps3']			= "http://www.irfree.com/games/ps3"
	feeds['psp']			= "http://www.irfree.com/games/psp"
	feeds['wii']			= "http://www.irfree.com/games/wii"
	feeds['xbox360']		= "http://www.irfree.com/games/xbox360"
	feeds['movies']			= "http://www.irfree.com/movies"
	feeds['anime']			= "http://www.irfree.com/movies/anime"
	feeds['hdrip']			= "http://www.irfree.com/movies/bdrip"
	feeds['cam']			= "http://www.irfree.com/movies/cam"
	feeds['dvdr']			= "http://www.irfree.com/movies/dvd-r"
	feeds['dvdrip']			= "http://www.irfree.com/movies/dvdrip"
	feeds['dvdscr']			= "http://www.irfree.com/movies/dvdscr"
	feeds['x264']			= "http://www.irfree.com/movies/moviesx264"
	feeds['r5']				= "http://www.irfree.com/movies/r5"
	feeds['ts']				= "http://www.irfree.com/movies/telesyncts"
	feeds['music']			= "http://www.irfree.com/music"
	feeds['musicvideos']	= "http://www.irfree.com/music/mvid"
	feeds['tutorials']		= "http://www.irfree.com/tutorials"
	feeds['tvshows']		= "http://www.irfree.com/tv-shows"
	feeds['tv_x264']		= "http://www.irfree.com/tv-shows/tv-shows264"
	feeds['boxsets']		= "http://www.irfree.com/tv-shows/tv-showsboxsets"
	feeds['search']			= "http://www.irfree.com/?s="

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
		{'label':__language__( 30013 )	,'path':"/root/games/ps3"		, 'thumbnail':"games"			, 'feed':"ps3" },
		{'label':__language__( 30014 )	,'path':"/root/games/psp"		, 'thumbnail':"games"			, 'feed':"psp" },
		{'label':__language__( 30015 )	,'path':"/root/games/wii"		, 'thumbnail':"games"			, 'feed':"wii" },
		{'label':__language__( 30016 )	,'path':"/root/games/x360"		, 'thumbnail':"games"			, 'feed':"xbox360" },
		{'label':__language__( 30017 )	,'path':"/root/ebooks"			, 'thumbnail':"ebooks"			, 'feed':"" },
		{'label':__language__( 30001 )	,'path':"/root/ebooks/all"		, 'thumbnail':"ebooks"			, 'feed':"ebooks" },
		{'label':__language__( 30018 )	,'path':"/root/ebooks/mags"		, 'thumbnail':"ebooks"			, 'feed':"magazines" },
		{'label':__language__( 30019 )	,'path':"/root/apps"			, 'thumbnail':"apps"			, 'feed':"" },
		{'label':__language__( 30001 )	,'path':"/root/apps/all"		, 'thumbnail':"apps"			, 'feed':"apps" },
		{'label':__language__( 30042 )	,'path':"/root/apps/android"	, 'thumbnail':"apps"			, 'feed':"android" },
		{'label':__language__( 30032 )	,'path':"/root/apps/iphone"		, 'thumbnail':"iphone"			, 'feed':"iphone" },
		{'label':__language__( 30044 )	,'path':"/root/apps/mac"		, 'thumbnail':"apps"			, 'feed':"mac" },
		{'label':__language__( 30043 )	,'path':"/root/apps/windows"	, 'thumbnail':"apps"			, 'feed':"windows" },
		# miscellaneous
		{'label':__language__( 30031 )	,'path':"/root/misc"			, 'thumbnail':"misc"			, 'feed':"" },
		{'label':__language__( 30036 )	,'path':"/root/misc/tutorials"	, 'thumbnail':"misc"			, 'feed':"tutorials" },
		# search
		#{'label':__language__( 30080 )	,'path':"/root/search"			, 'thumbnail':"search"			, 'feed':"search" }, # not possible anymore with new design
	)
	 
	def __init__(self):
		self._core = IRFreeCore()
