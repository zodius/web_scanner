# web-scanner #
## Overview ##
Using z3-like grammer to scan web site

## Installation ##
```bash
git clone https://github.com/zodius/web_scanner.git
cd web_scanner
pipenv install
```
## Example code ##
```python
good_signature = DefaultGoodSignature()
bad_signature = DefaultBadSignature()
bad_signature.add(lambda x: "an error" in x.text)

c = Crawler("https://google.com", "./test_dic.txt", default_signature=False)
c.attach_good(good_page)
c.attach_bad(bad_page)

c.start()
```
Full code can be found in web_scanner.py