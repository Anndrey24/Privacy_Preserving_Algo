from phe import paillier
from phe.paillier import EncryptedNumber
from Supplier import Supplier
from User import User
from TradingPlatform import TradingPlatform
from GridOperator import GridOperator
import time


grid_op = GridOperator()

suppl1 = Supplier("1", grid_op)
suppl2 = Supplier("2", grid_op)

user1 = User(suppl1)
user2 = User(suppl1)
user3 = User(suppl2)
user4 = User(suppl2)

user_list = [user1, user2, user3, user4]
suppl_list = [suppl1, suppl2]
payload_list = [(1, 1,3,-2), (1, 1,3,1), (1, 1,3,3), (1, -1,9,0)]

start_time = time.time()
for user in user_list:
    user.update_payload(payload_list.pop(0))
payload_time = time.time()
trade_plat = TradingPlatform(algorithm = 3, TP = 0.75, RP = 1, FiT = 0.5, user_list = user_list, supplier_list = suppl_list, grid_op = grid_op)
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
            print("User ", i, ": ", [x.ciphertext()%100 for x in user_bills_s_enc[user]])
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
            print("User ", i, ": ", user_bills_s_enc[user])
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
            print("User ", i, ": ", [x.ciphertext()%100 for x in user_bills_go_enc[user]])
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
            print("User ", i, ": ", user_bills_go_enc[user])
        print("Supplier bills:")
        for i, supplier in enumerate(suppl_list):
            print("Supplier ", i, ": ", suppl_bills_go_enc[supplier])

print_results([0,1,0,1])
decryption_time = time.time()
print()
print("Payload encryption time: , ", payload_time - start_time)
print("Algorithm time: , ", settlement_time - payload_time)
print("Decryption time: , ", decryption_time - settlement_time)