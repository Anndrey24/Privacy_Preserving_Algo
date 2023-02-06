from phe import paillier

class TradingPlatform:
    userCount = 0
    users = []
    userBids = []
    suppliers = []

    def _init_(self, TP, RP, FiT):
        self.TP = TP
        self.RP = RP
        self.FiT = FiT

    def add_user(self, user):
        self.userCount += 1
        self.users[self.userCount] = user
        self.userBids[self.userCount] = 0
        return self.userCount
    
    def calculate_bills(self):
        pass

    def algo_1(self, isNetBuyer, amount):
        return
