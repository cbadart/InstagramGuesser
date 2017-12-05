bad_users = set()

for line in open('warnings.txt'):
	if line.startswith("PHP Warning:"):
		data = line.split(':')
		url = data[2]
		user = url.split('/')[-1]
		# remove extra parenthesis from ends
		user = user[:-1]
		# print(user)
		bad_users.add(user)
	else:
		continue

# remove bad users from cleaned data
f = open("cleaned_users.txt","r")
lines = f.readlines()
f.close()

f = open("cleaned_users.txt","w")
for line in lines:
	line = line.rstrip()
	if line not in bad_users:
		f.write(line + "\n")