import sys, os, xbmc, xbmcaddon

# plugin constants
__version__			= "0.2.3"
__plugin__			= "IRFree.com-" + __version__
__addonID__			= "plugin.download.irfree"
__author__			= "pgoeri"
__url__				= "http://pgoeri-xbmc-plugins.googlecode.com"
__svn_url__			= "http://pgoeri-xbmc-plugins.googlecode.com/svn/trunk/plugin.download.irfree/"
__XBMC_Revision__	= "11.0" # Eden
__date__			= "25-06-2012"

__addon__			= xbmcaddon.Addon(id=__addonID__)
__language__		= __addon__.getLocalizedString
__dbg__				= __addon__.getSetting( "debug" ) == "true"


if (__name__ == "__main__" ):
	sys.path.append( os.path.join( __addon__.getAddonInfo('path'), "resources", "lib" ) )
	
	import IRFreeNavigation as navigation
	
	navigation.IRFreeNavigation().navigate()