#VERSION: 2.51

#AUTHORS: Adrian Mocan (adrian.mocan@gmail.com)

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from novaprinter import prettyPrinter
from helpers import download_file
#from helpers import retrieve_url, download_file

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from urllib import urlencode, quote, unquote
    from urllib2 import build_opener, HTTPCookieProcessor, URLError, HTTPError
except ImportError:
    from urllib.parse import urlencode, quote, unquote
    from urllib.request import build_opener, HTTPCookieProcessor
    from urllib.error import URLError, HTTPError

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar
    
try:
    import sgmllib
except:
    import sgmllib3

import gzip, tempfile
import re
import os
import tempfile

class filelist(object):
  # your id on filelist.ro:
  # TREBUIE SA INLOCUIESTI username SI password CU USERNAME SI PARLOLA TA DE PE FILELIST
  # YOU NEED TO REPLACE THE USERNAME AND PASSWORD WITH THE ONES YOU HAVE ON FILELIST.RO
  username = 'bula'
  # and your password:
  password = 'parola_lui_bula'
  PAGE_NUMBER = 7
  ## Cookies :
  search_auth = True   # is an authentication necessary to search torrents ?
  download_auth = True  # is an authentication necessary to download torrents ?
  # Debug / Log:
  debug = False
  # URL of the login page:
  login_page = "https://filelist.ro/takelogin.php"
  # ids and values of the login page fields:
  cookie_values = {'username':username, 'password':password}
  # Name of one of the obtained cookies (to verify):
  cookie2verify = 'uid' 
  log_file_name = os.path.join(tempfile.gettempdir(), "qbittorrent_filelist_plugin.log")
  url = 'https://www.filelist.ro'
  name = 'filelist'
