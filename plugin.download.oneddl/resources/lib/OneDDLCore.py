import re
from DDLScraperCore import DDLScraperCore

class OneDDLCore(DDLScraperCore):
	
	
	def __init__(self):
		self.__title__		= "OneDDL.com"
		self.__url__		= "http://www.oneddl.com"
		#self.__url__		= "http://www.oneddl.com/category/tv-shows/"
		self.__nextpage__	= "class='page larger'"
		
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
		if (filehoster == 0):
			fh_label = "rapidshare"
		elif (filehoster == 1):
			fh_label = "hotfile"		# deprecated
		elif (filehoster == 2):
			fh_label = "fileserve"
		elif (filehoster == 3):
			fh_label = "filesonic"		# dead
		elif (filehoster == 4):
			fh_label = "filefactory"	# deprecated
		elif (filehoster == 5):
			fh_label = "megaupload"		# dead
		elif (filehoster == 6):
			fh_label = "multiupload"
		elif (filehoster == 7):
			fh_label = "wupload" 
		elif (filehoster == 8):
			fh_label = "oron"
		elif (filehoster == 9):
			fh_label = "turbobit"
		elif (filehoster == 10):
			fh_label = "ul.to"
		elif (filehoster == 11):
			fh_label = "netload"
		elif (filehoster == 12):
			fh_label = "depositfiles"
		elif (filehoster == 13):
			fh_label = "filepost"
		else:
			return [ ]
		
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
		website = self._executeRE("<p><strong>%s(.*?)</p>" % (fh_label, ), website, re.IGNORECASE)
		if (website==None):
			return [ ]
		
		scraped_links = re.compile('href="(.+?)"',re.DOTALL).findall(website);
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
	