import socket
import base64
import multiprocessing
import sys

class AlphaClient():

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # findef

    def connect(self, host, port):
        self.socket.connect((host, port))
    # findef

    def send_msg(self,msg=""):
        tmp = ("txtxtx" + str(len(msg)).rjust(6, "0") + msg + "rxrxrx").encode()
        self.socket.sendall(base64.b64encode(tmp))
    # findef

    def recv_msg(self, msg=""):
        return self.socket.recv(1024)

    # findef

    def close(self):
        self.socket.close()
    # findef

    def __del__(self):
        self.socket.close()
    # findef

# finclass


def work(i, h, p):
    s = AlphaClient()
    s.connect(h, p)

    msg = '-' * 79 + "\n"
    msg = msg + "nb messages : " + str(i) + "\n"
    msg = msg + '-' * 79 + "\n"
    #msg = msg + """"When using the loopback interface (IPv4 address 127.0.0.1 or IPv6 address ::1), data never leaves the host or touches the external network. In the diagram above, the loopback interface is contained inside the host. This represents the internal nature of the loopback interface and that connections and data that transit it are local to the host. This is why you’ll also hear the loopback interface and IP address 127.0.0.1 or ::1 referred to as “localhost.”
    #
    #    # Applications use the loopback interface to communicate with other processes running on the host and for security and isolation from the external network. Since it’s internal and accessible only from within the host, it’s not exposed.
    #
    #    # You can see this in action if you have an application server that uses its own private database. If it’s not a database used by other servers, it’s probably configured to listen for connections on the loopback interface only. If this is the case, other hosts on the network can’t connect to it.
    #
    #    # When you use an IP address other than 127.0.0.1 or ::1 in your applications, it’s probably bound to an Ethernet interface that’s connected to an external network. This is your gateway to other hosts outside of your “localhost” kingdom:"""

    msg = msg + "toto fait du vélo"

    s.send_msg(msg)
    s.close()
# findef


def main():
    HOST = '192.168.1.9'  # The server's hostname or IP address
    PORT = 8000  # The port used by the server

    for i in range(1000000000000000000):
        with multiprocessing.Pool(5) as p:
            p.apply_async(work, (i, HOST, PORT))

            #f = p.apply_async(work, (i, ))
            #while not f.ready():
            #    sys.stdout.flush()
            #    f.wait(0.1)
        # finpour
# findef

if __name__ == "__main__": main()