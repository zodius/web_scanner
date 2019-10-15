from lib.signature import Signature
from lib.crawler import Crawler

import coloredlogs
coloredlogs.install(fmt="%(asctime)s %(name)s [%(levelname)s] %(message)s")

signature = Signature(status_code=200)
signature.add(lambda x: "an error" not in x.text)

c = Crawler("https://www.youtube.com", "./test_dic.txt", signature=signature)

c.start()