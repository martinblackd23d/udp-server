import socket
import sys
import hashlib
import datetime

def main():
	# get arguments
	if len(sys.argv) != 2:
		print('Usage: python3 server_simple_udp.py <port_num>')
		sys.exit()
	port = int(sys.argv[1])
	if port < 1 or port > 65535:
		print('Port number must be in range 1-65535')
		sys.exit()

	# create socket
	try:
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_socket.bind(('', port))
	except socket.error:
		print('Failed to create socket')
		sys.exit()

	while True:
		print('Waiting ...')

		# receive message
		message, address = server_socket.recvfrom(65535)
		time_received = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
		checksum, message = message.decode(encoding='utf-8').split(' ', 1)
		print('*** new message ***')
		print(f'Received time: {time_received}')
		print(f'Received message:\n{message}')
		print(f'Received checksum: {checksum}')

		# verify checksum
		checksum_calculated = hashlib.md5(message.encode()).hexdigest()
		print(f'Calculated checksum: {checksum_calculated}')
		if checksum == checksum_calculated:
			response = f'{time_received}'
		else:
			print('Checksum error')
			response = '0'

		# send response
		server_socket.sendto(response.encode(), address)
		print()

if __name__ == '__main__':
	main()