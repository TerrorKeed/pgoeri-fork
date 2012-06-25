import re
from DDLScraperCore import DDLScraperCore

class OneDDLCore(DDLScraperCore):
	
	def __init__(self):
		super(type(self),self).__init__()
		
		self.__title__		= "OneDDL.com"
		self.__url__		= "http://www.oneddl.eu"
		#self.__url__		= "http://www.oneddl.eu/category/tv-shows/" # used for filehoster self test
		self.__nextpage__	= "class='page larger'"
		
		self.__filehoster__	= {}
		self.__filehoster__["0"] = { "label": "rapidshare",	"alt_label": "",		"url": "http://rapidshare.com" }
		self.__filehoster__["4"] = { "label": "filefactory",	"alt_label": "" }
		self.__filehoster__["9"] = { "label": "turbobit",		"alt_label": "",		"url": "http://turbobit.net" }
		self.__filehoster__["10"] = { "label": "uploaded",		"alt_label": "ul.to",	"url": "http://ul.to" }
		self.__filehoster__["11"] = { "label": "netload",		"alt_label": "" }
		self.__filehoster__["12"] = { "label": "depositfiles",	"alt_label": "" }
		self.__filehoster__["13"] = { "label": "filepost",		"alt_label": "" }
		self.__filehoster__["14"] = { "label": "bitshare",		"alt_label": "" }
		#self.__filehoster__[""] = { "label": "",		"alt_label": "",	"url": "" }
		
		# ignore the following urls, when looking for new filehosters
		self.__urls__		= []
		self.__urls__.append("http://linksafe.me")
		 
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

	def _scrapeFilehosterLinksNow( self, website, getHD, get1Click, fh_key ):
		
		fh = self._getFilehoster(fh_key)
		if (fh == None):
			return []
		
		fh_label = fh["label"]
		fh_alt_label = fh["alt_label"]
		
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
		links = self._scrapeFilehosterLinksNow( website, getHD, get1Click, self.__addon__.getSetting( "filehoster" ) )
		if ( len(links) == 0):
			alt_filehoster = self.__addon__.getSetting( "alt_filehoster1" )
			if ( alt_filehoster != "0"):
				links = self._scrapeFilehosterLinksNow( website, getHD, get1Click, str(int(alt_filehoster)-1) )
		if ( len(links) == 0):
			alt_filehoster = self.__addon__.getSetting( "alt_filehoster2" )
			if ( alt_filehoster != "0"):
				links = self._scrapeFilehosterLinksNow( website, getHD, get1Click, str(int(alt_filehoster)-1) )
		if ( len(links) == 0):
			alt_filehoster = self.__addon__.getSetting( "alt_filehoster3" )
			if ( alt_filehoster != "0"):
				links = self._scrapeFilehosterLinksNow( website, getHD, get1Click, str(int(alt_filehoster)-1) )
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
	