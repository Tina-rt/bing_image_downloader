from pathlib import Path
import urllib.request
import urllib
import imghdr
import posixpath
import re

'''
Python api to download image form Bing.
Author: Guru Prasad (g.gaurav541@gmail.com)
'''


class Bing:
    def __init__(self, query, limit, output_dir, adult, timeout,  filter='', verbose=True):
        self.download_count = 0
        self.query = query
        self.output_dir = output_dir
        self.adult = adult
        self.filter = filter
        self.verbose = verbose
        self.seen = set()

        assert type(limit) == int, "limit must be integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout

        self.all_links = []
        # self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.page_counter = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}


    def get_filter(self, shorthand):
            if shorthand == "line" or shorthand == "linedrawing":
                return "+filterui:photo-linedrawing"
            elif shorthand == "photo":
                return "+filterui:photo-photo"
            elif shorthand == "clipart":
                return "+filterui:photo-clipart"
            elif shorthand == "gif" or shorthand == "animatedgif":
                return "+filterui:photo-animatedgif"
            elif shorthand == "transparent":
                return "+filterui:photo-transparent"
            else:
                return ""


    def get_links(self):
        while self.download_count < self.limit:
            if self.verbose:
                print('\n\n[!!]Indexing page: {}\n'.format(self.page_counter + 1))
            # Parse the page source and download pics
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + ('' if self.filter is None else self.get_filter(self.filter))
            request = urllib.request.Request(request_url, None, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf8')
            if html ==  "":
                print("[%] No more images are available")
                break
            links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
            if self.verbose:
                print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
                print("\n===============================================\n")
            self.all_links += links
            # for link in links:
            #     if self.download_count < self.limit and link not in self.seen:
            #         self.seen.add(link)
            #         # self.download_image(link)
            self.download_count += len(links)
            self.page_counter += 1
            
        return self.all_links[:self.limit]

