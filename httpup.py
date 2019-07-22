import socket
import sys
import argparse
from contextlib import closing


class Sock:
    def __init__(self, args):
        self.no_error = True if args.noerror else False
        self.host = args.host
        self.input_ports = args.p
        self.ports = self.get_ports()
        self.timeout = args.t if args.t else 0.5
        self.is_valid_addr = True
        self.ip = self.get_ip()

    def get_ip(self):
        try:
            return socket.gethostbyname(self.host)
        except socket.gaierror as e:
            self.is_valid_addr = False
            if self.no_error:
                return False
            else:
                print("Invalid Host")
                exit(255)

    def get_ports(self):
        try:
            port = int(self.input_ports)
            return [port]
        except ValueError:
            pass
        if '-' in self.input_ports:
            ports = self.input_ports.split('-')
            ports = [int(i) for i in ports]
            ports.sort()
            if len(ports) != 2 or ports[1] > 65535:
                if self.no_error:
                    return None
                else:
                    print("Range can only include two integers between 1 and 65535")
                    exit(255)
            ports = list(range(ports[0], ports[1] + 1))
            return ports
        elif ',' in self.input_ports:
            ports = self.input_ports.split(',')
            ports = list(filter(None, ports))
            ports = [int(i) for i in ports]
            ports.sort()
            ports = list(filter(lambda a: a < 65535, ports))
            ports = list(filter(lambda a: a > 0, ports))
            return ports
        return None


class Tcp(Sock):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        if not self.is_valid_addr:
            return False
        for port in self.ports:
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                sock.settimeout(self.timeout)
                conn = sock.connect_ex((self.ip, port))
                if not conn:
                    return True
        return 1


def arguments():
    p = argparse.ArgumentParser(prog=sys.argv[0])
    p.add_argument('host', type=str)
    p.add_argument('-p', type=str, help='Ports to check. Ex: -p 80 443 445')
    p.add_argument('-t', type=float, help='Timeout')
    p.add_argument('--no-error', dest='noerror', action='store_true', help="Return false and don't fail out")
    p.set_defaults(noerror=False)
    return p.parse_args()


def main():
    a = arguments()
    scan = Tcp(a)
    val = scan.run()
    exit(val)


if __name__ == "__main__":
    main()
