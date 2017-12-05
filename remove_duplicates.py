users_set = set()

for line in open('users.txt'):
	user = line.rstrip()
	users_set.add(user)
	
for user in users_set:
	print(user)

