import re
from DDLScraperCore import DDLScraperCore

class OneDDLCore(DDLScraperCore):
	
	def __init__(self):
		self.__title__		= "OneDDL.com"
		self.__url__		= "http://www.oneddl.eu"
		#self.__url__		= "http://www.oneddl.eu/category/tv-shows/" # used for self test
		self.__nextpage__	= "class='page larger'"
		
		self.__filehoster__	= []
		self.__filehoster__.insert(0,	{ "label": "rapidshare",	"alt_label": "" } )
		self.__filehoster__.insert(1,	{ "label": "hotfile",		"alt_label": "" } )			# deprecated
		self.__filehoster__.insert(2,	{ "label": "fileserve",		"alt_label": "" } )
		self.__filehoster__.insert(3,	{ "label": "filesonic",		"alt_label": "" } )			# dead
		self.__filehoster__.insert(4,	{ "label": "filefactory",	"alt_label": "" } )		# deprecated
		self.__filehoster__.insert(5,	{ "label": "megaupload",	"alt_label": "" } )			# dead
		self.__filehoster__.insert(6,	{ "label": "multiupload",	"alt_label": "" } )
		self.__filehoster__.insert(7,	{ "label": "wupload",		"alt_label": "" } )
		self.__filehoster__.insert(8,	{ "label": "oron",			"alt_label": "" } )
		self.__filehoster__.insert(9,	{ "label": "turbobit",		"alt_label": "" } )
		self.__filehoster__.insert(10,	{ "label": "uploaded",		"alt_label": "ul.to" } )
		self.__filehoster__.insert(11,	{ "label": "netload",		"alt_label": "" } )
		self.__filehoster__.insert(12,	{ "label": "depositfiles",	"alt_label": "" } )
		self.__filehoster__.insert(13,	{ "label": "filepost",		"alt_label": "" } )
		self.__filehoster__.insert(14,	{ "label": "bitshare",		"alt_label": "" } )
		 
	#===============================================================================
	#
	# OneDDL specific functions
	
	#===============================================================================
	
	def _trimPosts(self, full_website):
		# get only area with the file-links (ignore samples and comments)
		website = self._executeRE('id="more-(.+?)class="postmeta"', full_website)
		if (website == None):
			website = self._executeRE('id="more-(.+?)<!-- .entry-content -->', full_website)
		if (website == None):
			# not possible to extract link section, use the whole website for scraping
			website = full_website
		return website
	
	def _extractPosts(self, link, website):
		# 1: url
		# 2: title
		# 3: img
		posts = re.compile('class="posttitle">.+?<a href="(.+?)".+?>(.+?)</a>.+?</div>.+?<img.+?src="(.+?)"',re.DOTALL).findall(website)
		if (len(posts) == 0):
			posts = re.compile('class="entry-title">.*?<a href="(.+?)".+?>(.+?)</a>.+?class="entry-content".+?<img.+?src="(.+?)"',re.DOTALL).findall(website)
		return posts

	def _scrapeFilehosterLinksNow( self, website, getHD, get1Click, filehoster ):
		
		fh_label = self.__filehoster__[filehoster]["label"]
		fh_alt_label = self.__filehoster__[filehoster]["alt_label"]
		
		if self.__dbg__:
			print self.__plugin__ + " _scrapeFilehosterLinksNow: hd: %s - 1click: %s - filehoster: %s" % (getHD, get1Click, fh_label)
			
		if (getHD==True):
			# assumption sd and hd version are always seperated by an hsep and sd is always above hd
			website = self._executeRE("<hr />(.*)", website)
		else:
			tmp = self._executeRE("(.*)<hr />", website)
			if (tmp!=None):
				website = tmp
			
		if (website==None):
			return [ ]
		
		if (get1Click==True):
			website = self._executeRE("<oneclickimg(.*)", website)
		else:
			website = self._executeRE("<downloadimg(.*)", website)
		if (website==None):
			return [ ]
		
		# get filehoster content
		all_links = self._executeRE("<p><strong>%s(.*?)</p>" % (fh_label, ), website, re.IGNORECASE)
		if (all_links==None and len(fh_alt_label)>0 ):
			all_links = self._executeRE("<p><strong>%s(.*?)</p>" % (fh_alt_label, ), website, re.IGNORECASE)
		if (all_links==None):
			return [ ]
		
		scraped_links = re.compile('href="(.+?)"',re.DOTALL).findall(all_links);
		return scraped_links
	
	def _scrapeFilehosterLinksByLinkType( self, website, getHD, get1Click):
		links = self._scrapeFilehosterLinksNow( website, getHD, get1Click, int(self.__addon__.getSetting( "filehoster" )) )
		if ( len(links) == 0):
			alt_filehoster = int(self.__addon__.getSetting( "alt_filehoster1" ))
			if ( alt_filehoster != 0):
				links = self._scrapeFilehosterLinksNow( website, getHD, get1Click, (alt_filehoster-1) )
		if ( len(links) == 0):
			alt_filehoster = int(self.__addon__.getSetting( "alt_filehoster2" ))
			if ( alt_filehoster != 0):
				links = self._scrapeFilehosterLinksNow( website, getHD, get1Click, (alt_filehoster-1) )
		if ( len(links) == 0):
			alt_filehoster = int(self.__addon__.getSetting( "alt_filehoster3" ))
			if ( alt_filehoster != 0):
				links = self._scrapeFilehosterLinksNow( website, getHD, get1Click, (alt_filehoster-1) )
		return links
	
	def _scrapeFilehosterLinksByQuality( self, website, getHD):
		prefer1Click = self.__addon__.getSetting( "prefer_1click" ) == "true"
		
		links = self._scrapeFilehosterLinksByLinkType( website, getHD, prefer1Click)
		if (len(links)==0):
			links = self._scrapeFilehosterLinksByLinkType( website, getHD, not prefer1Click)
		return links
				
	
	def _scrapeFilehosterLinks( self, website):
		preferHD = self.__addon__.getSetting( "prefer_hd" ) == "true"
		
		links = self._scrapeFilehosterLinksByQuality( website, preferHD)
		if len(links)==0:
			links = self._scrapeFilehosterLinksByQuality( website, not preferHD)
		
		# remove duplicates
		links = set(links)
		
		return links
	
	def _scrapeFilehoster( self, website):
		# extract links
		urls = re.compile('href="(http://.+?)/').findall(website);
		
		# extract strings
		filehoster = re.compile('<p><strong>(.+?)[ <(]').findall(website);
		
		return set(urls) | set(filehoster)
	
	def _getCategories(self):
		categories = []
		
		( full_website, result_str, result) = self._fetchWebsite(self.__url__)
		
		if (result == 200):
			# extract relevant part
			website = self._executeRE('<div class="menu-categories-container"(.+?)</div>', full_website)
			
			categories = re.compile('<a href="(.+?)"',re.DOTALL).findall(website)
			
		return categories
	