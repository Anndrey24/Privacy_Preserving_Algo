from phe import paillier
from phe.paillier import EncryptedNumber
from Supplier import Supplier
from User import User
from TradingPlatform import TradingPlatform
from GridOperator import GridOperator
import time
import random
from math import copysign


grid_op = GridOperator()

user_list = []
suppl_list = []
payload_list = []
no_suppl = 3
no_users = 100
for i in range(no_suppl):
    suppl_list.append(Supplier(str(i), grid_op))

# (is_bid_accepted, bid_type, committed_value, indiv_deviation)
# 1 => buy  /  -1 => sell
start_time = time.time()   
# payload_list = [(1, 1,3,-3), (1, 1,3,1), (1,1,3,3), (1, -1,5,-2), (1, -1,4,1), (0,1,3,3) ]
total = 0
for i in range(no_users-1):
    bid_type = random.choice([-1,1])
    committed = random.random()
    total += bid_type * committed
    indev = random.random()
    payload_list.append((1,bid_type,committed,indev))
payload_list.append((1,int(copysign(1,-total)),abs(-total),random.random()))
print(payload_list)
for payload in payload_list:
    user = User(random.choice(suppl_list))
    user_list.append(user)
    user.update_payload(payload)

payload_time = time.time()
trade_plat = TradingPlatform(algorithm = 4, TP = 0.2, RP = 0.35, FiT = 0.05, user_list = user_list, supplier_list = suppl_list, grid_op = grid_op)
trade_plat.calculate_partial_bills()
trade_plat.calculate_partial_bills()
settlement_time = time.time()


def print_all_results(options):
    # Supplier Decryption
    print("SUPPLIER KEY")
    user_bills_s_enc = trade_plat.get_partial_bills()
    final_user_bills_s_enc = trade_plat.get_final_user_bills()
    suppl_bills_s_enc = trade_plat.get_supplier_bills()
    final_suppl_bills_s_enc = trade_plat.get_final_supplier_bills()

    if options[0]:
        print("ENCRYPTED")
        print("User bills:")
        for i, user in enumerate(user_list):
            print("User ", i," (S",user.get_supplier().get_name(),"): ", [x.ciphertext()%100 for x in user_bills_s_enc[user]], " -> ", final_user_bills_s_enc[user].ciphertext()%100)
        print()
        print("Supplier bills: ")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", [[x.ciphertext()%100 for x in w] for w in suppl_bills_s_enc[supplier]], " -> ", [x.ciphertext()%100 for x in final_suppl_bills_s_enc[supplier]])
        print()

    for user in user_list:
        user_bills_s_enc[user] = [user.get_supplier().decode(x) for x in user_bills_s_enc[user]]
        final_user_bills_s_enc[user] = user.get_supplier().decode(final_user_bills_s_enc[user])


    for supplier in suppl_list:
        for i in range(len(suppl_bills_s_enc[supplier])):
            suppl_bills_s_enc[supplier][i] = [supplier.decode(x) for x in suppl_bills_s_enc[supplier][i]]
        final_suppl_bills_s_enc[supplier] = [supplier.decode(x) for x in final_suppl_bills_s_enc[supplier]]

    if options[1]:
        print("DECRYPTED")
        print("User bills:")
        for i, user in enumerate(user_list):
            print("User ", i, " (S",user.get_supplier().get_name(),"): ", user_bills_s_enc[user], " -> ", final_user_bills_s_enc[user])
        print("Supplier bills:")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", suppl_bills_s_enc[supplier], " -> ", final_suppl_bills_s_enc[supplier])
        print()
    print()


    # GridOp Decryption
    print("GRIDOP KEY")
    user_bills_go_enc = trade_plat.get_partial_bills('go')
    final_user_bills_go_enc = trade_plat.get_final_user_bills('go')
    suppl_bills_go_enc = trade_plat.get_supplier_bills('go')
    final_suppl_bills_go_enc = trade_plat.get_final_supplier_bills('go')

    if options[2]:
        print("ENCRYPTED")
        print("User bills:")
        for i, user in enumerate(user_list):
            print("User ", i, " (S",user.get_supplier().get_name(),"): ", [x.ciphertext()%100 for x in user_bills_go_enc[user]], " -> ", final_user_bills_go_enc[user].ciphertext()%100)
        print()
        print("Supplier bills: ")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", [[x.ciphertext()%100 for x in w] for w in suppl_bills_go_enc[supplier]], " -> ", [x.ciphertext()%100 for x in final_suppl_bills_go_enc[supplier]])
        print()


    for user in user_list:
        user_bills_go_enc[user] = [grid_op.decode(x) for x in user_bills_go_enc[user]]
        final_user_bills_go_enc[user] = grid_op.decode(final_user_bills_go_enc[user])

    for supplier in suppl_list:
        for i in range(len(suppl_bills_go_enc[supplier])):
            suppl_bills_go_enc[supplier][i] = [grid_op.decode(x) for x in suppl_bills_go_enc[supplier][i]]
        final_suppl_bills_go_enc[supplier] = [grid_op.decode(x) for x in final_suppl_bills_go_enc[supplier]]

    if options[3]:
        print("DECRYPTED")
        print("User bills:")
        for i, user in enumerate(user_list):
            print("User ", i, " (S",user.get_supplier().get_name(),"): ", user_bills_go_enc[user], " -> ", final_user_bills_go_enc[user])
        print("Supplier bills:")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", suppl_bills_go_enc[supplier], " -> ", final_suppl_bills_go_enc[supplier])

    print()
    total_supp_keep = 0
    total_pot = 0
    for i, supplier in enumerate(suppl_list):
        sum1 = 0
        for user in supplier.get_users():
            sum1 += final_user_bills_go_enc[user]
        supp_keep = sum(final_suppl_bills_go_enc[supplier])
        total_supp_keep += supp_keep
        total_pot += (-sum1 - supp_keep) 
        print("Supplier ", i ," gets from users ", -sum1, " and needs to keep ", supp_keep, " so it puts ", -sum1 - supp_keep," in the pot")
    print("\nSuppliers keep ", total_supp_keep, " from the users")
    print("Pot after trading period: ", "%.2f" % total_pot, " (should be 0)")

