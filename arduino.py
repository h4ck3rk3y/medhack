import serial
ser = serial.Serial("/dev/ttyACM0", 9600)

import socket

# Loneliness

def send_message(message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ip='192.168.43.132'
	port = 8081
	BUFFER_SIZE = 1024
	sock.connect((ip, port))
	sock.send(message)
	sock.close()

def parse_input():

	current_word = []

	entire_message = []

	abvs = {'btw': 'BY THE WAY', 'hhu': 'HI HOW ARE YOU? ', 'afaik': 'AS FAR AS I KNOW',
			'pot': 'POINT OF VIEW', 'ge': 'GOOD EVERNING', 'ind': 'INDIA', 'gn': 'GOOD NIGHT',
			'gm': 'GOOD MORNING',
			'txt': 'TEXT', 'ie': 'THAT IS', 'brb': 'BE RIGHT BACK', 'cu': 'SEE YOU', 'grt': 'GREAT', 'thnx': 'THANKS', 'lol': 'LAUGHING OUT LOUD', '2': 'TO', '4': 'FOR', 'msg': 'MESSAGE', 'omg': 'OH MY GOD!!', 'asap': 'AS SOON AS POSSIBLE', 'plz': 'PLEASE', 'np': 'NO PROBLEM', '2moro': 'TOMMOROW', 'thku': 'THANK YOU', 'c': 'SEE', 'k': 'OK', 'coz': 'BECAUSE', 'sos': 'SAVE OUR SOULS',
			'bcc': 'BRING ME A CUP OF COFFEE',
			'idk': "I DON'T KNOW", 'y': 'WHY', 'ot': 'OUT OF CONTEXT', 'ily': ' I LOVE YOU'}

	while True:
		data = ser.readline().strip()


		if data == "its a dit":
			current_word.append("0")
		elif data == "its a dash":
			current_word.append("1")

		print current_word

		if len(current_word) == 5:
			number = int(''.join(current_word), 2)

			if not number:
				# @ToDo Send Message to Rocky
				message = ''.join(entire_message)
				if message.strip() in abvs:
					message = abvs[message.strip()].lower()
					message = message[0].upper() + message[1:]
					print message
				else:
					print 'Entire Message: %s' %(message)

				send_message(message)
				entire_message = []
				current_word = []
				continue
			elif number < 26:
				message = chr(ord('a') + number - 1)
				print 'Character: %s' %(message)
			elif number == 27:
				message = " "
			elif number == 28:
				# @ToDO Gyani independent sendall this asap
				message = "change_mode"
				current_word = []
				data = s.recv(BUFFER_SIZE)
				send_message(message)
				continue
			elif number == 29:
				# @ToDO independent sendall
				message = "this_is_an_sos"
				send_message(message)
				current_word = []
				continue

			entire_message.append(message)
			current_word = []



parse_input()