# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder
import base64
import hashlib
import hmac
import zlib

class AesCoder(object):
	def __init__(self):		
		self.key='/fXAsKvK0gHMbaGTQayi9Q=='
		self.iv='Eeip/teYRjOvkASKbazXUg=='
		self.gamekey='8632781872155bc53b54729c4bdb368c'
		self.mode = AES.MODE_ECB
		self.encoder = PKCS7Encoder()
		
	def Decode(self,cipherText,res=False):
		e = AES.new(base64.b64decode(self.key), self.mode)
		if res:
			try:
				return zlib.decompress(self.encoder.decode(e.decrypt(base64.b64decode(cipherText))), 16+zlib.MAX_WBITS)
			except:
				return zlib.decompress(self.encoder.decode(e.decrypt(cipherText)), 16+zlib.MAX_WBITS)
		else:
			try:
				return self.encoder.decode(e.decrypt(base64.b64decode(cipherText)))
			except:
				return self.encoder.decode(e.decrypt(cipherText))

	def Encode(self,plainText):
		e = AES.new(base64.b64decode(self.key), self.mode)
		padded_text = self.encoder.encode(plainText)
		return e.encrypt(padded_text)
	
	def MakeSigV3(self,postData):
		return 'FP 2031:%s'%(base64.b64encode(hmac.new(self.gamekey, msg=postData, digestmod=hashlib.sha256).hexdigest()))