from phe import paillier

class TradingPlatform:
    userCount = 0
    users = []
    user_volumes = {}
    user_bills = {}
    suppliers = []
    supplier_dict = {}

    def __init__(self, algorithm, TP, RP, FiT, user_list, supplier_list):
        self.algorithm = algorithm
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

    def calculate_partial_bills(self):
        for supplier in self.suppliers:
            self.supplier_dict[supplier].append([])

        if self.algorithm == 1:
            for user in self.users:
                payload = user.get_payload()
                supplier = user.get_supplier()
                self.algo_1(user, payload, supplier)

        elif self.algorithm == 2:
            for user in self.users:
                payload = user.get_payload()
                supplier = user.get_supplier()
                bid_type = payload[0]
                # Bid rejected
                if bid_type == 0:
                    self.algo_1(user, payload, supplier)
                # Bid accepted
                else:
                    self.algo_2(user, payload, supplier)


    def algo_1(self, user, payload, supplier):
        bid_type = payload[0]
        consumption_type = payload[1]
        electricity_amount = payload[2] + payload[3]
        self.user_volumes[user].append(payload)

        if consumption_type != bid_type:
            electricity_amount *= -1

        # Net Buyer
        if consumption_type == 1:
            bill = electricity_amount * self.RP
            self.supplier_dict[supplier][-1].append(bill)
            self.user_bills[user].append(bill * (-1))
        # Net Seller    
        else:
            reward = electricity_amount * self.FiT
            self.supplier_dict[supplier][-1].append(reward * (-1))
            self.user_bills[user].append(reward)
            
    def algo_2(self, user, payload, supplier):
        payload = user.get_payload()
        supplier = user.get_supplier()
        bid_type, consumption_type, committed_value, indiv_deviation, indiv_dev_sign = payload
        self.user_volumes[user].append(payload)
        bill = reward = supplier_balance = 0

        if bid_type == 1:
            bought_from_P2P = committed_value * self.TP
            if indiv_dev_sign == 0:
                bill = bought_from_P2P
            elif indiv_dev_sign == -1: 
                sold_to_supplier = indiv_deviation * self.FiT
                bill = bought_from_P2P + sold_to_supplier
                supplier_balance = sold_to_supplier
            elif indiv_dev_sign == 1:
                bought_from_supplier = indiv_deviation * self.RP
                bill = bought_from_P2P + bought_from_supplier
                supplier_balance = bought_from_supplier
            self.user_bills[user].append(bill * (-1))
        else:
            sold_to_P2P = committed_value * self.TP
            if indiv_dev_sign == 0:
                reward = sold_to_P2P
            elif indiv_dev_sign == -1: 
                bought_from_supplier = indiv_deviation * self.RP
                reward = sold_to_P2P + bought_from_supplier
                supplier_balance = bought_from_supplier * (-1)
            elif indiv_dev_sign == 1:
                sold_to_supplier = indiv_deviation * self.FiT
                reward = sold_to_P2P + sold_to_supplier
                supplier_balance = sold_to_supplier * (-1)
            self.user_bills[user].append(reward)
        self.supplier_dict[supplier][-1].append(supplier_balance)