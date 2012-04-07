import sys, os, xbmc, xbmcaddon

# plugin constants
__version__			= "0.2.3"
__plugin__			= "OneDDL.com-" + __version__
__author__			= "pgoeri"
__url__				= "http://pgoeri-xbmc-plugins.googlecode.com"
__svn_url__			= "http://pgoeri-xbmc-plugins.googlecode.com/svn/trunk/plugin.download.oneddl/"
__XBMC_Revision__	= "ec33f1f05a364d6dc69504134158cab31b970f29" # 03-04-2012
__date__			= "06-04-2012"

__addon__			= xbmcaddon.Addon(id='plugin.download.oneddl')
__language__		= __addon__.getLocalizedString
__dbg__				= __addon__.getSetting( "debug" ) == "true"
__JDaddonID__		= "plugin.program.jdownloader"

sys.path.append( os.path.join( __addon__.getAddonInfo('path'), "resources", "lib" ) )

if (__name__ == "__main__" ):
	if __dbg__:
		print __plugin__ + " ARGV: " + repr(sys.argv)
	else:
		print __plugin__
	
	import OneDDLNavigation as navigation
	from PluginException import PluginException
	navigator = navigation.OneDDLNavigation()
	
	try:
		if (not sys.argv[2]):
			navigator.listMenu()
		else:
			params = navigator.getParameters(sys.argv[2])
			get = params.get
			if (get("action")):
				navigator.executeAction(params)
			elif (get("path")):
				navigator.listMenu(params)
	except PluginException, e:
		navigator.showError(e.message)
