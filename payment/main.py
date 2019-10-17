import requests
import json

s='http://koabot.com/applications/nexus/interface/licenses/%s'

proxies = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}

u='aeca940a-279c-4f3b-a148-ef1dee884066'
k='c6e75ed00bd8aa22ab486b6763b66d19'

def activate():
	d={'key':k,
		'identifier':u,
		'setIdentifier':'1',
		'extra':json.dumps({'key':k})}
	r=requests.post(s%('?activate'),data=d,proxies=proxies)
	print r.content
	
def check():
	d={'key':k,
		'identifier':u,
		'usage_id':1}
	r=requests.post(s%('?check'),data=d,proxies=proxies)
	print r.content
	
activate()
check()