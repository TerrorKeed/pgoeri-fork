import sys, urllib, urllib2, re, pickle, html2text, time, xbmcgui
# ERRORCODES:
# 200 = OK
# 303 = See other (returned an error message)
# 500 = uncaught error

class OneDDLCore(object):
	__addon__		= sys.modules[ "__main__" ].__addon__
	__language__	= sys.modules[ "__main__" ].__language__
	__plugin__		= sys.modules[ "__main__" ].__plugin__
	__dbg__			= sys.modules[ "__main__" ].__dbg__
	__dbgv__		= False
	
	USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"

	#===============================================================================
	#
	# External functions called by OneDDLNavigation.py
	#
	# return MUST be a tupple of ( result[string or dict], status[int] )
	# 
	#===============================================================================
	
	last_fetch = 0

	def __init__(self):
		return None
	
	def scrapePosts(self, link, page ):
		if self.__dbg__:
			print self.__plugin__ + " scrapePosts: " + repr(link) + " - page: " + repr(page)
		
		page_cnt = int(self.__addon__.getSetting( "perpage" )) + 1
		
		from_page = page_cnt * page + 1
		to_page = from_page + page_cnt - 1
		
		( posts, next, result_str, result) = self._scrapePosts( link,from_page,to_page )
		if (result != 200):
			return ( result_str, result )
		
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

		( full_website, result_str, result) = self._fetchWebsite(link)
		
		# get only area with the file-links (ignore samples and comments)
		website = self._executeRE('id="more-(.+?)class="postmeta"', full_website)
		if (website == None):
			# not possible to extract link section, use the whole website for scraping
			website = full_website
			
		if (result == 200):
			links = self._scrapeFilehosterLinks(website)
			if ( len(links) == 0):
				return (self.__language__(30604), 303)
		else:
			return ( result_str , result )
		
		if self.__dbg__:
			print self.__plugin__ + " scrapeFilehosterLinks done: " + str(links)
		return ( links, 200 )

	#=================================== Testing ======================================= 
	def testLinks(self, links):
		for link in links:
			( pagecontent, result_str, result) = self._fetchWebsite(link)
			if ( result != 200):
				print self.__plugin__ + " ERROR: " + link
			

	#===============================================================================
	#
	# Internal functions to OneDDLCore.py
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
			#raw_descr = value[3]
			raw_descr = ""
			
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

	def _fetchWebsite(self, link, recursion_cnt=0):
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
			
			self.last_fetch = time.time()
	
			if self.__dbg__:
				print self.__plugin__ + " _fetchWebsite done"
			return ( website, "", 200 )
		except (urllib2.HTTPError, urllib2.URLError), e:
			if self.__dbg__:
				print self.__plugin__ + " _fetchWebsite exception: " + str(e)
			return ( "", self.__language__(30603), 303 )
		except:
			if self.__dbg__:
				print self.__plugin__ + " _fetchWebsite uncaught exception"
				print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__
								   , sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, sys.exc_info()[1])
				print self.__plugin__ + " _fetchWebsite result: " + repr(website)
			
			return ( "", "", 500 )

	def _scrapePosts( self, link, from_page, to_page ):
		if self.__dbg__:
			print self.__plugin__ + " _scrapePosts: " + link + "(Page %d-%d)" % ( from_page, to_page, )
		
		next = True
		website = ""
		posts = [ ]
		result_str = ""
		result = 200
		page_cnt = to_page - from_page + 1
		
		pDialog = xbmcgui.DialogProgress()
		pDialog.create("OneDDL.com",self.__language__(30700))
		pDialog.update(0)
		for page in range ( from_page, to_page+1 ):
			if pDialog.iscanceled():
				break
			
			( pagecontent, result_str, result) = self._fetchWebsite(link+"/page/"+str(page))
			if ( result != 200):
				break
			
			website += pagecontent
			
			perc = (page-from_page+1)*100/page_cnt
			pDialog.update(int(perc))
			
			# check if there are still more pages after this
			if (re.compile("class='page larger'").search(pagecontent) == None ):
				# abort, if this was the last page
				next = False
				break
		
		pDialog.close()
		
		if ( result == 200 ):
			# 1: url
			# 2: title
			# 3: img
			posts = re.compile('class="posttitle">.+?<a href="(.+?)".+?>(.+?)</a>.+?</div>.+?<img.+?src="(.+?)"',re.DOTALL).findall(website)
		else:
			posts = [ ]

		return ( posts, next, result_str, result)
	
	def _scrapeFilehosterLinksNow( self, website, getHD, get1Click, filehoster ):
		if (filehoster == 0):
			fh_label = "Rapidshare"
		elif (filehoster == 1):
			fh_label = "Hotfile"
		elif (filehoster == 2):
			fh_label = "FileServe"
		elif (filehoster == 3):
			fh_label = "FileSonic"
		elif (filehoster == 4):
			fh_label = "FileFactory"
		else:
			return [ ]
		
		if self.__dbg__:
			print self.__plugin__ + " _scrapeFilehosterLinksNow: filehoster: %s - hd: %s - 1click: %s" % (fh_label, getHD, get1Click)
			
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
		return links
	
	def _executeRE(self, regexp, content, add_flags=0):
		result = re.compile(regexp,re.DOTALL+add_flags).findall( content )
		if ( len(result)>=1 ):
			return result[0]
		else:
			return None
