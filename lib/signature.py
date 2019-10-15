'''
	Signature class determine a set of a good/bad signatures of a url
	For example:
		A web page is consider found with HTTP status code 200 and contain "Good" in title,
		we have Signature(status_code=200, contain="Good")
		A web page is consider not found while HTTP status code is 200, and contain a regex "Page .* is not found" in page body,
		we hace Signature(status_code=200, contain="Page .* is not found")
	
	Supported signature:
		status_code 		HTTP status code
		contain				regular expression contained in response header or body
		not_contain			regular expression not contained in response header or body
		page_size			size of responsed page
'''
import re

class Signature:
	def __init__(self, status_code=0, contain=None, not_contain=None, page_size=0):
		self.filter = []
		
		if status_code != 0:
			self.filter.append(lambda x: x.status_code == status_code)

		if contain is not None:
			contain = re.compile(contain)
			self.filter.append(lambda x: (contain.search(x.text) is not None))

		if not_contain is not None:
			not_contain = re.compile(not_contain)
			self.filter.append(lambda x: (not_contain.search(x.text) is None))

		if page_size > 0:
			self.filter.append(lambda x: len(x.text) == page_size)
	
	def add(self, filter_function):
		self.filter.append(filter_function)
	
	def check(self, page):
		page = [page]
		for f in self.filter:
			page = filter(f, page)
		return len(list(page)) > 0

if __name__ == "__main__":
	# example code
	import requests as req
	url = 'https://www.google.com.tw/'
	signature = Signature(status_code=200, not_contain="an error")

	page1 = req.get(url)
	page2 = req.get(url+"not_exists")

	print("Page 1 is valid? " + ("Y" if signature.check(page1) else "N"))
	print("Page 2 is valid? " + ("Y" if signature.check(page2) else "N"))

	url = 'https://www.youtube.com'

	page1 = req.get(url)
	page2 = req.get(url+"/robots.txt")
	page3 = req.get(url+"/not_exists")

	print("Page 1 is valid? " + ("Y" if signature.check(page1) else "N"))
	print("Page 2 is valid? " + ("Y" if signature.check(page2) else "N"))
	print("Page 3 is valid? " + ("Y" if signature.check(page3) else "N"))
