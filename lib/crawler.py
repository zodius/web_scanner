'''
	Web crawler using thread pool and dictionary file
'''

import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import requests as req

from .signature import Signature, DefaultBadSignature, DefaultGoodSignature

logger = logging.getLogger("Crawler")

class Crawler:
	def __init__(self, url, dictionary_file, max_thread=10, default_signature=True, session=req.session()):
		self.target = url
		self.dictionary_file = dictionary_file
		self.executor = ThreadPoolExecutor(max_workers=max_thread)
		self.session = session

		self.good_sig = None
		self.bad_sig = None

		if default_signature:
			logger.info("Using default signature.")
			self.good_sig = DefaultGoodSignature()
			self.bad_sig = DefaultBadSignature()
	
	def start(self):
		with open(self.dictionary_file, 'r') as dictionary:
			for path in dictionary:
				path = urljoin(self.target, path.replace("\n",""))
				self.executor.submit(self.get, path)
			
			self.executor.shutdown(wait=True)
	
	def get(self, url):
		try:
			res = self.session.get(url)
			if self.good_sig.check(res) and not self.bad_sig.check(res):
				logger.info("%d %s" % (res.status_code, url))
		except Exception as e:
			logger.error(repr(e))
	
	def attach_good(self, sig):
		self.good_sig = sig
	
	def attach_bad(self, sig):
		self.bad_sig = sig