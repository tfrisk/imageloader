"""Image Loader
Finds and downloads images from given url

(C) 2017 Teemu Frisk
Distributed under the MIT License
"""

import argparse #command line argument parser
import sys #exits and version checkings
import os #file functionalities
# try blocks to handle both python 2 and 3
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
try:
    from urllib.error import ContentTooShortError
    from urllib.error import URLError
    from urllib.parse import urlparse
    from urllib.request import urlretrieve
except ImportError:
    from urllib import ContentTooShortError
    from urllib import urlretrieve
    from urllib2 import URLError
    from urlparse import urlparse
from time import sleep
from random import randint
import socket
from datetime import datetime
import requests #http library

class imageLoader:
    """Image loader class"""
    def __init__(self, cmd_args):
        """ Init config from raw command line arguments """
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--url", help="URL to read", required=True)
        parser.add_argument("-D", "--dir", \
            help="Write images to specific directory", required=False, default=False)
        parser.add_argument("-d", "--debug", \
            help="Display debug messages", required=False, action='store_true', default=False)
        parser.set_defaults(dir="saved-images")
        self.args = parser.parse_args(cmd_args)
        #self.savedir = self.args.output.strip()
        self.DEBUG_MODE = self.args.debug

    def get_url_response(self, url):
        """Download url"""
        try:
            resp = requests.get(url)
            stat = resp.status_code
        except requests.ConnectionError:
            pass # continue to return "ERROR", -1
        else:
            if self.DEBUG_MODE:
                print("Downloading URL '" + url + "' returned with status code " + str(stat))
            return resp, stat
        return "ERROR", -1 # return this if we got ConnectionError

    @staticmethod
    def readPageStructure(resp):
        """Read html structure from plain HTTP response"""
        souped_html = BeautifulSoup(resp.content, "lxml")
        return souped_html

    def isUrlValid(self, testurl):
        """Check if URL exists by pinging it"""
        # sleep a bit before request to prevent flooding
        sleep(randint(50, 500) / 1000) # random 50..500 ms
        req = requests.get(testurl)
        if req.status_code == 200:
            return True
        return False

    def formProposedUrl(self, imagepath, proposal):
        """Create proposed url based on proposal case
        Case = append | combine
        """
        if proposal == "append":
            # try to append http to url and see if it helps
            proposed_url = str("http:" + imagepath)
        elif proposal == "combine":
            # guess: combine the base hostname + imagepath
            # for example: "http://solita.fi" and
            # "/wp-content/uploads/Karri.png"
            # will result "http://solita.fi//wp-content/uploads/Karri.png"
            urlparts = urlparse(self.args.url)
            if self.DEBUG_MODE:
                print("urlparts=" + str(urlparts))
            proposed_url = str(urlparts.scheme + "://" + urlparts.netloc + "/" + imagepath)
        return proposed_url

    def formProperImageUrl(self, imagepath):
        """Use some fuzzy logic to figure out the proper image url"""
        # if the image source has proper url
        if imagepath.startswith("http"):
            if self.isUrlValid(imagepath):
                return imagepath

        if imagepath.startswith("//"):
            proposed_url = self.formProposedUrl(imagepath, "append")
            if self.isUrlValid(proposed_url):
                return proposed_url

        proposed_url = self.formProposedUrl(imagepath, "combine")
        if self.isUrlValid(proposed_url):
            return proposed_url
        # nope, it didn't work
        if self.DEBUG_MODE:
            print("imagepath: " + imagepath)
            print("proposed_url: " + proposed_url)
        return "DID_NOT_WORK"

    def findImagesFromHtml(self, scraped_html):
        """
        Parse all <img> tags from html, ignore entries without src attributes
        """
        resultset = {}
        url = ''
        images = scraped_html.find_all("img")
        for image in images:
            source = imageLoader.findKeyOrEmpty(image, "src")
            if not source:
                continue # move to next image, this has no src defined
            alttext = imageLoader.findKeyOrEmpty(image, "alt")
            title = imageLoader.findKeyOrEmpty(image, "title")
            filename = os.path.basename(source)
            print("Image found: [" + filename + "]")
            url = self.formProperImageUrl(source)
            if url == "DID_NOT_WORK":
                print("---- Validation failed")
                continue
            print("++++ Validation ok")
            resultset[filename] = \
                {'src':source, 'alt': alttext, 'title': title, 'url': url, 'filename': filename}
        return resultset

    @staticmethod
    def findKeyOrEmpty(resultset, key):
        """
        Find if collection has key, otherwise return empty string
        """
        try:
            value = resultset[key]
        except KeyError:
            value = ''
        return value

    def downloadFiles(self, downloadlist, downloaddir):
        """Iterate imagelist and download files"""
        logfile = open(os.path.join(downloaddir, "filelist.txt"), "w")
        logfile.truncate()
        logtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        logfile.write(str("Downloaded images from " + self.args.url + " at " + logtime + "\n"))
        logfile.write("----------\n")
        for image in downloadlist.values():
            try:
                urlretrieve(image['url'], os.path.join(downloaddir, image['filename']))
            except (URLError, ContentTooShortError, socket.timeout, IOError) as e:
                # download failed, skip this image
                print("---- " + str(image['url']) + " download failed")
                print(e)
                continue
            print("++++ " + str(image['filename']))
            logfile.write(str(image['url'] + "\n"))
        logfile.write("----------\n")
        logfile.close()

if __name__ == "__main__":
    if sys.version_info <= (2, 7):
        print("Python version is too old, 2.7 or later is required!")
        sys.exit(2)

    loader = imageLoader(sys.argv[1:])

    # handle both absolute and relative paths
    execdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    savepath = loader.args.dir
    if not os.path.isabs(loader.args.dir):
        savepath = os.path.join(execdir, loader.args.dir)
    if not os.path.isdir(savepath):
        try:
            os.makedirs(savepath)
        except PermissionError:
            print("Could not create directory [" + savepath + "]. Stopping.")
            sys.exit(-1)

    if loader.DEBUG_MODE:
        print("Debug mode! Hooray!")
        print("url: " + loader.args.url)
        print("Exec dir: " + os.path.join(os.path.abspath(os.path.dirname(sys.argv[0]))))
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        print("Image loader started at " + str(timestamp))

    # set default socket timeout so we won't end up stuck forever
    socket.setdefaulttimeout(10)

    print("Given URL is " + str(loader.args.url))
    print("Begin reading URL..")
    response, status = loader.get_url_response(loader.args.url)
    if status != 200:
        print("ERROR while reading URL! Stopping.")
        sys.exit(-1)

    print("Read OK, parsing response..")
    parsed_html = loader.readPageStructure(response)
    print("Response parsing OK, forming list of images..")
    imagelist = loader.findImagesFromHtml(parsed_html)
    print("Forming list of images done, found " + str(len(imagelist)) + " images.")

    images_found = len(imagelist)
    if images_found > 0:
        print("Image list formed and validated, downloading files..")
        loader.downloadFiles(imagelist, savepath)
        print("File download finished.")
    else:
        print("No images to download.")
    sys.exit(0)
