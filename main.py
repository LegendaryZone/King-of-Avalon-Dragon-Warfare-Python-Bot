from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import argparse
import base64
import hashlib
import hmac
import json
import requests
import time
import zlib

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

api_url='http://dw-us.funplusgame.com/api/'

s=requests.session()
proxies = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}
h={'X-Unity-Version':'5.2.2f1',
'Pragma':'no-cache',
'GDataVer':'v1',
'Expires':'0',
'User-Agent':'kingofavalon/178 CFNetwork/808.2.16 Darwin/16.3.0',
'Accept-Encoding':'gzip',
'Accept-Language':'en-gb',
'Content-Type':'application/octet-stream'}
s.headers.update(h)
s.verify=False

key='/fXAsKvK0gHMbaGTQayi9Q=='
iv='Eeip/teYRjOvkASKbazXUg=='
gameKey='8632781872155bc53b54729c4bdb368c'
mode = AES.MODE_ECB
encoder = PKCS7Encoder()
client_version='2.3.0'
bvg='2.3.0.184.G'

def getSessionID(guid):
	d='idfa=00000000-0000-0000-0000-000000000000&l=en-GB&method=express_signin&game_id=2031&guid=%s&funplus_sdk_version=3.0.38'%(guid)
	auth=MakeSigV3(d)
	return json.loads(s.post('https://passport.funplusgame.com/client_api.php?ver=3',data=d,headers={'Content-Type':'application/x-www-form-urlencoded','User-Agent':'kingofavalon/178 CFNetwork/808.2.16 Darwin/16.3.0','Connection':'keep-alive','Accept-Language':'en-gb','Authorization':auth,
'Accept-Encoding':'gzip, deflate'}).content)

def MakeSigV3(d):
	a_= hmac.new(gameKey, msg=d, digestmod=hashlib.sha256).hexdigest()
	return 'FP 2031:%s'%(base64.b64encode(a_))

def dec(s,res=False):
	e = AES.new(base64.b64decode(key), mode)
	if res:
		try:
			return zlib.decompress(encoder.decode(e.decrypt(base64.b64decode(s))), 16+zlib.MAX_WBITS)
		except:
			return zlib.decompress(encoder.decode(e.decrypt(s)), 16+zlib.MAX_WBITS)
	else:
		try:
			return encoder.decode(e.decrypt(base64.b64decode(s)))
		except:
			return encoder.decode(e.decrypt(s))
	
def enc(s):
	e = AES.new(base64.b64decode(key), mode)
	padded_text = encoder.encode(s)
	return e.encrypt(padded_text)
	
def Init(kingdom_id,fpid,session_key):
	s.headers.update(h)
	d='{"params":{"lang":"en","idfv":"","social_id":"","kingdom_id":%s,"fpid":"%s","device_lang":"","time_zone":"","os_version":"0.0.00","sys_lang":"en-GB","idfa":"","device":"IPhonePlayer","app_version":"0.0.0","session_key":"%s","os":"ios","android_id":"","gaid":""},"method":"init","req_id":"1486562987695.8","class":"call"}'%(kingdom_id,fpid,session_key)
	return doApiCall(enc(d),True)
	
def enterKingdomBlock(city_id,token,enter):
	d='{"params":{"city_id":%s,"leave":[],"client_version":"2.3.0","token":"%s","enter":%s},"method":"enterKingdomBlock","req_id":"1486640324415.21","class":"Map"}'%(city_id,token,enter)
	return doApiCall(enc(d))
	
def getIntegralActivityState(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"getIntegralActivityState","req_id":"1486562990285.43","class":"activity"}'%(token)
	return doApiCall(enc(d))
	
def getIapPackage(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"getIapPackage","req_id":"1486562990414.32","class":"Player"}'%(token)
	return doApiCall(enc(d))

def getUnReadCount(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"getUnReadCount","req_id":"1486562990910.52","class":"Mail"}'%(token)
	return doApiCall(enc(d))

