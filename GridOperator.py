from phe import paillier

class GridOperator:

    public_key, private_key = paillier.generate_paillier_keypair()

    def get_public_key(self):
        return self.public_key
    
    def decode(self, x):
        return self.private_key.decrypt(x)

