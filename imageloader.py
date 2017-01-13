#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# F-Secure homework

import argparse #command line argument parser
import sys #exits and version checkings
import os #file functionalities
import re #regex for string parsing
import timeit #execution time calculations
import requests #http library
from lxml import html #html scraper
# try blocks to handle both python 2 and 3
try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup
try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse
try:
	from urllib.parse import quote
except ImportError:
	from urllib import quote
try:
	from urllib.request import urlretrieve
except ImportError:
	from urllib import urlretrieve
from time import sleep
from random import randint

class imageLoader:
	def __init__(self, cmd_args):
		""" Init config from raw command line arguments """
		parser = argparse.ArgumentParser()
		parser.add_argument("-u","--url", help="URL to read", required=True)
		parser.add_argument("-d","--debug", help="Display debug messages", required=False, action='store_true', default=False)
		parser.add_argument("-O","--output", help="Write images to specific directory", required=False, action='store_true', default=False)
		parser.set_defaults(output="saved-images")
		self.args = parser.parse_args(cmd_args)
		self.DEBUG_MODE = self.args.debug

	@staticmethod
	def getUrlResponse(url):
		"""Download url
		"""
		try:
			response = requests.get(url)
			status = response.status_code
		except requests.ConnectionError:
			pass # continue to return "ERROR", -1
		else:
			#print("Downloading URL '" + url + "' returned with status code " + str(status))
			return response, status
		return "ERROR", -1 # return this if we got ConnectionError

	@staticmethod
	def readPageStructure(response):
		"""Read html structure from plain HTTP response"""
		html = BeautifulSoup(response.content, "lxml")
		return html

	def isUrlValid(self,url):
		"""Check if URL exists by pinging it"""
		# sleep a bit before request to prevent flooding
		sleep(randint(50,500)/1000) # random 50..500 ms
		req = requests.get(url)
		if (req.status_code == 200):
			return True
		return False

	def formProperImageUrl(self,imagepath):
		"""Use some fuzzy logic to figure out the proper image url"""
		# if the image source has proper url
		if (imagepath.startswith("http")):
			if self.isUrlValid(imagepath):
				return imagepath
		# try to append http to url and see if it helps
		if (imagepath.startswith("//")):
			proposed_url = str("http:" + imagepath)
			if self.isUrlValid(proposed_url):
				return proposed_url
		# guess: combine the base hostname + imagepath
		# for example: "http://solita.fi" and
		# "/wp-content/uploads/Karri.png"
		# will result "http://solita.fi//wp-content/uploads/Karri.png"

		urlparts = urlparse(self.args.url)
		#print("urlparts=" + str(urlparts))
		proposed_url = str(urlparts.scheme + "://" + urlparts.netloc + "/" + imagepath)
		if self.isUrlValid(proposed_url):
			return proposed_url
		# nope, it didn't work
		print("imagepath: " + imagepath)
		print("proposed_url: " + proposed_url)
		return "DID_NOT_WORK"

	def findImagesFromHtml(self,parsed_html):
		resultset = {}
		url=''
		images = parsed_html.find_all("img")
		for image in images:
			source = imageLoader.findKeyOrEmpty(image,"src")
			if not source:
				continue # move to next image, this has no src defined
			alttext = imageLoader.findKeyOrEmpty(image,"alt")
			title = imageLoader.findKeyOrEmpty(image,"title")
			filename = os.path.basename(source)
			print("Image found: [" + filename + "]")
			url = self.formProperImageUrl(source)
			if (url == "DID_NOT_WORK"):
				print("---- Validation failed")
				continue
			print("++++ Validation ok")
			resultset[filename] = {'src':source, 'alt': alttext, 'title': title, 'url': url, 'filename': filename}
		return resultset

	@staticmethod
	def findKeyOrEmpty(resultset, key):
		"""
		Find if collection has key, otherwise return empty string
		>>> imageLoader.findKeyOrEmpty({"a":1, "b":2}, "a")
		1
		>>> imageLoader.findKeyOrEmpty({"a":1, "b":2}, "c")
		''
		"""
		try:
			value = resultset[key]
		except KeyError:
			value = ''
		return value

	@staticmethod
	def downloadFiles(imagelist):
		"""Iterate imagelist and download files"""
		print("imagelist=" + str(imagelist.values()))
		for image in imagelist.values():
			print("image=" + str(image['url']))
			urlretrieve(image['url'], image['filename'])

if __name__ == "__main__":
	if sys.version_info <= (2,7):
		print("Python version is too old, 2.7 or later is required!")
		sys.exit(2)

	loader = imageLoader(sys.argv[1:])

	if (loader.DEBUG_MODE):
		print("Debug mode! Hooray!")
		print("url: " + loader.args.url)

	start_time = timeit.default_timer()
	print("Image loader started at " + str(start_time))

	print("Given URL is " + str(loader.args.url))
	print("Begin reading URL..")
	response, status = loader.getUrlResponse(loader.args.url)
	if (status != 200):
		print("ERROR while reading URL! Stopping.")
		sys.exit(-1)

	print("Read OK, parsing response..")
	parsed_html = loader.readPageStructure(response)
	print("Response parsing OK, forming list of images..")
	imagelist = loader.findImagesFromHtml(parsed_html)
	print("Forming list of images OK, found " + str(len(imagelist)) + " images.")
	#print("resultset=" + str(imagelist))

	print("Image list formed and validated, downloading files..")
	loader.downloadFiles(imagelist)
	print("File download OK.")
	elapsed = timeit.default_timer() - start_time
	sys.exit(0)
