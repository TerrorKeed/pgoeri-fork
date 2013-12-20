import sys
from RlsBBCore import RlsBBCore
from DDLScraperNavigation import DDLScraperNavigation
	
class RlsBBNavigation(DDLScraperNavigation):
	__language__	= sys.modules[ "__main__" ].__language__
	
	#===============================================================================
	# dictionary 'feeds' stores the links for all categories
	#===============================================================================
	feeds = {};
	feeds['all']			= "http://www.rlsbb.com"
	feeds['apps']			= "http://www.rlsbb.com/category/applications"
	feeds['apps_android']	= "http://www.rlsbb.com/category/applications/android"
	feeds['apps_ios']		= "http://www.rlsbb.com/category/applications/ios"
	feeds['apps_mac']		= "http://www.rlsbb.com/category/applications/mac"
	feeds['apps_windows']	= "http://www.rlsbb.com/category/applications/windows"
	feeds['ebooks']			= "http://www.rlsbb.com/category/ebooks-magazines"
	feeds['games']			= "http://www.rlsbb.com/category/games"
	feeds['games_android']	= "http://www.rlsbb.com/category/games/android-games"
	feeds['games_ios']		= "http://www.rlsbb.com/category/games/ios-games"
	feeds['games_mac']		= "http://www.rlsbb.com/category/games/mac-games"
	feeds['games_pc']		= "http://www.rlsbb.com/category/games/pc"
	feeds['games_ps3']		= "http://www.rlsbb.com/category/games/ps3"
	feeds['games_psp']		= "http://www.rlsbb.com/category/games/psp"
	feeds['games_wii']		= "http://www.rlsbb.com/category/games/wii"
	feeds['games_xbox360']	= "http://www.rlsbb.com/category/games/xbox360"
	feeds['movies']			= "http://www.rlsbb.com/category/movies"
	feeds['movies_1080p']	= "http://www.rlsbb.com/category/movies/1080p-movie"
	feeds['movies_720p']	= "http://www.rlsbb.com/category/movies/720p-movie"
	feeds['movies_bdrip']	= "http://www.rlsbb.com/category/movies/bdrip-movies"
	feeds['movies_cam']		= "http://www.rlsbb.com/category/movies/cam-movies"
	feeds['movies_dvdr']	= "http://www.rlsbb.com/category/movies/dvd-r"
	feeds['movies_dvdrip']	= "http://www.rlsbb.com/category/movies/dvdrip-movies"
	feeds['movies_dvdscr']	= "http://www.rlsbb.com/category/movies/dvdscr"
	feeds['movies_hdtv']	= "http://www.rlsbb.com/category/movies/hdtv"
	feeds['movies_old']		= "http://www.rlsbb.com/category/movies/old-movie"
	feeds['movies_ppvrip']	= "http://www.rlsbb.com/category/movies/ppvrip"
	feeds['movies_r5']		= "http://www.rlsbb.com/category/movies/r5-movies"
	feeds['movies_scr']		= "http://www.rlsbb.com/category/movies/scr"
	feeds['movies_ts']		= "http://www.rlsbb.com/category/movies/telesync"
	feeds['movies_tvrip']	= "http://www.rlsbb.com/category/movies/tvrip"
	feeds['movies_webrip']	= "http://www.rlsbb.com/category/movies/webrip"
	feeds['music']			= "http://www.rlsbb.com/category/music"
	feeds['music_album']	= "http://www.rlsbb.com/category/music/album"
	feeds['music_itunes']	= "http://www.rlsbb.com/category/music/itunes-music"
	feeds['music_video']	= "http://www.rlsbb.com/category/music/music-video"
	feeds['music_singles']	= "http://www.rlsbb.com/category/music/singleseps"
	feeds['offtopic']		= "http://www.rlsbb.com/category/offtopic"
	feeds['tutorials']		= "http://www.rlsbb.com/category/tutorials"
	feeds['tvshows']		= "http://www.rlsbb.com/category/tv-shows"
	feeds['tvshows_packs']	= "http://www.rlsbb.com/category/tv-shows/tv-packs"
	feeds['uncategorized']	= "http://www.rlsbb.com/category/uncategorized"
	feeds['search']			= "http://www.rlsbb.com/?s="

	# tuple with all menu items
	#	label							,path							, thumbnail						feed
	menuitems = (
		{'label':__language__( 30000 )	,'path':"/root/all"				, 'thumbnail':"all"				, 'feed':"all" },
		# tvshows
		{'label':__language__( 30001 )	,'path':"/root/tvshows"			, 'thumbnail':"tvshows"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/tvshows/all"		, 'thumbnail':"tvshows"			, 'feed':"tvshows" },
		{'label':__language__( 30002 )	,'path':"/root/tvshows/packs"	, 'thumbnail':"tvshows"			, 'feed':"tvshows_packs" },
		# movies
		{'label':__language__( 30010 )	,'path':"/root/movies"			, 'thumbnail':"movies"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/movies/all"		, 'thumbnail':"movies"			, 'feed':"movies" },
		{'label':__language__( 30011)	,'path':"/root/movies/1080p"	, 'thumbnail':"movies"			, 'feed':"movies_1080p" },
		{'label':__language__( 30012)	,'path':"/root/movies/720p"		, 'thumbnail':"movies"			, 'feed':"movies_720p" },
		{'label':__language__( 30013)	,'path':"/root/movies/bdrip"	, 'thumbnail':"movies"			, 'feed':"movies_bdrip" },
		{'label':__language__( 30014)	,'path':"/root/movies/cam"		, 'thumbnail':"movies"			, 'feed':"movies_cam" },
		{'label':__language__( 30015)	,'path':"/root/movies/dvdr"		, 'thumbnail':"movies"			, 'feed':"movies_dvdr" },
		{'label':__language__( 30016)	,'path':"/root/movies/dvdrip"	, 'thumbnail':"movies"			, 'feed':"movies_dvdrip" },
		{'label':__language__( 30017)	,'path':"/root/movies/dvdscr"	, 'thumbnail':"movies"			, 'feed':"movies_dvdscr" },
		{'label':__language__( 30018)	,'path':"/root/movies/hdtv"		, 'thumbnail':"movies"			, 'feed':"movies_hdtv" },
		{'label':__language__( 30019)	,'path':"/root/movies/old"		, 'thumbnail':"movies"			, 'feed':"movies_old" },
		{'label':__language__( 30020)	,'path':"/root/movies/ppvrip"	, 'thumbnail':"movies"			, 'feed':"movies_ppvrip" },
		{'label':__language__( 30021)	,'path':"/root/movies/r5"		, 'thumbnail':"movies"			, 'feed':"movies_r5" },
		{'label':__language__( 30022)	,'path':"/root/movies/scr"		, 'thumbnail':"movies"			, 'feed':"movies_scr" },
		{'label':__language__( 30023)	,'path':"/root/movies/ts"		, 'thumbnail':"movies"			, 'feed':"movies_ts" },
		{'label':__language__( 30024)	,'path':"/root/movies/tvrip"	, 'thumbnail':"movies"			, 'feed':"movies_tvrip" },
		{'label':__language__( 30025)	,'path':"/root/movies/webrip"	, 'thumbnail':"movies"			, 'feed':"movies_webrip" },
		# music
		{'label':__language__( 30030 )	,'path':"/root/music"			, 'thumbnail':"music"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/music/all"		, 'thumbnail':"music"			, 'feed':"music" },
		{'label':__language__( 30031 )	,'path':"/root/music/flac"		, 'thumbnail':"music"			, 'feed':"music_album" },
		{'label':__language__( 30032 )	,'path':"/root/music/mp3"		, 'thumbnail':"music"			, 'feed':"music_itunes" },
		{'label':__language__( 30033 )	,'path':"/root/music/mvid"		, 'thumbnail':"music"			, 'feed':"music_video" },
		{'label':__language__( 30034 )	,'path':"/root/music/mvid"		, 'thumbnail':"music"			, 'feed':"music_singles" },
		# games
		{'label':__language__( 30040 )	,'path':"/root/games"			, 'thumbnail':"games"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/games/all"		, 'thumbnail':"games"			, 'feed':"games" },
		{'label':__language__( 30041 )	,'path':"/root/games/android"	, 'thumbnail':"games"			, 'feed':"games_android" },
		{'label':__language__( 30042 )	,'path':"/root/games/ios"		, 'thumbnail':"iphone"			, 'feed':"games_ios" },
		{'label':__language__( 30043 )	,'path':"/root/games/mac"		, 'thumbnail':"games"			, 'feed':"games_mac" },
		{'label':__language__( 30044 )	,'path':"/root/games/pc"		, 'thumbnail':"games"			, 'feed':"games_pc" },
		{'label':__language__( 30045 )	,'path':"/root/games/ps3"		, 'thumbnail':"games"			, 'feed':"games_ps3" },
		{'label':__language__( 30046 )	,'path':"/root/games/psp"		, 'thumbnail':"games"			, 'feed':"games_psp" },
		{'label':__language__( 30047 )	,'path':"/root/games/wii"		, 'thumbnail':"games"			, 'feed':"games_wii" },
		{'label':__language__( 30048 )	,'path':"/root/games/x360"		, 'thumbnail':"games"			, 'feed':"games_xbox360" },
		# ebooks
		{'label':__language__( 30050 )	,'path':"/root/ebooks"			, 'thumbnail':"ebooks"			, 'feed':"ebooks" },
		# apps
		{'label':__language__( 30060 )	,'path':"/root/apps"			, 'thumbnail':"apps"			, 'feed':"" },
		{'label':__language__( 30000 )	,'path':"/root/apps/all"		, 'thumbnail':"apps"			, 'feed':"apps" },
		{'label':__language__( 30061 )	,'path':"/root/apps/android"	, 'thumbnail':"apps"			, 'feed':"apps_android" },
		{'label':__language__( 30062 )	,'path':"/root/apps/ios"		, 'thumbnail':"iphone"			, 'feed':"apps_ios" },
		{'label':__language__( 30063 )	,'path':"/root/apps/mac"		, 'thumbnail':"apps"			, 'feed':"apps_mac" },
		{'label':__language__( 30064 )	,'path':"/root/apps/win"		, 'thumbnail':"apps"			, 'feed':"apps_windows" },
		# miscellaneous
		{'label':__language__( 30070 )	,'path':"/root/misc"			, 'thumbnail':"misc"			, 'feed':"" },
		{'label':__language__( 30071 )	,'path':"/root/misc/offtopic"	, 'thumbnail':"misc"			, 'feed':"offtopic" },
		{'label':__language__( 30072 )	,'path':"/root/misc/tutorials"	, 'thumbnail':"misc"			, 'feed':"tutorials" },
		{'label':__language__( 30073 )	,'path':"/root/misc/uncategorized"	, 'thumbnail':"misc"		, 'feed':"uncategorized" },
		# search
		{'label':__language__( 30080 )	,'path':"/root/search"			, 'thumbnail':"search"			, 'feed':"search" },
	)

	 
	def __init__(self):
		self._core = RlsBBCore()