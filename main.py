from phe import paillier
from phe.paillier import EncryptedNumber
from Supplier import Supplier
from User import User
from TradingPlatform import TradingPlatform
from GridOperator import GridOperator
import time
import random


grid_op = GridOperator()

user_list = []
suppl_list = []
no_suppl = 2
for i in range(no_suppl):
    suppl_list.append(Supplier(str(i), grid_op))

start_time = time.time()   
payload_list = [(1, 1,3,-3), (1, 1,3,1), (1, 1,3,3), (1, -1,3,-2), (1, -1,3,1), (1, -1,3,3)]
for payload in payload_list:
    user = User(random.choice(suppl_list))
    user_list.append(user)
    user.update_payload(payload)

payload_time = time.time()
trade_plat = TradingPlatform(algorithm = 4, TP = 0.75, RP = 1, FiT = 0.5, user_list = user_list, supplier_list = suppl_list, grid_op = grid_op)
trade_plat.calculate_partial_bills()
settlement_time = time.time()


def print_results(options):
    # Supplier Decryption
    print("SUPPLIER KEY")
    user_bills_s_enc = trade_plat.get_partial_bills()
    suppl_bills_s_enc = trade_plat.get_supplier_bills()

    if options[0]:
        print("ENCRYPTED")
        print("User bills:")
        for i, user in enumerate(user_list):
            print("User ", i," (S",user.get_supplier().get_name(),"): ", [x.ciphertext()%100 for x in user_bills_s_enc[user]])
        print()
        print("Supplier bills: ")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", [[x.ciphertext()%100 for x in w] for w in suppl_bills_s_enc[supplier]])
        print()

    for user in user_list:
        user_bills_s_enc[user] = [user.get_supplier().decode(x) for x in user_bills_s_enc[user]]


    for supplier in suppl_list:
        for i in range(len(suppl_bills_s_enc[supplier])):
            suppl_bills_s_enc[supplier][i] = [supplier.decode(x) for x in suppl_bills_s_enc[supplier][i]]

    if options[1]:
        print("DECRYPTED")
        print("User bills:")
        for i, user in enumerate(user_list):
            print("User ", i, " (S",user.get_supplier().get_name(),"): ", user_bills_s_enc[user])
        print("Supplier bills:")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", suppl_bills_s_enc[supplier])
        print()
    print()


    # GridOp Decryption
    print("GRIDOP KEY")
    user_bills_go_enc = trade_plat.get_partial_bills('go')
    suppl_bills_go_enc = trade_plat.get_supplier_bills('go')

    if options[2]:
        print("ENCRYPTED")
        print("User bills:")
        for i, user in enumerate(user_list):
            print("User ", i, " (S",user.get_supplier().get_name(),"): ", [x.ciphertext()%100 for x in user_bills_go_enc[user]])
        print()
        print("Supplier bills: ")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", [[x.ciphertext()%100 for x in w] for w in suppl_bills_go_enc[supplier]])
        print()


    for user in user_list:
        user_bills_go_enc[user] = [grid_op.decode(x) for x in user_bills_go_enc[user]]

    for supplier in suppl_list:
        for i in range(len(suppl_bills_go_enc[supplier])):
            suppl_bills_go_enc[supplier][i] = [grid_op.decode(x) for x in suppl_bills_go_enc[supplier][i]]

    if options[3]:
        print("DECRYPTED")
        print("User bills:")
        for i, user in enumerate(user_list):
            print("User ", i, " (S",user.get_supplier().get_name(),"): ", user_bills_go_enc[user])
        print("Supplier bills:")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", suppl_bills_go_enc[supplier])

    print()
    total_supp_keep = 0
    total_pot = 0
    for i, supplier in enumerate(suppl_list):
        sum1 = 0
        for user in supplier.get_users():
            sum1 += sum(user_bills_go_enc[user])
        supp_keep = sum([sum(x) for x in suppl_bills_go_enc[supplier]])
        total_supp_keep += supp_keep
        total_pot += (-sum1 - supp_keep) 
        print("Supplier ", i ," gets from users ", -sum1, " and needs to keep ", supp_keep, " so it puts ", -sum1 - supp_keep," in the pot")
    print("\nSuppliers keep ", total_supp_keep, " from the users")
    print("Pot after trading period: ", total_pot, " (should be 0)")

print_results([0,0,0,1])
decryption_time = time.time()
print()
print("Payload encryption time: , ", payload_time - start_time)
print("Algorithm time: , ", settlement_time - payload_time)
print("Decryption time: , ", decryption_time - settlement_time)

