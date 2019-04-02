import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):

    HOST = '127.0.0.1'
    PORT = 10000

    server_address = (HOST, PORT)

    # Instantiate a TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    # Connect your socket to the server
    sock.connect(server_address)

    # Cariable to accumulate the entire message received back from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        # TODO: send your message to the server here.
        sock.sendall(msg.encode('utf-8'))

        while True:
            chunk = sock.recv(16)
            received_message += chunk.decode('utf8')

            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)

            if len(received_message) == len(msg):
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        # TODO: after you break out of the loop receiving echoed chunks from
        #       the server you will want to close your client socket.
        print('closing socket', file=log_buffer)
        sock.close()

        # Return the entire reply you received from the server
        # as the return value of this function.
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
