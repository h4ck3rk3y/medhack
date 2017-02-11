import serial
ser = serial.Serial("/dev/ttyACM0", 9600)

ip = ''

def parse_input():

	current_word = []
	while True:
		data = ser.readline().strip()


		if data == "its a dit":
			current_word.append("0")
		elif data == "its a dash":
			current_word.append("1")

		print current_word

		if len(current_word) == 5:
			message = ""
			number = int(''.join(current_word), 2)

			if not number:
				message = "stop"
			else:
				message = chr(ord('a') + number - 1)

			print message
			current_word = []

parse_input()