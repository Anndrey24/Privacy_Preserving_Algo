from phe import paillier

class TradingPlatform:
    userCount = 0
    users = []
    user_volumes = {}
    user_bills = {}
    suppliers = []
    supplier_dict = {}

    def __init__(self, TP, RP, FiT, user_list, supplier_list):
        self.TP = TP
        self.RP = RP
        self.FiT = FiT
        for user in user_list:
            self.add_user(user)
        for supplier in supplier_list:
            self.add_supplier(supplier)

    def add_user(self, user):
        self.users.append(user)
        self.user_volumes[user] = []
        self.user_bills[user] = []

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)
        self.supplier_dict[supplier] = []
    
    def get_partial_bills(self):
        return self.user_bills

    def get_supplier_bills(self):
        return self.supplier_dict

    def calculate_partial_bills(self, algorithm = 1):
        for supplier in self.suppliers:
            self.supplier_dict[supplier].append([])

        if algorithm == 1:
            self.algo_1()


    def algo_1(self):
        for user in self.users:
            payload = user.get_payload()
            supplier = user.get_supplier()
            isNetBuyer = payload[0]
            electricity_amount = payload[1] + payload[2]
            self.user_volumes[user].append([isNetBuyer, payload[1], payload[2]])

            if isNetBuyer == 1:
                bill = electricity_amount * self.RP
                self.supplier_dict[supplier][-1].append(bill)
                self.user_bills[user].append(bill * (-1))
            else:
                reward = electricity_amount * self.FiT
                self.supplier_dict[supplier][-1].append(reward * (-1))
                self.user_bills[user].append(reward)
