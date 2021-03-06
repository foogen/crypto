#!/home/playerone/Code/projects/crypto/venv/bin/python3
import struct
import random
import hashlib
import binascii
from utils import Utils
'''
Hashcash cost-function
1. binary infix comparison operator:
a = 010101 1010
b = 010101 1101
-> a =(left, 6) b

this operator is used in the MINT function
MINT(s, w) = T
s: some unique indentifier
w: amount of work = amount of leading zeros
T: token = (s, x) where x is some bitstring that satisfies the amount of work.

pseudocode:
MINT(s,w):
	find x (bit-string) so that Hash(s||x) =(left, w) 0 k-bits bit-string.
	where k = hash output's fixed length
	return (s, x)

VALUE(T) = v
VALUE(.) is a function use to validate token. 
VALUE(T):
	Hash(s||x) =(left, v) 0^k
	return v

if v == w then legit.

'''
random.seed(1234)
UNIQUE = bytes([random.randint(0,255) for i in range(32)])

def sha(x) -> bytes:
	h = hashlib.sha256()
	h.update(x)
	return h.digest()

def infix_comp(a:bytes , b: bytes, w:int) -> bool: 
	str_a = binascii.hexlify(a).decode()
	str_b = binascii.hexlify(b).decode()
	
	if str_a[0:w] == str_b[0:w]:
		return True
	return False
def MINT(s: bytes, w: int) -> (bytes, bytes):
	nonce = 0
	while True:
		x = struct.pack('i', nonce)
		hashIn = s + x
		hashOut = sha(hashIn)
		if infix_comp(hashOut, bytes(32), w):
			return (s,nonce)

		nonce += 1
		#print(binascii.hexlify(x).decode())
def VALUE(s, token):
	return sha(s + token)

if __name__ == '__main__':
	util = Utils()
	myToken = MINT(UNIQUE, 5)[1]
	print(hex(myToken))
	print(util.b2s(VALUE(UNIQUE, struct.pack('i', myToken))))

