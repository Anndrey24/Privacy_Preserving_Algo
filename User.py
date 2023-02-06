from phe import paillier

class User:

    public_key, private_key = paillier.generate_paillier_keypair()
    bid = 0
    isBidAccepted = False
    payload = (0,0,0,0,0)

    def _init_(self, supplier):
        self.supplier = supplier
        pass

    def get_public_key(self):
        return self.public_key
    
    def get_bid(self):
        self.update_bid()
        return self.bid

    def set_accepted(self, accepted):
        self.isBidAccepted = accepted

    def get_payload(self):
        self.update_payload()
        return self.payload