#  supported_categories = {'all': '0', 'movies': '11', 'tv': '33', 'music': '3', 'games': '13', 'anime': '19', 'software': '12', 'books': '5'}
  supported_categories = {'all': '0'}
  
  def __init__(self):
    if self.debug:
      # Create a log file, or lets it empty :
      log_file = open(self.log_file_name, "w")
      log_file.write("")
      log_file.close()

  def log(self, msg):
    if self.debug:
      #print(msg)
      log_file = open(self.log_file_name, "a")
      log_file.write(msg)
      log_file.write("\n")
      log_file.close()
      
  def _sign_in(self, what=""):
    self.log("Signing-in")
    # Init the cookie handler.
    cj = CookieJar()
    self.opener = build_opener(HTTPCookieProcessor(cj))
    # self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    # Sign in.
    url_cookie = self.opener.open(self.login_page, urlencode(self.cookie_values).encode('UTF-8')) # (the cj CookieJar gets automatically cookies)
    # Verify cookies
    msg = ""
    if self.cookie2verify != '':
      page_cookie = url_cookie.read(500000)
      msg = ''
      if not self.cookie2verify in [cookie.name for cookie in cj]:
        credentials = (self.username, self.password)
        msg = "Unable to sign in with username={} and password={}".format(self.username,self.password)
        if self.username == 'bula' and self.password == 'parola_lui_bula':
          problem = "Setup error"
          currentFile = os.path.realpath(__file__)
          proposed_solution = "Edit file: '%s' to set user and password (lines 70 and 72)." % currentFile
        else:
          problem = "Sign-in error"
          proposed_solution = "Try to login into filelist.ro using the same credentials."
        self.handle_error(problem, what, proposed_solution)
        msg = msg + " " + proposed_solution
        self.log(msg)
        raise ValueError(msg)
      elif self.debug:
        msg = "Sign-in successful"
    else:
      msg = "cookie '{}' was empty".format(self.cookie2verify)
    self.log(msg)

  def download_torrent(self, url):
    # Sign in:
    if self.download_auth:
      self._sign_in()
      opener = self.opener
    else:
      opener = urllib2.build_opener(urllib2.BaseHandler())
    # Create temporary file to write the torrent file into it
    file, path = tempfile.mkstemp(".torrent")
    file = os.fdopen(file, "wb")
    # Download torrent
    dat = opener.open(url).read()
    # Write it to a file
    file.write(dat)
    file.close()
    # Logging:
    self.log("{}; from: {}".format(path, url))
    print(path+" "+url)


  class FilelistParser(HTMLParser):
    def __init__(self, results, url):
      HTMLParser.__init__(self)
      self.rowCount = 0
      self.columnCount = 0
      self.activeTag = ""
      self.torrentRow = {}
      self.crtTorrent = {}
      self.insideRow = False
      self.torrentrowDepth = 0
      self.url = url
      self.results = results

    def handle_starttag(self, tag, attrs):
      self.activeTag = tag
      attrsDict = dict(attrs)
      if (tag == "a") and (self.columnCount == 2):
        downloadLink = attrsDict["href"]
        self.crtTorrent["link"] = self.createLink(downloadLink, attrsDict["title"])
        self.crtTorrent["desc_link"] = self.url + '/' + downloadLink
      if tag == "div":
        if self.insideRow:
          self.torrentrowDepth += 1
        if (("class" in attrsDict) and (attrsDict["class"] == "torrentrow")):
          self.rowCount += 1
          self.columnCount = 0
          self.torrentRow = {}
          self.crtTorrent = {}
          self.insideRow = True
          self.torrentrowDepth = 0
          self.isFree = False
        if (("class" in attrsDict) and (attrsDict["class"] == "torrenttable")):
          self.columnCount += 1    
      if (tag == "img") and (self.columnCount == 2):
        if (("alt" in attrsDict) and (attrsDict["alt"] == "FreeLeech")):
          self.isFree = True

    def createLink(self, downloadUrl, title):
      """build the download link from the details link, without parsing the download page"""
      newUrl = downloadUrl.replace("details", "download") 
      return self.url + '/' + newUrl
    
    def handle_endtag(self, tag):
      if self.insideRow:
        if tag == "div":
          self.torrentrowDepth -= 1
          if self.torrentrowDepth < 0:
            self.insideRow = False
            self.crtTorrent["name"] = ("FREELEECH " if self.isFree else "") + self.torrentRow["c2"]
            self.crtTorrent["size"] =  self.torrentRow["c7"]
            self.crtTorrent["seeds"] = self.torrentRow["c9"]
            self.crtTorrent["leech"] = self.torrentRow["c10"]
            self.crtTorrent["engine_url"] = self.url
            prettyPrinter(self.crtTorrent)
            self.results.append('a')
           
    def handle_data(self, data):
      if len(data) > 0:
        key = "c" + str(self.columnCount)
        if not (key in self.torrentRow):
          self.torrentRow[key] = data
        # Calculate size (in bytes)
        if (data == "kB"):
          self.torrentRow["c7"] = str(int(float(self.torrentRow["c7"]) * 1024))
        if (data == "MB"):
          self.torrentRow["c7"] = str(int(float(self.torrentRow["c7"]) * 1024 * 1024))
        if (data == "GB"):
          self.torrentRow["c7"] = str(int(float(self.torrentRow["c7"]) * 1024 * 1024 * 1024))
        if (data == "TB"):
          self.torrentRow["c7"] = str(int(float(self.torrentRow["c7"]) * 1024 * 1024 * 1024 * 1024))


  def search(self, what, cat='all'):
    self.log('searching for {}'.format(what))
    """search the torrent parsing the site"""
    # Sign in:
    if self.search_auth:
      self._sign_in(what)
      opener = self.opener
    else:
      opener = urllib2.build_opener(urllib2.BaseHandler())
    ret = []
    page = 0
    while page < self.PAGE_NUMBER:
      results = []
      parser = self.FilelistParser(results, self.url)
      url = "{}/browse.php?search={}&cat={}&searchin=0&sort=0&page={}".format(self.url, what, self.supported_categories[cat], page)
      f = opener.open(url)
      dat = f.read().decode('iso-8859-1', 'replace')
      results_re = re.compile("(?s)<div class='cblock-innercontent'>.*")
      for match in results_re.finditer(dat):
        res_tab = match.group(0)
        parser.feed(res_tab)
        parser.close()
        break
      if len(results) <= 0:
        break
      page += 1
      
  def handle_error(self, error_msg, what, fixForError = ""):
    # we need to add the search text(what) to 'name' so that the error is shown in 
    # qBittorrent when 'Torrent names only' is enabled.
    # So you need to pass 'what' parameter through all the functions chain up to 'handle_error'
    prettyPrinter({
      'seeds': -1,
      'size': -1,
      'leech': -1,
      'engine_url': self.url,
      'link': self.url,
      'desc_link': 'https://github.com/adrianmocan/qbittorrent_plugin_filelist.ro/blob/master/README.adoc',
      'name': "Filelist: %s! Click 'Go to description' button to open help. %s Search was: '%s'" % (error_msg, fixForError, what)
  })
  

