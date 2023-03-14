from phe import paillier
from phe.paillier import EncryptedNumber
from Supplier import Supplier
from User import User
from TradingPlatform import TradingPlatform
from GridOperator import GridOperator
import time
import random
from math import copysign
from statistics import mean

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

def print_results(trade_plat, user_list, suppl_list):
    final_user_bills_s_enc = trade_plat.get_final_user_bills()
    final_suppl_bills_s_enc = trade_plat.get_final_supplier_bills()

    for user in user_list:
        final_user_bills_s_enc[user] = user.get_supplier().decode(final_user_bills_s_enc[user])

    for supplier in suppl_list:
        final_suppl_bills_s_enc[supplier] = [supplier.decode(x) for x in final_suppl_bills_s_enc[supplier]]

    print("User balance change:")
    for i, user in enumerate(user_list):
        print("User ", i, " (S",user.get_supplier().get_name(),"): ", final_user_bills_s_enc[user])
    print("Supplier balance change:")
    for i, supplier in enumerate(suppl_list):
        print("Supplier ", i, ": ", final_suppl_bills_s_enc[supplier])
    
    print()
    total_supp_keep = 0
    total_pot = 0
    for i, supplier in enumerate(suppl_list):
        suppl_user_bills = 0
        for user in supplier.get_users():
            suppl_user_bills += final_user_bills_s_enc[user]
        supp_keep = sum(final_suppl_bills_s_enc[supplier])
        total_supp_keep += supp_keep
        total_pot += (-suppl_user_bills - supp_keep) 
        print("Supplier ", i ," gets from users ", -suppl_user_bills, " and needs to keep ", supp_keep, " so it puts ", -suppl_user_bills - supp_keep," in the pot")
    print("\nTotal suppliers balance change ", total_supp_keep, " from trading with the users")
    print("Pot after trading period: ", "%.2f" % total_pot, " (should be 0)")
    return total_supp_keep
   

grid_op = GridOperator()

user_list = []
suppl_list = []
payload_list = []
no_suppl = 5
no_users = 100
no_slots = 3
for i in range(no_suppl):
    suppl_list.append(Supplier(str(i), grid_op))
for i in range(no_users):
    user = User(random.choice(suppl_list))
    user_list.append(user)

# (is_bid_accepted, bid_type, committed_value, indiv_deviation)
# 1 => buy  /  -1 => sell
start_time = time.time()   
# payload_list = [(1, 1,3,-3), (1, 1,3,1), (1,1,3,3), (1, -1,5,-2), (1, -1,4,1), (0,1,3,3) ]
for slot in range(no_slots):
    payload_list.append([])
    total = 0
    for i in range(no_users-1):
        bid_type = random.choice([-1,1])
        committed = random.random()
        total += bid_type * committed
        indev = random.random() - 0.5
        payload_list[-1].append((1,bid_type,committed,indev))
    payload_list[-1].append((1,int(copysign(1,-total)),abs(-total),random.random()))  
print("Payloads: ", payload_list)


algo_times = dict()
enc_times = list()
total_supp_keep_list = list()
trade_plat_list = list()
for i in range(1,5):
    trade_plat_list.append(TradingPlatform(algorithm = i, TP = 0.2, RP = 0.35, FiT = 0.05, user_list = user_list, supplier_list = suppl_list, grid_op = grid_op))
    algo_times[i] = []

for i, slot in enumerate(payload_list):
    print("\nEncrypting payloads for slot ", i + 1,"...")
    enc_start = time.time()
    for j, payload in enumerate(slot):
            user_list[j].update_payload(payload)
    enc_times.append(time.time() - enc_start)
    
    print("Running algorithms for slot ", i + 1,"...")
    for i, trade_plat in enumerate(trade_plat_list):
        algo_start_time = time.time()
        trade_plat.calculate_partial_bills()
        algo_times[i+1].append(time.time() - algo_start_time)
        
for i, trade_plat in enumerate(trade_plat_list):  
    print("\n\nResults for algorithm ", i, ":")
    total_supp_keep_list.append(print_results(trade_plat, user_list, suppl_list))

print("\n\nTotal supplier balances: ")
print(total_supp_keep_list)

decryption_time = time.time()
print()
print("Payload encryption time: , ", sum(enc_times)/(no_slots*no_users))
for i in range(len(trade_plat_list)):
    print("Algorithm ",i+1," time: , ", mean(algo_times[i+1]))
# print("Decryption time: , ", decryption_time - settlement_time)

