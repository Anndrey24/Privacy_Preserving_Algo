from phe import paillier

class Supplier:

    def __init__(self, name, grid_op):
        self.public_key, self.private_key = paillier.generate_paillier_keypair()
        self.user_list = []
        self.name = name
        self.grid_op = grid_op

    def get_grid_op(self):
        return self.grid_op

    def get_public_key(self):
        return self.public_key
    
    def decode(self, x):
        return self.private_key.decrypt(x)
    
    def add_user(self, user):
        self.user_list.append(user)

    def get_users(self):
        return self.user_list
    
    def get_name(self):
        return self.name
