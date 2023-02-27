"""All network functions."""
import datetime
import time
import socket
import typing

import icmplib

from contextlib import closing


def port_is_opened(host: str, port: int):
    """Checks if port is opened

    Port considered to be opened if it's responded in 15 seconds, otherwise it's
    considered to be closed.
    """
    with closing(socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)) as sock:  # type: socket.socket
        try:
            sock.settimeout(15)
            t1 = time.time() * 1000
            sock.connect((host, port))
            t2 = time.time() * 1000
            return True, t2 - t1
        except (
                TimeoutError,
                socket.gaierror,
                OverflowError,
                ConnectionRefusedError,
                OSError
        ):
            return False, 0


def http_is_opened(host: str, port: int):
    """Checks if port is opened and accepts HTTP requests.

    Port considered to be opened if it's responded in 15 seconds, otherwise it's
    considered to be closed.
    This function send VERY SIMPLE Http Request header. If we don't send it,
    most of HTTP and HTTPS servers will not respond.
    (but will accept connection)
    RTT is calculated like time between first byte sent and first byte received.
    Note: server it is considered to be alive ONLY if it responds to simple
    HTTP header. If it's accept socket connection but don't respond anything,
    when server and port considered to closed.

    """

    with closing(socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)) as sock:  # type: socket.socket
        try:
            sock.settimeout(15)
            sock.connect((host, port))
            res = b'GET / HTTP/1.0 \r\n\r\n'
            t1 = time.time() * 1000
            sock.sendall(res)
            sock.recv(1)
            t2 = time.time() * 1000
            return True, t2 - t1
        except (
                TimeoutError,
                socket.gaierror,
                OverflowError,
                ConnectionRefusedError,
                OSError
        ):
            return False, 0


def get_ips_from_hostname(hostname: str):
    """Returns ip addresses of hostname.

    Can resolve only IPv4 addresses, but it's all we need

    Args:
        hostname (str): hostname to check. no protocol needed. e.g. ya.ru
    """
    try:
        return socket.gethostbyname_ex(hostname)[-1]
    except socket.gaierror:
        return []


class CheckResult(typing.TypedDict):
    """Type definition for `check` function result. (for IDE code completion)"""
    time: datetime.datetime
    host: str
    ip: str | None
    rtt: float
    port: int | None
    status: int | None


def check(host: str, ports: list[int], **_) -> \
        typing.Generator[CheckResult, None, None]:
    """Main check for host availability

    Checks all resolved ips. This function works like generator, for app not
    look-like it's stopped. For example: we have 10 ips and every of them need
    2 seconds to check. it's 20 seconds without any output. So I fixed it by
    using generator.

    Status codes:
    0 - Closed for connections
    1 - Opened for connections
    None - not sure (if no ports provided, and ping result is ok).


    Args:
        host (str): hostname or ip address to check.
        ports (list[int]): list of ports to check on provided host.

    Returns:
        Generator[CheckResult, None, None): list of check results for
          all resolved ip/port pairs

    """
    ip_addresses = get_ips_from_hostname(host)
    if not ip_addresses:
        for port in ports:
            yield {
                'time': datetime.datetime.now(),
                'host': host,
                'ip': None,
                'rtt': 0,
                'port': port,
                'status': 0
            }

    for ip_address in ip_addresses:
        if not ports:
            ping_result = icmplib.ping(ip_address, count=3)
            yield {
                'time': datetime.datetime.now(),
                'host': host,
                'ip': ip_address,
                'rtt': ping_result.avg_rtt,
                'port': None,
                'status': None if ping_result.is_alive else 0
            }
            continue
        for port in ports:
            opened, rtt = port_is_opened(host, port)
            yield {
                'time': datetime.datetime.now(),
                'host': host,
                'ip': ip_address,
                'rtt': rtt,
                'port': port,
                'status': int(opened)
            }


if __name__ == '__main__':
    pass
    # SOME PREVIOUS TESTS
    # pprint.pprint(check('122.144.111.44', [80]))
    # print(get_ips_from_hostname('0.0.0.0'))
