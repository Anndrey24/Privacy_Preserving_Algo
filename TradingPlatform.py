from phe import paillier

class TradingPlatform:
    TP = RP = FiT = 0
    algorithm = 0
    grid_op = None
    users = []
    user_payloads = {}
    user_bills_s_enc = {}
    user_bills_go_enc = {}

    suppliers = []
    supplier_dict_s_enc = {}
    supplier_dict_go_enc = {}

    keylist = ["td", "tdd", "tsd", "td_down", "td_up", "t_c_over", "t_c_under", "p2p_c_over", "p2p_c_under", 
        "t_p_over", "t_p_under", "p2p_p_over", "p2p_p_under", "p2p_c_n", "p2p_p_n", 
        "c_n", "p_n", "t_p_sup"]
    agg = {}

    def __init__(self, algorithm, TP, RP, FiT, user_list, supplier_list, grid_op):
        self.algorithm = algorithm
        self.TP = TP
        self.RP = RP
        self.FiT = FiT
        for user in user_list:
            self.add_user(user)
        for supplier in supplier_list:
            self.add_supplier(supplier)
        self.grid_op = grid_op

    def add_user(self, user):
        self.users.append(user)
        self.user_payloads[user] = []
        self.user_bills_s_enc[user] = []
        self.user_bills_go_enc[user] = []

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)
        self.supplier_dict_s_enc[supplier] = []
        self.supplier_dict_go_enc[supplier] = []
    
    def get_partial_bills(self, type = 's'):
        if type == 's':
           return self.user_bills_s_enc
        else:
            return self.user_bills_go_enc

    def get_supplier_bills(self, type = 's'):
        if type == 's':
            return self.supplier_dict_s_enc
        else:
            return self.supplier_dict_go_enc


    def calculate_partial_bills(self):
        for supplier in self.suppliers:
            self.supplier_dict_s_enc[supplier].append([])
            self.supplier_dict_go_enc[supplier].append([])

        if self.algorithm == 1:
            for user in self.users:
                payload = user.get_payload()
                self.user_payloads[user].append(payload)
                self.algo_1(user, payload)
        elif self.algorithm == 2:
            for user in self.users:
                payload = user.get_payload()
                self.user_payloads[user].append(payload)
                is_bid_accepted = payload[0]
                if is_bid_accepted:
                    self.algo_2(user, payload)
                else:
                    self.algo_1(user, payload)
        elif self.algorithm == 3:
            self.aggregate_values()
            self.get_decrypted_aggregates()
            print(self.agg)
            for user in self.users:
                payload = user.get_payload()
                self.user_payloads[user].append(payload)
                is_bid_accepted = payload[0]
                if is_bid_accepted:
                    self.algo_3(user, payload)
                else:
                    self.algo_1(user, payload)
        elif self.algorithm == 4:
            self.aggregate_values()
            self.get_decrypted_aggregates()
            print(self.agg)
            for user in self.users:
                payload = user.get_payload()
                self.user_payloads[user].append(payload)
                is_bid_accepted = payload[0]
                if is_bid_accepted:
                    self.algo_4(user, payload)
                else:
                    self.algo_1(user, payload)


    def algo_1(self, user, payload):
        bid_type = payload[1]
        consumption_type = payload[2]
        # Supplier key encrypted
        energy_amount_s_enc = payload[3] + payload[4]
        self.algo_1_calc(user, self.user_bills_s_enc, user.get_supplier(), self.supplier_dict_s_enc, 
                         bid_type, consumption_type, energy_amount_s_enc)
        # GridOp key encrypted
        energy_amount_go_enc = payload[5] + payload[6]
        self.algo_1_calc(user, self.user_bills_go_enc, user.get_supplier(), self.supplier_dict_go_enc, 
                         bid_type, consumption_type, energy_amount_go_enc)

    def algo_1_calc(self, user, user_bills, supplier, supplier_dict, bid_type, consumption_type, energy_amount):
        if consumption_type != bid_type:
            energy_amount *= -1

        # Net Buyer
        if consumption_type == 1:
            bill = energy_amount * self.RP
            supplier_dict[supplier][-1].append(bill)
            user_bills[user].append(bill * (-1))
        # Net Seller    
        else:
            reward = energy_amount * self.FiT
            supplier_dict[supplier][-1].append(reward * (-1))
            user_bills[user].append(reward)


    def algo_2(self, user, payload):
        _, bid_type, _, committed_value_s_enc, indiv_deviation_s_enc, committed_value_go_enc, indiv_deviation_go_enc, indiv_dev_sign = payload
        # Supplier key encrypted
        self.algo_2_calc(user, self.user_bills_s_enc, user.get_supplier(), self.supplier_dict_s_enc, 
                         bid_type, committed_value_s_enc, indiv_deviation_s_enc, indiv_dev_sign)
        # GridOp key encrypted
        self.algo_2_calc(user, self.user_bills_go_enc, user.get_supplier(), self.supplier_dict_go_enc, 
                         bid_type, committed_value_go_enc, indiv_deviation_go_enc, indiv_dev_sign)

    def algo_2_calc(self, user, user_bills, supplier, supplier_dict, bid_type, committed_value, indiv_deviation, indiv_dev_sign):
        bill = reward = supplier_balance = committed_value * 0

        if bid_type == 1:
            bought_from_P2P = committed_value * self.TP
            if indiv_dev_sign == 0:
                bill += bought_from_P2P
            elif indiv_dev_sign == -1: 
                sold_to_supplier = indiv_deviation * self.FiT
                bill += bought_from_P2P + sold_to_supplier
                supplier_balance += sold_to_supplier
            elif indiv_dev_sign == 1:
                bought_from_supplier = indiv_deviation * self.RP
                bill += bought_from_P2P + bought_from_supplier
                supplier_balance += bought_from_supplier
            user_bills[user].append(bill * (-1))
        else:
            sold_to_P2P = committed_value * self.TP
            if indiv_dev_sign == 0:
                reward += sold_to_P2P
            elif indiv_dev_sign == -1: 
                bought_from_supplier = indiv_deviation * self.RP
                reward += sold_to_P2P + bought_from_supplier
                supplier_balance += bought_from_supplier * (-1)
            elif indiv_dev_sign == 1:
                sold_to_supplier = indiv_deviation * self.FiT
                reward += sold_to_P2P + sold_to_supplier
                supplier_balance += sold_to_supplier * (-1)
            user_bills[user].append(reward)
        supplier_dict[supplier][-1].append(supplier_balance)


    def aggregate_values(self):
        self.agg = dict.fromkeys(self.keylist, 0) 
        for user in self.users:
            is_bid_accepted, bid_type, consumption_type, _, _, committed_value_go_enc, indiv_deviation_go_enc, indiv_dev_sign = user.get_payload()
            if is_bid_accepted:
                # Consumer
                if bid_type == 1:
                    self.agg["p2p_c_n"] += 1
                    self.agg["tdd"] += indiv_deviation_go_enc
                    # Over-consumed
                    if indiv_dev_sign == 1:
                        self.agg["t_c_over"] += indiv_deviation_go_enc
                        self.agg["p2p_c_over"] += 1
                    # Under-consumed
                    else:
                        self.agg["t_c_under"] -= indiv_deviation_go_enc
                        self.agg["p2p_c_under"] += 1

                # Prosumer
                else:
                    self.agg["p2p_p_n"] += 1
                    self.agg["tsd"] += indiv_deviation_go_enc
                    # Over-supplied
                    if indiv_dev_sign == 1:
                        self.agg["t_p_over"] += indiv_deviation_go_enc
                        self.agg["p2p_p_over"] += 1
                    # Under-supplied
                    else:
                        self.agg["t_p_under"] -= indiv_deviation_go_enc
                        self.agg["p2p_p_under"] += 1
            else:
                # Consumer
                if consumption_type == 1:
                    self.agg["c_n"] += 1
                # Prosumer
                else:
                    self.agg["p_n"] += 1
                    energy_amount = committed_value_go_enc + indiv_deviation_go_enc
                    if bid_type == 1:
                        energy_amount *= -1
                    self.agg["t_p_sup"] += energy_amount
        self.agg["td"]  = self.agg["tsd"] - self.agg["tdd"]
        self.agg["tdd"] = self.agg["t_c_over"] - self.agg["t_c_under"]
        self.agg["tsd"] = self.agg["t_p_over"] - self.agg["t_p_under"]
        self.agg["td_down"] = self.agg["t_c_over"] + self.agg["t_p_under"]
        self.agg["td_up"] = self.agg["t_p_over"] + self.agg["t_c_under"]


    def get_decrypted_aggregates(self):
        keylist = ["td", "tdd", "tsd", "td_down", "td_up", "t_c_over", "t_c_under", "t_p_over", "t_p_under", "t_p_sup"]
        for key in keylist:
            temp = self.agg[key]
            try:
                self.agg[key] = self.grid_op.decode(self.agg[key])
            except:
                self.agg[key] = temp
            
    def algo_3(self, user, payload):
        _, bid_type, _, committed_value_s_enc, indiv_deviation_s_enc, committed_value_go_enc, indiv_deviation_go_enc, indiv_dev_sign = payload
        # Supplier key encrypted
        self.algo_3_calc(user, self.user_bills_s_enc, user.get_supplier(), self.supplier_dict_s_enc, 
                         bid_type, committed_value_s_enc, indiv_deviation_s_enc, indiv_dev_sign)
        # GridOp key encrypted
        self.algo_3_calc(user, self.user_bills_go_enc, user.get_supplier(), self.supplier_dict_go_enc, 
                         bid_type, committed_value_go_enc, indiv_deviation_go_enc, indiv_dev_sign)
        
    def algo_3_calc(self, user, user_bills, supplier, supplier_dict, bid_type, committed_value, indiv_deviation, indiv_dev_sign):
        bill = reward = supplier_balance = committed_value * 0
        # Consumer
        if bid_type == 1:
            bought_from_P2P = committed_value * self.TP
            if self.agg["tdd"] == 0:
                bill += bought_from_P2P
            elif self.agg["tdd"] < 0:
                if indiv_dev_sign >= 0:
                    bill += bought_from_P2P + indiv_deviation * self.TP
                else:
                    sold_to_supplier = indiv_deviation * (1 - self.agg["t_c_over"] / self.agg["t_c_under"]) * self.FiT
                    bill += bought_from_P2P + (indiv_deviation * self.agg["t_c_over"] / self.agg["t_c_under"] * self.TP) + sold_to_supplier
                    supplier_balance += sold_to_supplier
            elif self.agg["tdd"] > 0:
                if indiv_dev_sign <= 0:
                    bill += bought_from_P2P + indiv_deviation * self.TP
                else:
                    bought_from_supplier = indiv_deviation * (1 - self.agg["t_c_under"] / self.agg["t_c_over"]) * self.RP
                    bill += bought_from_P2P + (indiv_deviation * self.agg["t_c_under"] / self.agg["t_c_over"] * self.TP) + bought_from_supplier
                    supplier_balance += bought_from_supplier
            user_bills[user].append(bill * (-1))
        # Prosumer
        else:
            sold_to_P2P = committed_value * self.TP
            if self.agg["tsd"] == 0:
                reward += sold_to_P2P
            elif self.agg["tsd"] < 0:
                if indiv_dev_sign >= 0:
                    reward += sold_to_P2P + indiv_deviation * self.TP
                else:
                    bought_from_supplier = indiv_deviation * (1 - self.agg["t_p_over"] / self.agg["t_p_under"]) * self.RP
                    reward += sold_to_P2P + (indiv_deviation * self.agg["t_p_over"] / self.agg["t_p_under"] * self.TP) + bought_from_supplier
                    supplier_balance += bought_from_supplier * (-1)
            elif self.agg["tsd"] > 0:
                if indiv_dev_sign <= 0:
                    reward += sold_to_P2P + indiv_deviation * self.TP
                else:
                    # sold_to_P2P = (committed_value + self.agg["t_p_under"] / self.agg["p2p_p_over"]) * self.TP
                    sold_to_supplier = indiv_deviation * (1 - self.agg["t_p_under"] / self.agg["t_p_over"]) * self.FiT
                    reward += sold_to_P2P + (indiv_deviation *  self.agg["t_p_under"] / self.agg["t_p_over"] * self.TP) + sold_to_supplier
                    supplier_balance += sold_to_supplier * (-1)
            user_bills[user].append(reward)
        supplier_dict[supplier][-1].append(supplier_balance)


    def algo_4(self, user, payload):
        _, bid_type, _, committed_value_s_enc, indiv_deviation_s_enc, committed_value_go_enc, indiv_deviation_go_enc, indiv_dev_sign = payload
        # Supplier key encrypted
        self.algo_4_calc(user, self.user_bills_s_enc, user.get_supplier(), self.supplier_dict_s_enc, 
                         bid_type, committed_value_s_enc, indiv_deviation_s_enc, indiv_dev_sign)
        # GridOp key encrypted
        self.algo_4_calc(user, self.user_bills_go_enc, user.get_supplier(), self.supplier_dict_go_enc, 
                         bid_type, committed_value_go_enc, indiv_deviation_go_enc, indiv_dev_sign)
        
    def algo_4_calc(self, user, user_bills, supplier, supplier_dict, bid_type, committed_value, indiv_deviation, indiv_dev_sign):
        bill = reward  = supplier_balance = committed_value * 0
        # Consumer
        if bid_type == 1:
            bought_from_P2P = committed_value * self.TP
            if self.agg["td"] == 0:
                bill += bought_from_P2P
            elif self.agg["td"] < 0:
                if indiv_dev_sign <= 0:
                    bill += bought_from_P2P + indiv_deviation * self.TP
                else:
                    bought_from_supplier = indiv_deviation * (1 - self.agg["td_up"] / self.agg["td_down"]) * self.RP
                    bill += bought_from_P2P + (indiv_deviation * self.agg["td_up"] / self.agg["td_down"] * self.TP) + bought_from_supplier
                    supplier_balance += bought_from_supplier
            elif self.agg["td"] > 0:
                if indiv_dev_sign >= 0:
                    bill += bought_from_P2P + indiv_deviation * self.TP
                else:
                    sold_to_supplier = indiv_deviation * (1 - self.agg["td_down"] / self.agg["td_up"]) * self.FiT
                    bill += bought_from_P2P + (indiv_deviation * self.agg["td_down"] / self.agg["td_up"] * self.TP) + sold_to_supplier
                    supplier_balance += sold_to_supplier
            user_bills[user].append(bill * (-1))
        # Prosumer
        else:
            sold_to_P2P = committed_value * self.TP
            if self.agg["td"] == 0:
                reward += sold_to_P2P
            elif self.agg["td"] < 0:
                if indiv_dev_sign >= 0:
                    reward += sold_to_P2P + indiv_deviation * self.TP
                else:
                    bought_from_supplier = indiv_deviation * (1 - self.agg["td_up"] / self.agg["td_down"]) * self.RP
                    reward += sold_to_P2P + (indiv_deviation * self.agg["td_up"] / self.agg["td_down"] * self.TP) + bought_from_supplier
                    supplier_balance += bought_from_supplier * (-1)
            elif self.agg["td"] > 0:
                if indiv_dev_sign <= 0:
                    reward += sold_to_P2P + indiv_deviation * self.TP
                else:
                    sold_to_supplier = indiv_deviation * (1 - self.agg["td_down"] / self.agg["td_up"]) * self.FiT
                    reward += sold_to_P2P + (indiv_deviation *  self.agg["td_down"] / self.agg["td_up"] * self.TP) + sold_to_supplier
                    supplier_balance += sold_to_supplier * (-1)
            user_bills[user].append(reward)
        supplier_dict[supplier][-1].append(supplier_balance)

        # # Consumer
        # if bid_type == 1:
        #     bought_from_P2P = committed_value * self.TP
        #     if self.agg["td"] == 0:
        #         bill += bought_from_P2P
        #     elif self.agg["td"] < 0:
        #         if indiv_dev_sign <= 0:
        #             bill += bought_from_P2P
        #         else:
        #             # bought_from_P2P = (committed_value - self.agg["td"] / self.agg["p2p_c_n"]) * self.TP # Remove
        #             bought_from_supplier = (-self.agg["td"] / self.agg["p2p_c_over"]) * self.RP
        #             bill += bought_from_P2P + bought_from_supplier
        #             supplier_balance += bought_from_supplier
        #     elif self.agg["td"] > 0:
        #         bill += bought_from_P2P
        #     user_bills[user].append(bill * (-1))
        # # Prosumer
        # else:
        #     sold_to_P2P = committed_value * self.TP
        #     if self.agg["td"] == 0:
        #         reward += sold_to_P2P
        #     elif self.agg["td"] < 0:
        #         reward += sold_to_P2P
        #     elif self.agg["td"] > 0:
        #         if indiv_dev_sign <= 0:
        #             reward += sold_to_P2P
        #         else:
        #             # sold_to_P2P = (committed_value - self.agg["td"] / self.agg["p2p_p_n"]) * self.TP # Remove
        #             sold_to_supplier = (self.agg["td"] / self.agg["p2p_p_over"]) * self.FiT
        #             reward += sold_to_P2P + sold_to_supplier
        #             supplier_balance += sold_to_supplier * (-1)
        #     user_bills[user].append(reward)
        # supplier_dict[supplier][-1].append(supplier_balance)