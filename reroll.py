# -*- coding: utf-8 -*-
import os
import binascii
from koa import KOA

def createAccs():
	rnd= binascii.hexlify(os.urandom(16))
	api=KOA(rnd)
	#api=KOA('b2cb9b129df941dee617e06144738dd8')
	print api.user_info['power']
	if api.user_info['power']== 5020:
		api.completeTutorial()
	api.upgradeBuildings()
	api.upgradeBuildings()
	api.upgradeBuildings()
	api.checkMail()
	api.useConsumableItem("koabot.com %s"%(binascii.hexlify(os.urandom(3))[:-1]))
	api.refreshTokens()
	s='fpid:%s power:%s name:"%s" uid:%s x:%s y:%s'%(api.user_info['fpid'],api.user_info['power'],api.user_info['name'],api.user_city['uid'],api.user_city['map_x'],api.user_city['map_y'])
	save(s,str(api.user_info['fpid'])+'.json')

createAccs()