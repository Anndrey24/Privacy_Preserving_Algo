import random

users = []
total_P2P = 0
for i in range(8):
   to_S = random.randint(-10, 10)
   to_P2P = random.randint(-5, 5)
   total_P2P += to_P2P
   users.append((to_S, to_P2P))
users.append((random.randint(-10, 10), -total_P2P))
print("Supplier: [(owed_to_supplier, owed_to_P2P),...], [(final_bill),...], Total needed: _ , Total received: _ , Delta: _")
print()
S1_need = sum(x[0] for x in users[:3])
S1_received = sum(sum(x) for x in users[:3])
print("S1: ", users[:3], ", ",[sum(x) for x in users[:3]],", Total needed: ", S1_need,", Total received: ", S1_received, ", Delta: ", S1_received - S1_need)
S2_need = sum(x[0] for x in users[3:6])
S2_received = sum(sum(x) for x in users[3:6])
print("S2: ", users[3:6], ", ",[sum(x) for x in users[3:6]],", Total needed: ", S2_need,", Total received: ", S2_received, ", Delta: ", S2_received - S2_need)
S3_need = sum(x[0] for x in users[6:])
S3_received = sum(sum(x) for x in users[6:])
print("S3: ", users[6:], ", ",[sum(x) for x in users[6:]],", Total needed: ", S3_need,", Total received: ", S3_received, ", Delta: ", S3_received - S3_need)
print()
if S1_need + S2_need + S3_need == S1_received + S2_received + S3_received:
    print(S1_need, "+", S2_need, "+", S3_need, "=", S1_received, "+", S2_received, "+", S3_received, "=", (S1_need + S2_need + S3_need))
