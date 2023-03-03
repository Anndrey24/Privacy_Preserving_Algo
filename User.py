from phe import paillier
from math import copysign

class User:
  
    # (is_bid_accepted, bid_type, consumption_type, committed_value_s_enc, indiv_deviation_s_enc, committed_value_go_enc, indiv_deviation_go_enc, indiv_dev_sign)
    # 1 => buy  /  -1 => sell

    def __init__(self, supplier):
        self.payload = (0,0,0,0,0,0,0)
        self.supplier = supplier
        supplier.add_user(self)

    def get_supplier(self):
        return self.supplier
    
    def get_bid(self):
        self.update_bid()
        return self.bid

    def set_accepted(self, accepted):
        self.isBidAccepted = accepted

    def get_payload(self):
        return self.payload

    def update_payload(self, payload_in):
        supplier_key = self.supplier.get_public_key()
        gridop_key = self.supplier.get_grid_op().get_public_key()

        is_bid_accepted = payload_in[0]
        bid_type = payload_in[1]
        committed = payload_in[2]
        ind_dev = payload_in[3]
        if ind_dev == 0:
            ind_dev_sign = 0
        else:
            ind_dev_sign = int(copysign(1,ind_dev))
        energy_amount = committed + ind_dev
        energy_amount_sign = int(copysign(1,energy_amount))
        consumption_type = energy_amount_sign * bid_type

        self.payload = (is_bid_accepted, bid_type, consumption_type,
                        supplier_key.encrypt(committed), supplier_key.encrypt(ind_dev),
                        gridop_key.encrypt(committed), gridop_key.encrypt(ind_dev),
                        ind_dev_sign)