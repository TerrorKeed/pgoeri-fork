import sys
from IRFreeCore import IRFreeCore
from DDLScraperNavigation import DDLScraperNavigation


class IRFreeNavigation(DDLScraperNavigation):
	__language__	= sys.modules[ "__main__" ].__language__
	
	#===============================================================================
	# dictonary 'feeds' stores the links for all categories
	#===============================================================================
	feeds = {};
	feeds['all']			= "http://irfree.com"
	feeds['apps']			= "http://irfree.com/category/applications"
	feeds['ebooks']			= "http://irfree.com/category/e-books"
	feeds['magazines']		= "http://irfree.com/category/e-books/magazines"
	feeds['games']			= "http://irfree.com/category/gamez"
	feeds['congames']		= "http://irfree.com/category/gamez/console-games"
	feeds['ps2']			= "http://irfree.com/category/gamez/console-games/ps2"
	feeds['ps3']			= "http://irfree.com/category/gamez/console-games/ps3"
	feeds['psp']			= "http://irfree.com/category/gamez/console-games/psp"
	feeds['wii']			= "http://irfree.com/category/gamez/console-games/wii-console-games"
	feeds['xbox360']		= "http://irfree.com/category/gamez/console-games/xbox360"
	feeds['iphone']			= "http://irfree.com/category/iphoneiopd-apps-games"
	feeds['movies']			= "http://irfree.com/category/moviez"
	feeds['anime']			= "http://irfree.com/category/moviez/anime"
	feeds['hdrip']			= "http://irfree.com/category/moviez/bdripbbrip"
	feeds['cam']			= "http://irfree.com/category/moviez/cam"
	feeds['dvdr']			= "http://irfree.com/category/moviez/dvd-r"
	feeds['dvdrip']			= "http://irfree.com/category/moviez/dvdrip-moviez"
	feeds['dvdscr']			= "http://irfree.com/category/moviez/dvdscr"
	feeds['x264']			= "http://irfree.com/category/moviez/moviesx264"
	feeds['r5']				= "http://irfree.com/category/moviez/r5"
	feeds['ts']				= "http://irfree.com/category/moviez/telesyncts"
	feeds['music']			= "http://irfree.com/category/music"
	feeds['musicvideos']	= "http://irfree.com/category/music/music-videos"
	#feeds['off-topic']		= "http://irfree.com/category/off-topic" news, announcements, no downloads
	feeds['other']			= "http://irfree.com/category/other"
	feeds['retro']			= "http://irfree.com/category/retro"
	feeds['templates']		= "http://irfree.com/category/templates"
	feeds['tutorials']		= "http://irfree.com/category/tutorials"
	feeds['tvshows']		= "http://irfree.com/category/tv-shows"
	feeds['tv_x264']		= "http://irfree.com/category/tv-shows/tv-showx264"
	feeds['boxsets']		= "http://irfree.com/category/tv-shows/tv-showsboxsets"
	feeds['vectors']		= "http://irfree.com/category/vectors"
	feeds['wallpapers']		= "http://irfree.com/category/wallpapers"
	feeds['search']			= "http://irfree.com/?s="

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
		# search
		{'label':__language__( 30080 )	,'path':"/root/search"			, 'thumbnail':"search"			, 'feed':"search" },
	)
	 
	def __init__(self):
		self._core = IRFreeCore()
