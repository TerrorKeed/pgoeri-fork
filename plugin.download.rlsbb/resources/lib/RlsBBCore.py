import re
from DDLScraperCore import DDLScraperCore

class RlsBBCore(DDLScraperCore):
	
	def __init__(self):
		super(type(self),self).__init__()
		
		self.__title__		= "RlsBB.me"
		self.__url__		= "http://www.rlsbb.com"
		#self.__url__		= "http://www.rlsbb.com/category/tv-shows" # used for filehoster self test
		self.__nextpage__	= '<span id="olderEntries"><a href="'
		
		self.__filehoster__	= {}
		self.__filehoster__["1"] = { "label": "netload",		"alt_label": "",		"url": "http://netload.in",		"alt_url": "http://netfolder.in" }
		self.__filehoster__["2"] = { "label": "turbobit",		"alt_label": "",		"url": "http://turbobit.net",	"alt_url": "" }
		self.__filehoster__["3"] = { "label": "rapidgator",		"alt_label": "",		"url": "http://rapidgator.net",	"alt_url": "" }
		self.__filehoster__["4"] = { "label": "uploaded",		"alt_label": "",		"url": "http://ul.to",			"alt_url": "http://uploaded.to" }
		self.__filehoster__["5"] = { "label": "ryushare",		"alt_label": "",		"url": "http://ryushare.com",	"alt_url": "" }
		#self.__filehoster__[""] = { "label": "",		"alt_label": "",	"url": "" }
		
		
		#===============================================================================
		# SELF TEST:
		#===============================================================================
		# ignore the following urls/labels, when looking for new filehosters
		self.__urls__		= []
		self.__urls__.append("http://www.torrentdownload.ws")
		self.__urls__.append("http://nfo.rlsbb.me")
		self.__urls__.append("http://www.imdb.com")
		self.__urls__.append("http://www.tv.com")
		self.__urls__.append("http://www.tvrage.com")
		self.__urls__.append("http://kickass.to")
		self.__urls__.append("http://nfo.rlsbb.com")
		self.__urls__.append("http://www.youtube.com")
		self.__urls__.append("homepage")
		self.__urls__.append("nfo")
		self.__urls__.append("torrent search")
		self.__urls__.append("imdb")
		self.__urls__.append("tv.com")
		self.__urls__.append("tvrage")
		self.__urls__.append("trailer")

		#self.__urls__.append("")
		 
	#===============================================================================
	#
	# RlsBB specific functions
	
	#===============================================================================
	
	def _trimPosts(self, full_website):
		# get only area with the file-links (ignore samples and comments)
		website = self._executeRE('<div class="postContent">(.+?)<div class="postLinkPages">', full_website)		
		if (website == None):
			# fallback to previous regexp
			website = self._executeRE('<div id="contentArea">(.+?)<div id="pageNavigation">', full_website)
		if (website == None):
			# not possible to extract link section, use the whole website for scraping
			website = full_website
		return website
	
	def _extractPosts(self, link, website):
		# 1: url
		# 2: title
		# 3: img
		
		# STARTPAGE
		posts = re.compile('<div class="entry post">.+?<a href="(.+?)".+?>(.+?)</a>.+?<div class="entry-content">.+?<img.+?src="(.+?)"',re.DOTALL).findall(website)
		if (len(posts) == 0):
			# SUB PAGES
			posts = re.compile('<div class="post">.+?<a href="(.+?)".+?>(.+?)</a>.+?<div class="postContent">.+?<img.+?src="(.+?)"',re.DOTALL).findall(website)
		return posts
	
	
	#===============================================================================
	#
	# Scrape specific filehoster links from a post
	#
	#===============================================================================
	def _scrapeFilehosterLinksByFilehoster( self, website, fh_key ):
		
		fh = self._getFilehoster(fh_key,"0") # "0" means, there is not alternative filehoster defined
		if (fh == None):
			return []
		
		fh_label	= fh["label"]
		fh_url		= fh["url"]
		fh_alt_url	= fh["alt_url"]
		
		if self.__dbg__:
			print self.__plugin__ + " _scrapeFilehosterLinksNow: filehoster: %s" % (fh_label,)
		if self.__dbgv__:
			print self.__plugin__ + " FROM:\n" + website
			
		# get filehoster content based on the beginning of the links
		scraped_links = re.compile('href="(%s.+?)"' % (fh_url, ),re.DOTALL).findall(website)
		
		if ((scraped_links==None or len(scraped_links)==0) and len(fh_alt_url)>0 ):
			scraped_links = re.compile('href="(%s.+?)"' % (fh_alt_url, ),re.DOTALL).findall(website)
			
		if ((scraped_links==None or len(scraped_links)==0)):
			# links could be on another page!
			# get link to sub page
			subpage_link = self._executeRE('href=" *?(http://nfo.rlsbb.com/view/\w+?)">%s' % ( fh_label, ), website, re.IGNORECASE)
			if (subpage_link!=None and len(subpage_link)>0):
				if self.__dbgv__:
					print self.__plugin__ + " SUB PAGE: " + subpage_link
				# fetch the sub page
				( subpage_content, result_str, result) = self._fetchWebsite(subpage_link)
				if (result == 200):
					# now scrape the sub page
					scraped_links = re.compile('<div style=.*?>(%s.*?)</div>' % (fh_url, ),re.DOTALL).findall(subpage_content)
				
		if (scraped_links==None):
			return [ ]
		
		return scraped_links
	
	def _scrapeFilehosterLinksByRelease( self, website):
		links = self._scrapeFilehosterLinksByFilehoster( website, self.__addon__.getSetting( "filehoster" ) )
		if ( len(links) == 0):	
			links = self._scrapeFilehosterLinksByFilehoster( website, self.__addon__.getSetting( "filehoster_alt1" ) )
		if ( len(links) == 0):
			links = self._scrapeFilehosterLinksByFilehoster( website, self.__addon__.getSetting( "filehoster_alt2" ) )
		return links
	
	def _scrapeFilehosterLinksByQuality( self, all_releases, getHD):
		links = []
		
		for release in all_releases:
			isHD = ".720p." in release[0] # is this a HD release?
			if (len(links)==0 and (getHD == isHD)):
				valid_links = re.sub("<del>.+?<\/del>","",release[1]) # remove invalid (nuked) links
				links = self._scrapeFilehosterLinksByRelease(valid_links)
		
		return links
				
	
	def _scrapeFilehosterLinks( self, website):
		preferHD = self.__addon__.getSetting( "prefer_hd" ) == "true"
		
		# tv shows -> get all the releases
		all_releases = re.compile('<p style="text-align: center;"><strong>(.*?)</strong>(.*?)</p>', re.DOTALL).findall(website)
		
		# every other content
		if len(all_releases)==0:
			all_releases = re.compile('<strong>(Download|Links):?</strong>(.*?)<div', re.DOTALL).findall(website)
			
		# fallback (= complete posting)
		if len(all_releases)==0:
			all_releases = [ ("POST",website) ]
		
		if self.__dbgv__:
			print self.__plugin__ + " LINK CONTENT:\n" + str(all_releases)
			
		links = self._scrapeFilehosterLinksByQuality( all_releases, preferHD)
		if len(links)==0:
			links = self._scrapeFilehosterLinksByQuality( all_releases, not preferHD)
		
		# remove duplicates
		links = set(links)
		
		return links
	
	
	#===============================================================================
	#
	# SELF TEST
	#
	#===============================================================================
	def _scrapeFilehoster( self, website):
		# extract links
		urls = re.compile('href="(http://.+?)/').findall(website)
		
		# extract strings
		filehoster = re.compile('<a href=".+?">(.+?)</a>').findall(website)
		
		return set(urls) | set(filehoster)
	
	def _getCategories(self):
		categories = []
		
		( full_website, result_str, result) = self._fetchWebsite(self.__url__)
		
		if (result == 200):
			# extract relevant part
			website = self._executeRE('<li id="categories(.+?)<li id="archives', full_website)
			
			categories = re.compile('<a href="(.+?)"',re.DOTALL).findall(website)
			
		return categories
	