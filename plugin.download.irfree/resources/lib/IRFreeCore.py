import sys, urllib, urllib2, re, pickle, html2text
# ERRORCODES:
# 200 = OK
# 303 = See other (returned an error message)
# 500 = uncaught error

class IRFreeCore(object):
	__addon__ = sys.modules[ "__main__" ].__addon__
	__language__ = sys.modules[ "__main__" ].__language__
	__plugin__ = sys.modules[ "__main__" ].__plugin__
	__dbg__ = sys.modules[ "__main__" ].__dbg__
	__dbgv__ = False
	
	USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"

	#===============================================================================
	#
	# External functions called by IRFreeNavigation.py
	#
	# return MUST be a tupple of ( result[string or dict], status[int] )
	# 
	#===============================================================================
	
	def __init__(self):
		return None
	
	def scrapePosts(self, link, page ):
		if self.__dbg__:
			print self.__plugin__ + " scrapePosts: " + repr(link) + " - page: " + repr(page)
		
		page_cnt = ( 1, 2, 3, 4, 5 )[ int( self.__addon__.getSetting( "perpage" ) ) ]
		
		from_page = page_cnt * page + 1
		to_page = from_page + page_cnt - 1
		
		( posts, next, result) = self._scrapePosts( link,from_page,to_page )
		if (result != 200):
			return ( posts, result )
		
		objects = []
		for post in posts:
			objects.append(self._getPostInfo(post))
		
		# set next status of last scraped post
		if (next == False):
			objects[-1]['next'] = "false"
		
		if self.__dbg__:
			print self.__plugin__ + " scrapePosts done"
		return ( objects, 200 )

	def scrapeFilehosterLinks(self, link ):
		if self.__dbg__:
			print self.__plugin__ + " scrapeFilehosterLinks: " + repr(link)

		( website, result) = self._fetchWebsite(link)
		
		# get only area with the file-links (ignore samples and comments)
		website = re.compile('</table></span>(.+?)<a href="http://www.irfree.com/premium-member/" >',re.DOTALL).findall( website )[0]
		
		if (result == 200):
			file_links = self._scrapeFilehosterLinks( website, int(self.__addon__.getSetting( "filehoster" )) )
			if ( len(file_links) == 0):
				alt_filehoster = int(self.__addon__.getSetting( "alt_filehoster" ))
				if ( alt_filehoster != 0):
					file_links = self._scrapeFilehosterLinks( website, (alt_filehoster-1) )
			
			if ( len(file_links) == 0):
				return (self.__language__(30604), 303)
		else:
			return ( [ ], result )
		
		if self.__dbg__:
			print self.__plugin__ + " scrapeFilehosterLinks done: " + str(file_links)
		return ( file_links, 200 )


	#===============================================================================
	#
	# Internal functions to IRFreeCore.py
	#
	# Return should be value(True for bool functions), or False if failed.
	#
	# False MUST be handled properly in External functions
	#
	#===============================================================================

	def _getPostInfo(self, value):
		if self.__dbg__:
			print self.__plugin__ + " _getPostInfo: " + value[1]

		try:
			post = {}
			
			post['url'] = value[0]
			post['raw_title'] = value[1]
			post['img'] = value[2]
			raw_descr = value[3]
			
			"""
			# try to extract info from descr
			release_name = re.compile("release name:</strong>(.+?)<", re.IGNORECASE).findall(raw_descr)
			for tmp in release_name:
				post['release_name'] = tmp
				plot += "Release name: "+ tmp + "\n"
			
			tmps = re.compile("audio quality:</strong>(.+?)<", re.IGNORECASE).findall(raw_descr)
			for tmp in tmps:
				post['audio_quality'] = tmp
				plot += tmp + "\n"
				
			tmps = re.compile("video quality:</strong>(.+?)<", re.IGNORECASE).findall(raw_descr)
			for tmp in tmps:
				post['video_quality'] = tmp
				plot += tmp + "\n"
				
			tmps = re.compile("size:</strong>(.+?)<", re.IGNORECASE).findall(raw_descr)
			for tmp in tmps:
				post['size_str'] = tmp
				plot += tmp + "\n"
			"""
			
			# fill video specific fields, used by info dialog
			post['Title'] = html2text.html2text(post['raw_title'].decode('utf-8'))
			#for now, just show raw_descr
			post['Plot'] = html2text.html2text(raw_descr.decode('utf-8'))
			# per default, there is always a next page (if not, will be set in parent function)
			post['next'] = "true"

			if self.__dbg__:
				print self.__plugin__ + " _getPostInfo done"
			return post;
		except:
			if self.__dbg__:
				print self.__plugin__ + " _getPostInfo uncaught exception"
				print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__
								   , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				
			return ( dict(), 500 )

	def _fetchWebsite(self, link):
		if self.__dbg__:
			print self.__plugin__ + " _fetchWebsite: " + repr(link)
		website = ""

		url = urllib2.Request(link)
		url.add_header('User-Agent', self.USERAGENT)
		try:
			con = urllib2.urlopen(url)
			website = con.read()
			if self.__dbgv__:
				print self.__plugin__ + " _fetchWebsite result: " + repr(website)
			con.close()
			
			if self.__dbg__:
				print self.__plugin__ + " _fetchWebsite done"
			return ( website, 200 )
		except urllib2.HTTPError, e:
			if self.__dbg__:
				print self.__plugin__ + " _fetchWebsite exception: " + str(e)
			return ( self.__language__(30603), "303" )
		except:
			if self.__dbg__:
				print self.__plugin__ + " _fetchWebsite uncaught exception"
				print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__
								   , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				print self.__plugin__ + " _fetchWebsite result: " + repr(website)
			
			return ( "", 500 )

	def _scrapePosts( self, link, from_page, to_page ):
		if self.__dbg__:
			print self.__plugin__ + " _scrapePosts: " + link + "(Page %d-%d)" % ( from_page, to_page, )
		
		next = True
		website = ""
		posts = [ ]
		result = 200
		
		for page in range ( from_page, to_page+1 ):
			( pagecontent, result) = self._fetchWebsite(link+"/page/"+str(page))
			if ( result != 200):
				break;
			
			website += pagecontent
			
			# check if there are still more pages after this
			if (re.compile('class="nextpostslink"').search(pagecontent) == None ):
				# abort, if this was the last page
				next = False
				break
		
		if ( result == 200 ):
			posts = re.compile('class="storytitle"><a href="(.+?)" rel="bookmark">(.+?)</a>.+?<p><img.+?src="(.+?)".+?</p>\n(.+?)</div><!-- end storycontent',re.DOTALL).findall(website);
			#posts = re.compile('class="storytitle"><a href="(.+?)" rel="bookmark">(.+?)</a>.+?<p><img.+?src="(.+?)".+?</p>\n(.+?)<p>.+?class="more-link"',re.DOTALL).findall(website);
		else:
			posts = [ ]

		return ( posts, next, result)

	def _scrapeFilehosterLinks( self, website, filehoster ):
		if (filehoster == 0):
			url = "http://hotfile.com/dl/"
		elif (filehoster == 1):
			url = "http://www.filesonic.com/file/"
		elif (filehoster == 2):
			url = "http://www.fileserve.com/file/"
		else:
			return [ ]
		
		if self.__dbg__:
			print self.__plugin__ + " _scrapeFilehosterLinks: starting with " + repr(url)
			
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