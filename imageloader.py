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
			req = requests.get(url)
			status = req.status_code
		except requests.ConnectionError:
			pass # continue to return "ERROR", -1
		else:
			#print("Downloading URL '" + url + "' returned with status code " + str(status))
			return req, status
		return "ERROR", -1 # return this if we got ConnectionError

if __name__ == "__main__":
	if sys.version_info <= (2,7):
		print("Python version is too old, 2.7 or later is required!")
		sys.exit(2)

	runParameters = imageLoader(sys.argv[1:])

	if (runParameters.DEBUG_MODE):
		print("Debug mode! Hooray!")
		print("url: " + runParameters.args.url)

	start_time = timeit.default_timer()

	imageLoader.getUrlResponse(runParameters.args.url)
	elapsed = timeit.default_timer() - start_time
	sys.exit(0)