def print_results():
    final_user_bills_s_enc = trade_plat.get_final_user_bills()
    final_suppl_bills_s_enc = trade_plat.get_final_supplier_bills()

    for user in user_list:
        final_user_bills_s_enc[user] = user.get_supplier().decode(final_user_bills_s_enc[user])

    for supplier in suppl_list:
        final_suppl_bills_s_enc[supplier] = [supplier.decode(x) for x in final_suppl_bills_s_enc[supplier]]

    print("User bills:")
    for i, user in enumerate(user_list):
        print("User ", i, " (S",user.get_supplier().get_name(),"): ", final_user_bills_s_enc[user])
    print("Supplier bills:")
    for i, supplier in enumerate(suppl_list):
        print("Supplier ", i, ": ", final_suppl_bills_s_enc[supplier])
    
    print()
    total_supp_keep = 0
    total_pot = 0
    for i, supplier in enumerate(suppl_list):
        sum1 = 0
        for user in supplier.get_users():
            sum1 += final_user_bills_s_enc[user]
        supp_keep = sum(final_suppl_bills_s_enc[supplier])
        total_supp_keep += supp_keep
        total_pot += (-sum1 - supp_keep) 
        print("Supplier ", i ," gets from users ", -sum1, " and needs to keep ", supp_keep, " so it puts ", -sum1 - supp_keep," in the pot")
    print("\nSuppliers keep ", total_supp_keep, " from the users")
    print("Pot after trading period: ", "%.2f" % total_pot, " (should be 0)")

# print_all_results([0,0,0,1])
print_results()
decryption_time = time.time()
print()
print("Payload encryption time: , ", payload_time - start_time)
print("Algorithm time: , ", settlement_time - payload_time)
print("Decryption time: , ", decryption_time - settlement_time)