def getBigTimeChest(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"getBigTimeChest","req_id":"1486562991048.24","class":"gift"}'%(token)
	return doApiCall(enc(d))

def loginCheckSingleActivityState(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"loginCheckSingleActivityState","req_id":"1486562991072.78","class":"activity"}'%(token)
	return doApiCall(enc(d))

def loadWarList(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"loadWarList","req_id":"1486562991114.32","class":"Alliance"}'%(token)
	return doApiCall(enc(d))

def paymentPackage(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"paymentPackage","req_id":"1486562991345.62","class":"player"}'%(token)
	return doApiCall(enc(d))

def getPaymentReturnInfo(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"getPaymentReturnInfo","req_id":"1486562991377.53","class":"PaymentReturn"}'%(token)
	return doApiCall(enc(d))
	
def getSuperLoginState(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"getSuperLoginState","req_id":"1486562991560.59","class":"Activity"}'%(token)
	return doApiCall(enc(d))
	
def getKingdomBuffList(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"getKingdomBuffList","req_id":"1486562991627.69","class":"Wonder"}'%(token)
	return doApiCall(enc(d))
	
def getDiyInfo(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"getDiyInfo","req_id":"1486562991677.5","class":"casino"}'%(token)
	return doApiCall(enc(d))
	
def getPaymentLevel(token,uid):
	d='{"params":{"token":"%s","client_version":"2.3.0","uid":%s},"method":"getPaymentLevel","req_id":"1486562991795.2","class":"Player"}'%(token,uid)
	return doApiCall(enc(d))
	
def checkFirstJoinAlliance(token):
	d='{"params":{"client_version":"2.3.0","token":"%s"},"method":"checkFirstJoinAlliance","req_id":"1486562991828.59","class":"Alliance"}'%(token)
	return doApiCall(enc(d))
	
def loadUserBank(token,uid):
	d='{"params":{"token":"%s","client_version":"2.3.0","uid":%s},"method":"loadUserBank","req_id":"1486562991860.74","class":"player"}'%(token,uid)
	return doApiCall(enc(d))

def doSetTutorial(seq,args,fpid,token,session_key):
	d='{"seq":%s,"race_mode":0,"class":"call","params":{"bvr":"2.3.0.184.R","args":%s,"fpid":"%s","token":"%s","bvg":"2.3.0.184.G","client_version":"2.3.0","session_key":"%s","os":"ios","cv":"1486449937","op":"Player:setTutorial"},"req_id":"1486563028785.91","method":"commit"}'%(seq,args,fpid,token,session_key)
	return doApiCall(enc(d))
	
def doTrainTroop(seq,args,fpid,token,session_key):
	d='{"seq":%s,"race_mode":0,"class":"call","params":{"bvr":"2.3.0.184.R","args":%s,"fpid":"%s","token":"%s","bvg":"2.3.0.184.G","client_version":"2.3.0","session_key":"%s","os":"ios","cv":"1486449937","op":"City:trainTroop"},"req_id":"1486563055974.65","method":"commit"}'%(seq,args,fpid,token,session_key)
	return doApiCall(enc(d))
	
def doAddObject(seq,args,fpid,token,session_key):
	d='{"seq":%s,"race_mode":0,"class":"call","params":{"bvr":"2.3.0.184.R","args":%s,"fpid":"%s","token":"%s","bvg":"2.3.0.184.G","client_version":"2.3.0","session_key":"%s","os":"ios","cv":"1486449937","op":"City:addObject"},"req_id":"1486563063251.23","method":"commit"}'%(seq,args,fpid,token,session_key)
	data= doApiCall(enc(d))
	if data['ok']==1:
		return True,data['data']['set']['job'][0]['job_id']
	else:
		print json.dumps(data)
		exit(1)
	
