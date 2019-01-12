# requirements

- requests
- pymongo
-  BeautifulSoup
-  re
-  json
-  multiprocessing 

# Config

MONGO_URL ='localhost'
MONGO_DB = 'toutiao'
MONGO_TABLE = 'toutiao'

GROUP_START = 1
GROUP_END = 2
KEYWORD = '模特'


# Run

`python3 ajax_clawer.py`

then it will download a lot of pic from www.toutiao.com
