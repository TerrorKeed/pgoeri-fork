import re
from DDLScraperCore import DDLScraperCore

class IRFreeCore(DDLScraperCore):
	
	def __init__(self):
		self.__title__		= "IRFree.com"
		self.__url__		= "http://www.irfree.com"
		self.__nextpage__	= 'class="nextpostslink"'
		# prevent dos attack ;), wait at least 400 milliseconds between every fetch
		# otherwise more than 20 posts per page doesn't work
		self.__delay__ = 0.4
	
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
			website = self._executeRE('Download:(.+?)Tags: ', full_website)
		if (website == None):
			website = self._executeRE('Download:(.+?)<p class="postmetacat"', full_website)
		if (website == None):
			# not possible to extract link section, use the whole website for scraping
			website = full_website
		return website;
	
	def _extractPosts(self, link, website):
		# 1: url
		# 2: title
		# 3: img
		# 4: description
		if ( link == "http://irfree.com" ):
			posts = re.compile('class="entry_header">.+?<a href="(.+?)".*?>(.+?)</a>.+?<img.+?src="(.+?)"(.+?)</p>',re.DOTALL).findall(website)
		elif ( "/?s=" in link ):
			posts = re.compile('class="posts">.+?<a href="(.+?)".*?>(.+?)</a>.+?(?:<img.+?src="(.+?)".+?<p>|<p>)(.+?)</p>',re.DOTALL).findall(website)
		else:
			posts = re.compile('class="page-content">.+?<a href="(.+?)".+?>(.+?)</a>.+?(?:<img.+?src="(.+?)".+?<p>|<p>)(.+?)</p>',re.DOTALL).findall(website)
		return posts
	
	def _scrapeFilehosterLinksNow( self, website, filehoster ):
		if (filehoster == 0):
			url = "http://hotfile.com/dl/"
		elif (filehoster == 1):
			url = "http://www.filesonic.com/file/"
		elif (filehoster == 2):
			url = "http://www.fileserve.com/file/"
		elif (filehoster == 3):
			url = "http://upfile.in"
		elif (filehoster == 4):
			url = "http://www.wupload.com"
		else:
			return [ ]
		
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
		file_links = self._scrapeFilehosterLinksNow( website, int(self.__addon__.getSetting( "filehoster" )) )
		if ( len(file_links) == 0):
			alt_filehoster = int(self.__addon__.getSetting( "alt_filehoster" ))
			if ( alt_filehoster != 0):
				file_links = self._scrapeFilehosterLinksNow( website, (alt_filehoster-1) )
		
		return file_links
	
	def _scrapeFilehoster( self, website):
		# extract links
		urls = re.compile('href="(http://.+?)/').findall(website);
		
		return set(urls)
	
	def _getCategories(self):
		categories = []
		
		( full_website, result_str, result) = self._fetchWebsite(self.__url__)
		
		if (result == 200):
			# extract relevant part
			website = self._executeRE('<li id="categories"(.+?)<li id="archives"', full_website)
			
			categories = re.compile('<a href="(.+?)"',re.DOTALL).findall(website)
			
		return categories
	