def doFreeSpeedup(seq,args,fpid,token,session_key):
	d='{"seq":%s,"race_mode":0,"class":"call","params":{"bvr":"2.3.0.184.R","args":%s,"fpid":"%s","token":"%s","bvg":"2.3.1.185.G","client_version":"2.3.0","session_key":"%s","os":"ios","cv":"1486449937","op":"City:freeSpeedup"},"req_id":"1486641883430.87","method":"commit"}'%(seq,args,fpid,token,session_key)
	return doApiCall(enc(d))
	
def doUpgradeObject(seq,args,fpid,token,session_key):
	d='{"seq":%s,"race_mode":0,"class":"call","params":{"bvr":"2.3.0.184.R","args":%s,"fpid":"%s","token":"%s","bvg":"2.3.1.185.G","client_version":"2.3.0","session_key":"%s","os":"ios","cv":"1486449937","op":"City:upgradeObject"},"req_id":"1486644923921.42","method":"commit"}'%(seq,args,fpid,token,session_key)
	return doApiCall(enc(d))
	
def doCollectEmpireQuestReward(seq,args,fpid,token,session_key):
	d='{"seq":%s,"race_mode":0,"class":"call","params":{"bvr":"2.3.0.184.R","args":%s,"fpid":"%s","token":"%s","bvg":"2.3.1.185.G","client_version":"2.3.0","session_key":"%s","os":"ios","cv":"1486449937","op":"Quest:collectEmpireQuestReward"},"req_id":"1486640203507.7","method":"commit"}'%(seq,args,fpid,token,session_key)
	return doApiCall(enc(d))
	
def doStartMarch(seq,args,city_id,k,with_dragon,y,x,fpid,token,session_key):
	d='{"seq":%s,"race_mode":0,"class":"call","params":{"bvr":"2.3.0.184.R","args":%s,"city_id":%s,"k":%s,"with_dragon":%s,"y":%s,"x":%s,"type":"gather","job_id":"6385071641215303682"},"fpid":"%s","token":"%s","bvg":"2.3.1.185.G","client_version":"2.3.0","session_key":"%s","os":"ios","cv":"1486449937","op":"PVP:startMarch"},"req_id":"1486640340195","method":"commit"}'%(seq,args,city_id,k,with_dragon,y,x,fpid,token,session_key)
	return doApiCall(enc(d))
	
def doApiCall(cmd,login=False):
	r=s.post(api_url,data=cmd)
	return json.loads(dec(r.content,True))
	
def test(session_key,fpid):
	seq=0
	user_info= Init(0,fpid,session_key)
	seq+=1
	token= user_info['payload']['token']
	uid= user_info['data']['user_info'][0]['uid']
	world_id= user_info['data']['user_info'][0]['world_id']
	power= user_info['data']['user_info'][0]['power']
	name= user_info['data']['user_info'][0]['name']
	city_id= user_info['data']['city_map'][0]['city_id']
	print uid,name,city_id,power
	
