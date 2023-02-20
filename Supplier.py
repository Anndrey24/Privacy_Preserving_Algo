from phe import paillier

class Supplier:

    public_key, private_key = paillier.generate_paillier_keypair()

    def __init__(self, name, grip_op):
        self.name = name
        self.grid_op = grip_op

    def get_grid_op(self):
        return self.grid_op

    def get_public_key(self):
        return self.public_key
    
    def decode(self, x):
        return self.private_key.decrypt(x)
