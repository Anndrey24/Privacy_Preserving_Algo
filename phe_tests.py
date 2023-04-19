from phe import paillier
import time
import random
import sys


public_key, private_key = paillier.generate_paillier_keypair()
start = time.process_time()
for i in range(100):
    public_key, private_key = paillier.generate_paillier_keypair()
stop = time.process_time()
print("KeyGen: ", (stop - start) * 10)
list = [random.uniform(-1, 1) for _ in range(1000)]
start = time.process_time()
enc_list = [public_key.encrypt(x) for x in list]
stop = time.process_time()
print("HomoEnc: ", (stop - start))
start = time.process_time()
dec_list = [private_key.decrypt(x) for x in enc_list]
stop = time.process_time()
print("HomoDec: ",(stop - start))