def doTutorial(session_key,fpid):
	seq=0
	#step 0
	user_info= Init(0,fpid,session_key)
	#print json.dumps(user_info)
	seq+=1
	token= user_info['payload']['token']
	uid= user_info['data']['user_info'][0]['uid']
	world_id= user_info['data']['user_info'][0]['world_id']
	power= user_info['data']['user_info'][0]['power']
	name= user_info['data']['user_info'][0]['name']
	city_id= user_info['data']['city_map'][0]['city_id']
	print uid,name,city_id,power
	#step 1
	getIapPackage(token)
	#step 2
	getIntegralActivityState(token)
	#step 3
	getUnReadCount(token)
	#step 4
	getBigTimeChest(token)
	#step 5
	loginCheckSingleActivityState(token)
	#step 6
	loadWarList(token)
	#step 7
	paymentPackage(token)
	#step 8
	getPaymentReturnInfo(token)
	#step 9
	getSuperLoginState(token)
	#step 10
	getKingdomBuffList(token)
	#step 11
	getDiyInfo(token)
	#step 12
	getPaymentLevel(token,uid)
	#step 13
	checkFirstJoinAlliance(token)
	#step 14
	loadUserBank(token,uid)
	#step 15
	doSetTutorial(seq,'{"city_id":%s,"tutorial":"eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX2x1bWJlcl9taWxsLjQifX0="}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 15 done'
	#step 16
	doSetTutorial(seq,'{"city_id":%s,"step":1000,"type":200032,"tutorial":"eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX2JhcnJhY2tzLjQifX0="}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 16 done'
	#step 17
	doSetTutorial(seq,'{"city_id":%s,"step":1001,"type":200187,"tutorial":"eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX2Zhcm0uNSJ9fQ=="}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 17 done'
	#step 18
	doSetTutorial(seq,'{"city_id":%s,"step":1002,"type":200001,"tutorial":"eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX3Ryb29wLjQifX0="}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 18 done'
	#step 19
	doTrainTroop(seq,'{"count":20,"instant":false,"gold":0,"city_id":%s,"building_id":1001,"class":"infantry_t1"}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 19 done'
	#step 20
	doSetTutorial(seq,'{"city_id":%s,"tutorial":"eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6IlR1dG9yaWFsX3RpcHMuMiJ9fQ=="}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 20 done'
	#step 21
	doSetTutorial(seq,'{"city_id":%s,"tutorial":"eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIn19"}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 21 done'
	#step 22
	job_res,job_id= doAddObject(seq,'{"instant":false,"gold":0,"city_id":%s,"c_job_id":0,"slot_id":36,"building_id":%s,"type":200001}'%(city_id,int(time.time())),fpid,token,session_key)
	seq+=1
	print 'step 22 done'
	doFreeSpeedup(seq,'{"job_id":%s}'%(job_id),fpid,token,session_key)
	seq+=1
	#step 24
	doCollectEmpireQuestReward(seq,'{"city_id":%s,"quest_id":400001}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 24 done'
	#step 25
	doSetTutorial(seq,'{"city_id":%s,"tutorial":"eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIiwiVHV0b3JpYWxfcXVlc3QiOiJUdXRvcmlhbF9raW5nZG9tLjUifX0="}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'step 25 done'
	#step 27
	doSetTutorial(seq,'{"city_id":%s,"tutorial":"eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIiwiVHV0b3JpYWxfcXVlc3QiOiJmaW5pc2hlZCJ9fQ=="}'%(city_id),fpid,token,session_key)
	seq+=1
	doUpgradeObject(seq,'{"city_id":%s,"c_job_id":0,"building_id":1,"instant":false,"gold":0}'%(city_id),fpid,token,session_key)
	seq+=1
	doSetTutorial(seq,'{"city_id": %s, "tutorial": "eyJjdXJyZW50UHJvY2VzcyI6eyJiZWdpbm5lciI6ImZpbmlzaGVkIiwiVHV0b3JpYWxfcXVlc3QiOiJmaW5pc2hlZCIsIlR1dG9yaWFsX21pbGl0YXJ5X3RlbnQiOiJmaW5pc2hlZCJ9fQ=="}'%(city_id),fpid,token,session_key)
	seq+=1
	print 'tutorial completed'

def getPlayerKey(d):
	return d['data']['session_key'],d['data']['fpid']
	
def main():
	parser = argparse.ArgumentParser(description='King of Avalon Bot')
	parser.add_argument('-p','--proxy', action="store_true", default=False)
	parser.add_argument('-t','--tutorial', action="store_true", default=False)
	parser.add_argument('-g','--guid', dest='guid',default='19e2d1d8bc3946723ce1b2096cb4ceca')
	results =parser.parse_args()
	if results.proxy:
		s.proxies.update(proxies)
	session_key,fpid=getPlayerKey(getSessionID(results.guid))
	if results.tutorial:
		doTutorial(session_key,fpid)
	test(session_key,fpid)
	
if __name__ == '__main__':
	main()