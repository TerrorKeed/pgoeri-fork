import sys, urllib, urllib2, re, pickle, html2text, time, os, xbmcgui, xbmc, socket
from operator import itemgetter
from PluginException import PluginException
# ERRORCODES:
# 200 = OK
# 303 = See other (returned an error message)
# 500 = uncaught error

class DDLScraperCore(object):
	__addon__		= sys.modules[ "__main__" ].__addon__
	__language__	= sys.modules[ "__main__" ].__language__
	__plugin__		= sys.modules[ "__main__" ].__plugin__
	__dbg__			= sys.modules[ "__main__" ].__dbg__
	__dbgv__		= False
	# the following members must be set in the child class
	__title__		= ""
	__url__			= ""
	__nextpage__	= ""
	__delay__		= 0.0
	__filehoster__	= {}
	__urls__		= []
	
	USERAGENT			= "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
	BASE_RESOURCE_PATH	= xbmc.translatePath( __addon__.getAddonInfo( "Profile" ) )
	
	#===============================================================================
	#
	# External functions called by Navigation Class
	#
	# return MUST be a tuple of ( result[string or dict], status[int] )
	# 
	#===============================================================================
	
	last_fetch = 0

	def __init__(self):
		# make sure addon_data dir exists
		try: os.mkdir(self.BASE_RESOURCE_PATH)
		except: pass
		
		return None
	
	def _log(self,msg):
		if self.__dbg__:
			print self.__plugin__ + " DEBUG: " + msg
			
	def _info(self,msg):
		print self.__plugin__ + " INFO: " + msg
			
	def _error(self,msg):
		print self.__plugin__ + " ERROR: " + msg

	def _raise(self,msg):
		self._error(msg)
		raise PluginException(msg)

	def _exception(self,function):
		print self.__plugin__ + " uncaught exception in " + function
		print 'ERROR: %s::%s (%d) - %s' % (self.__class__.__name__,
										sys.exc_info()[2].tb_frame.f_code.co_name,
										sys.exc_info()[2].tb_lineno,
										sys.exc_info()[1])
		
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
		if (len(objects)>0 and next == False):
			objects[-1]['next'] = "false"
		
		if self.__dbg__:
			print self.__plugin__ + " scrapePosts done"
		return ( objects, 200 )

	def scrapeFilehosterLinks(self, link ):
		if self.__dbg__:
			print self.__plugin__ + " scrapeFilehosterLinks: " + repr(link)

		( full_website, result_str, result) = self._fetchWebsite(link)
		
		# get only area with the file-links (ignore samples and comments)
		website = self._trimPosts(full_website)
			
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
	def _testLinks(self, links):
			
		pDialog = xbmcgui.DialogProgress()
		pDialog.create(self.__title__,self.__language__(30702))
		pDialog.update(0)
			
		cnt = len(links)
		idx = 0
		for link in links:
			if pDialog.iscanceled():
				break
				
			( pagecontent, result_str, result) = self._fetchWebsite(link)
			if ( result != 200):
				print self.__plugin__ + " ERROR: " + link
				
			idx += 1
			perc = idx*100.0/cnt
			pDialog.update(int(perc))
			
		pDialog.close()
	
	def _testSearchNewCategories(self, my_links):
		all_links = self._getCategories()
		
		for link in all_links:
			if "http://" not in link:
				link = self.__url__ + link
			if (link.rstrip("/") not in my_links):
				self._error("New categorie found: "+link)

	def _testScrapeFileHoster(self, link ):
		if self.__dbg__:
			print self.__plugin__ + " scrapeFilehoster: " + repr(link)

		( full_website, result_str, result) = self._fetchWebsite(link)
		
		# get only area with the file-links (ignore samples and comments)
		website = self._trimPosts(full_website)
			
		if (result == 200):
			filehoster = self._scrapeFilehoster(website)
		else:
			filehoster = ()
		
		return filehoster
	
	def _getFileHosterFlag(self, filehoster):
		found = False
		
		for url in self.__urls__:
			if (filehoster.startswith(url)):
				return "L"	# this is a known none filehoster url
		
		for fh in self.__filehoster__.values():
			if (("label" in fh and filehoster == fh["label"]) or
				("label_alt" in fh and filehoster == fh["label_alt"]) or
				("url" in fh and filehoster == fh["url"])):
				found = True # known filehoster
				break
		
		if (found):
			return " "	# known filehoster
		else:
			return "*"	# new filehoster!
	
	def _testSearchAllFileHoster(self):
		all_filehoster = {}
		( posts, next, result_str, result) = self._scrapePosts( self.__url__, 0, 9 )
		if (result == 200):
			
			pDialog = xbmcgui.DialogProgress()
			pDialog.create(self.__title__,self.__language__(30701))
			pDialog.update(0)
			
			cnt = len(posts)
			idx = 0
			for post in posts:
				if pDialog.iscanceled():
					break
				
				filehoster = self._testScrapeFileHoster(post[0])
				
				for fh in filehoster:
					fh = fh.lower();
					
					# extract specific posts for testing a specific filehoster
					#if (fh == "bitshare"):
					#	print "BITSHARE:"+post[0]
					
					if fh in all_filehoster:
						all_filehoster[fh] = all_filehoster[fh] + 1
					else:
						all_filehoster[fh] = 1
				
				idx += 1
				perc = idx*100.0/cnt
				pDialog.update(int(perc))
			
			pDialog.close()
		
		# sort all found filehoster by number of occurence	
		sorted_fh = sorted(all_filehoster.iteritems(), key=itemgetter(1), reverse=True)
		
		# save results to file
		fh_file = os.path.join( self.BASE_RESOURCE_PATH , "filehoster.txt" )
		try:
			f = open(fh_file,"wb")
			pickle.dump(sorted_fh,f)
			f.close()
		except IOError:
			self._exception("_testSearchAllFileHoster")
	
	def _testPrintAllFileHoster(self):
		# load filehoster from file
		fh_file = os.path.join( self.BASE_RESOURCE_PATH , "filehoster.txt" )
		try:
			f = open(fh_file,"rb")
			sorted_fh = pickle.load(f)
			f.close()
			
			# print filehoster
			self._info("All filehoster:\n"+str("\n".join([self._getFileHosterFlag(fh[0])+" "+str(fh[1]).ljust(3)+": "+fh[0] for fh in sorted_fh])))
		except IOError:
			self._exception("_testPrintAllFileHoster")
	
	def selfTest(self, feeds):
		# test all category links (this takes a while)
		self._testLinks(feeds)
		
		# search for new category links
		self._testSearchNewCategories(feeds)
		
		# search for all available file hoster and save it to a file
		self._testSearchAllFileHoster()
		
		# print all filehoster from that file
		self._testPrintAllFileHoster()
		
		self._info("self test DONE!")
	
	#===============================================================================
	#
	# Internal functions to DDLScraperCore.py
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
			self._exception("_getPostInfo")
				
			return ( dict(), 500 )

	def _fetchWebsite(self, link, recursion_cnt=0):
		if self.__dbg__:
			print self.__plugin__ + " _fetchWebsite: " + repr(link)
		website = ""
		 
		if (self.__delay__ > 0.0):
			while (self.last_fetch+self.__delay__>time.time()):
				time.sleep(0.1)
			
		url = urllib2.Request(link)
		url.add_header('User-Agent', self.USERAGENT)
		try:
			con = urllib2.urlopen(url) # timeout=
			website = con.read()
			if self.__dbgv__:
				print self.__plugin__ + " _fetchWebsite result: " + repr(website)
			con.close()
			
			self.last_fetch = time.time()
	
			if self.__dbg__:
				print self.__plugin__ + " _fetchWebsite done"
			return ( website, "", 200 )
		except (urllib2.HTTPError, urllib2.URLError), e:
			# retry access via recursion for a maximum of 20 tries (prevent endless loop)
			if (isinstance(e,urllib2.URLError) and not isinstance(e,urllib2.HTTPError)):
				if (e.reason[0]==111 and recursion_cnt<20):
					# irfree.com refused connection due to too short access intervals
					# access will be refused for about 1 sec
					time.sleep(0.5)
					if self.__dbg__:
						print self.__plugin__ + " _fetchWebsite : access denied, sleep and try again in 500ms"
					return self._fetchWebsite(link,recursion_cnt+1)
			if self.__dbg__:
				print self.__plugin__ + " _fetchWebsite exception: " + str(e)
			return ( "", self.__language__(30603), 303 )
		except:
			self._exception("_fetchWebsite")
			if self.__dbg__:
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
		pDialog.create(self.__title__,self.__language__(30700))
		pDialog.update(0)
		for page in range ( from_page, to_page+1 ):
			if pDialog.iscanceled():
				break
			
			page_link = self._preparePageLink(link,page)
			
			( pagecontent, result_str, result) = self._fetchWebsite(page_link)
			if ( result != 200):
				break
			
			website += pagecontent
			
			perc = (page-from_page+1)*100/page_cnt
			pDialog.update(int(perc))
			
			# check if there are still more pages after this
			if (re.compile(self.__nextpage__).search(pagecontent) == None ):
				# abort, if this was the last page
				next = False
				break
		
		pDialog.close()
		
		if ( result == 200 ):
			posts = self._extractPosts(link,website)
		else:
			posts = [ ]

		return ( posts, next, result_str, result)
	
	def _executeRE(self, regexp, content, add_flags=0):
		result = re.compile(regexp,re.DOTALL+add_flags).findall( content )
		if ( len(result)>=1 ):
			return result[0]
		else:
			return None

	def _trimPosts(self, full_website):
		return full_website
	
	def _preparePageLink(self, link, page):
		if ("/?s=" in link):
			# special hack for the search result pages
			if (page > 1):
				page_link = link.replace("/?s=","/page/"+str(page)+"/?s=")
			else:
				page_link = link 
		else:
			page_link = link+"/page/"+str(page)
		return page_link
	
	def _getFilehoster(self, fh_key):
		
		if (fh_key not in self.__filehoster__.keys()):
			self._raise(self.__language__(30900))
			return None
		
		return self.__filehoster__[fh_key]
		