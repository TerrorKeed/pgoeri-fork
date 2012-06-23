import sys, os, xbmc, xbmcaddon

# plugin constants
__version__			= "0.1.0"
__plugin__			= "RlsBB.me-" + __version__
__author__			= "pgoeri"
__url__				= "http://pgoeri-xbmc-plugins.googlecode.com"
__svn_url__			= "http://pgoeri-xbmc-plugins.googlecode.com/svn/trunk/plugin.download.rlsbb/"
__XBMC_Revision__	= "11.0" # Eden
__date__			= "23-06-2012"

__addon__			= xbmcaddon.Addon(id='plugin.download.rlsbb')
__language__		= __addon__.getLocalizedString
__dbg__				= __addon__.getSetting( "debug" ) == "true"
__JDaddonID__		= "plugin.program.jdownloader"

sys.path.append( os.path.join( __addon__.getAddonInfo('path'), "resources", "lib" ) )

if (__name__ == "__main__" ):
	if __dbg__:
		print __plugin__ + " ARGV: " + repr(sys.argv)
	else:
		print __plugin__
	
	import RlsBBNavigation as navigation
	
	navigator = navigation.RlsBBNavigation().navigate(sys.argv[2])