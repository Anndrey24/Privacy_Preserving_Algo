from phe import paillier

public_key, private_key = paillier.generate_paillier_keypair()

list = [-100, -4.567, 6543.2432, 10000000]
enc_list = [public_key.encrypt(x) for x in list]
cypher = public_key.encrypt(5)
enc_calc_list1 = [x - cypher for x in enc_list]
enc_calc_list2 = [x + cypher for x in enc_list]
enc_calc_list3 = [x / 2 for x in enc_list]
enc_calc_list4 = [x + 2 for x in enc_list]
enc_calc_list5 = [x * (-1) for x in enc_list]

print(cypher)

print([private_key.decrypt(x) for x in enc_calc_list1])
print([private_key.decrypt(x) for x in enc_calc_list2])
print([private_key.decrypt(x) for x in enc_calc_list3])
print([private_key.decrypt(x) for x in enc_calc_list4])
print([private_key.decrypt(x) for x in enc_calc_list5])