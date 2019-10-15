from lib.signature import *
from lib.crawler import Crawler

import coloredlogs
coloredlogs.install(fmt="%(asctime)s %(name)s [%(levelname)s] %(message)s")

good_page = DefaultGoodSignature()
bad_page = DefaultBadSignature()
bad_page.add(lambda x: "an error" in x.text)

c = Crawler("https://google.com", "./test_dic.txt", default_signature=False)
c.attach_good(good_page)
c.attach_bad(bad_page)

c.start()