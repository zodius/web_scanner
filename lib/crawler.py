'''
	Web crawler using thread pool and dictionary file
'''

import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import requests as req

from .signature import Signature

logger = logging.getLogger("Crawler")

class Crawler:
	def __init__(self, url, dictionary_file, max_thread=10, signature=None, session=req.session()):
		self.target = url
		self.dictionary_file = dictionary_file
		self.executor = ThreadPoolExecutor(max_workers=max_thread)
		self.session = session
		self.signature = signature

		if signature is None:
			logger.info("Using default signature.")
			self.signature = Signature(status_code=200)
	
	def start(self):
		with open(self.dictionary_file, 'r') as dictionary:
			for path in dictionary:
				path = urljoin(self.target, path.replace("\n",""))
				self.executor.submit(self.get, path)
			
			self.executor.shutdown(wait=True)
	
	def get(self, url):
		try:
			res = self.session.get(url)
			if self.signature.check(res):
				logger.info("%d %s" % (res.status_code, url))
		except Exception as e:
			logger.error(repr(e))