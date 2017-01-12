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
try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup

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

	def formProperImageUrl(self,imagepath):
		return os.path.join(self.args.url,imagepath)

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
			url = self.formProperImageUrl(source)
			resultset[filename] = {'src':source, 'alt': alttext, 'title': title, 'url': url}
			#print("src=" + source + ", alt=" + alttext + ", title=" + title + "\n")
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

if __name__ == "__main__":
	if sys.version_info <= (2,7):
		print("Python version is too old, 2.7 or later is required!")
		sys.exit(2)

	loader = imageLoader(sys.argv[1:])

	if (loader.DEBUG_MODE):
		print("Debug mode! Hooray!")
		print("url: " + loader.args.url)

	start_time = timeit.default_timer()

	response, status = loader.getUrlResponse(loader.args.url)
	if (status != 200):
		sys.exit(-1)

	parsed_html = loader.readPageStructure(response)
	imagelist = loader.findImagesFromHtml(parsed_html)

	print("resultset=" + str(imagelist))

	elapsed = timeit.default_timer() - start_time
	sys.exit(0)
