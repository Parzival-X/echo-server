import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for our server
    HOST = '127.0.0.1'
    PORT = 10000

    address = (HOST, PORT)

    # Instantiates a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # Flag tells the kernel to reuse a local socket in TIME_WAIT state,
    # without waiting for its natural timeout to expire.
    # https://docs.python.org/3/library/socket.html#example
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Binding the socket to the address above and
    # begin to listen for incoming connections
    sock.bind(address)
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:

                    data = conn.recv(16)

                    if not data:
                        break
                    else:
                        print('received "{0}"'.format(data.decode('utf8')))
                        conn.sendall(data)
                        print('sent "{0}"'.format(data.decode('utf8')))

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:

                #  close the socket you created above when a client connected.
                print(
                    'echo complete, client connection closed', file=log_buffer
                )
                conn.close()

    except KeyboardInterrupt:
        # Close the server socket and exit from the server function.
        sock.close()
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
