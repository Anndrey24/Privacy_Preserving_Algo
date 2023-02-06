from Supplier import Supplier
from User import User
from TradingPlatform import TradingPlatform

suppl1 = Supplier("1")
suppl2 = Supplier("2")

user1 = User(suppl1)
user2 = User(suppl1)
user3 = User(suppl2)
user4 = User(suppl2)

user_list = [user1, user2, user3, user4]
suppl_list = [suppl1, suppl2]
payload_list = [(1, 5, 2, 0), (1,7,7,0), (-1,9,1,0), (1, -1, 4, 0)]
for user in user_list:
    user.update_payload(payload_list.pop(0))

trade_plat = TradingPlatform(TP = 1, RP = 1, FiT = 1, user_list = user_list, supplier_list = [suppl1,suppl2])
trade_plat.calculate_partial_bills()
# trade_plat.calculate_partial_bills()

user_bills = trade_plat.get_partial_bills()
suppl_bills = trade_plat.get_supplier_bills()
print("ENCRYPTED")
print("User bills: ",  user_bills)
print("Supplier bills: ",  suppl_bills)

for user in user_list[:2]:
    user_bills[user] = [suppl1.decode(x) for x in user_bills[user]]

for user in user_list[2:]:
    user_bills[user] = [suppl2.decode(x) for x in user_bills[user]]

for supplier in suppl_list:
    for i in range(len(suppl_bills[supplier])):
        suppl_bills[supplier][i] = [supplier.decode(x) for x in suppl_bills[supplier][i]]
print("DECRYPTED")
print("User bills: ", user_bills)
print("Supplier bills: ", suppl_bills)

