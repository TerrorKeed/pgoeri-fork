import re
from DDLScraperCore import DDLScraperCore

class IRFreeCore(DDLScraperCore):
	
	def __init__(self):
		super(type(self),self).__init__()
		
		self.__title__		= "IRFree.com"
		self.__url__		= "http://www.irfree.com"
		#self.__url__		= "http://www.irfree.com/tv-shows" # used for filehoster self test
		self.__nextpage__	= '<div class="turnRight"><a'
		# prevent dos attack ;), wait at least 400 milliseconds between every fetch
		# otherwise more than 20 posts per page doesn't work
		self.__delay__ = 0.4
	
		self.__filehoster__	= {}
		self.__filehoster__["0"] =	{ "url": "http://turbobit.net" }
		self.__filehoster__["1"] =	{ "url": "http://extabit.com" }
		#self.__filehoster__[""] =	{ "url": "" }
		
		# ignore the following urls, when looking for new filehosters
		self.__urls__		= []
		self.__urls__.append("http://www.irfree.com")
		self.__urls__.append("http://irfree.net")
		self.__urls__.append("http://www.tv.com")
		self.__urls__.append("http://www.tvrage.com")
		self.__urls__.append("http://www.trutv.com")
		self.__urls__.append("http://www.colbertnation.com")
		self.__urls__.append("http://www.travelchannel.com")
		self.__urls__.append("http://www.wnetwork.com")
		self.__urls__.append("http://tviv.org")
		self.__urls__.append("http://uk.eonline.com")
		#self.__urls__.append("")
		
	#===============================================================================
	#
	# IRFree specific functions
	
	#===============================================================================
	
	def _trimPosts(self, full_website):
		# get only area with the file-links (ignore samples and comments)
		website = self._executeRE('</table></span>(.+?)<a href="http://www.irfree.com/premium-member/"', full_website)
		if (website == None):
			website = self._executeRE('Type The Password(.+?)Tags: ', full_website)
		if (website == None):
			website = self._executeRE('Download(.+?)Tags: ', full_website)
		if (website == None):
			website = self._executeRE('Download(.+?)<p class="postmetacat"', full_website)
		if (website == None):
			website = self._executeRE('Download(.+?)class="ratingBox"', full_website)
		if (website == None):
			# not possible to extract link section, use the whole website for scraping
			website = full_website
		
		return website;
	
	def _extractPosts(self, link, website):
		# 1: url
		# 2: title
		# 3: img
		# 4: description
		posts = re.compile('class="newsTitle">.*?<a href="(.+?)".*?>(.+?)</a>.+?(?:<img.+?src="(.+?)".+?</p>|</p>)(.+?)<ul class="newsActions">',re.DOTALL).findall(website)
		
		# ignore general posts
		for post in posts:
			if (post[0] == "http://www.irfree.com/off-topic/45091-download-files-from-our-private-server.html"):
				posts.remove(post)
		
		return posts
	
	
	#===============================================================================
	#
	# Scrape specific filehoster links from a post
	#
	#===============================================================================
	def _scrapeFilehosterLinksNow( self, website, fh_key ):
		
		fh = self._getFilehoster(fh_key)
		if (fh == None):
			return []
		
		url = fh["url"]
		
		if self.__dbg__:
			print self.__plugin__ + " _scrapeFilehosterLinksNow: starting with " + repr(url)
			
		scraped_links = re.compile('href="(%s.+?)"|>(OR)<|>(SUB)<' % url,re.DOTALL).findall(website);
		
		# put all file links in one list (but only the first block, no alternatives, no links from comments
		file_links = [ ]
		for scraped_link in scraped_links:
			
			if ( len(file_links) > 0 ):
				if (scraped_link[1] == "OR" or scraped_link[1] == "SUB"):
					# ignore alternative file links and sub titles
					break
			
			# add links to list
			if ( len(scraped_link[0]) > 0 ):
				file_links.append(scraped_link[0])
		
		return file_links
	
	def _scrapeFilehosterLinks( self, website):
		file_links = self._scrapeFilehosterLinksNow( website, self.__addon__.getSetting( "filehoster" ) )
		if ( len(file_links) == 0):
			alt_filehoster = self.__addon__.getSetting( "alt_filehoster" )
			if ( alt_filehoster != "-1"):
				file_links = self._scrapeFilehosterLinksNow( website, alt_filehoster )
		
		# remove duplicates
		file_links = set(file_links)
		
		return file_links
	
	
	#===============================================================================
	#
	# SELF TEST
	#
	#===============================================================================
	def _scrapeFilehoster( self, website):
		# extract links
		urls = re.compile('href="(http://.+?)["/]').findall(website)
		return set(urls)
	
	def _getCategories(self):
		categories = []
		
		( full_website, result_str, result) = self._fetchWebsite(self.__url__)
		
		if (result == 200):
			# extract relevant part
			website = self._executeRE('<ul class="category"(.+?)<form id="search"', full_website)
			if ( website == None):
				website = self._executeRE('<ul class="category"(.+?)</div>', full_website)
			# extract categories
			if ( website != None ):
				categories = re.compile('<a href="(.+?)"',re.DOTALL).findall(website)
			
		return categories
	