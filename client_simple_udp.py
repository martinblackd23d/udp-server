import socket
import sys
import hashlib
import time
import datetime

def main():
	# get arguments
	if len(sys.argv) != 4:
		print('Usage: python3 client_simple_udp.py <server_ip> <port_num> <"Test text"|test_file.txt>')
		sys.exit()
	host = sys.argv[1]
	port = int(sys.argv[2])
	message = sys.argv[3]

	# check arguments
	if port < 1 or port > 65535:
		print('Port number must be in range 1-65535')
		sys.exit()
	try:
		with open(message, 'r', encoding='utf-8') as file:
			message = file.read()
	except FileNotFoundError:
		pass

	# create checksum
	checksum = hashlib.md5(message.encode()).hexdigest()

	# send message
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		time_sent = time.time()
		# create message with checksum
		message = checksum + ' ' + message
		client_socket.sendto(message.encode(), (host, port))
	except socket.gaierror:
		print('Invalid address')
		sys.exit()
	#except socket.error:
		print('Failed to create socket')
		sys.exit()
	print(f'checksum sent: {checksum}')

	# receive response
	client_socket.settimeout(1)
	try:
		response, address = client_socket.recvfrom(1024)
		time_received = time.time()
		time.strptime(response.decode(), '%Y-%m-%d %H:%M:%S.%f')
		print(f'server has successfully received the message at {response.decode()}')

		print(f'RTT: {int((time_received - time_sent) * 1000000)}us')
	except ValueError:
		print('Invalid response')
	except socket.timeout:
		print('Response timed out')
	print()

if __name__ == '__main__':
	main()
