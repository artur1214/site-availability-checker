"""Some useful functions"""
import re


def is_hostname(hostname: str):
    """Is provided string is hostname"""
    if len(hostname) > 255 or not len(hostname):
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile(r'(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def is_ip(ip: str):
    """Is provided string is ip"""
    return bool(re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$').match(ip))


def check_host(host: str):
    """Checks if provided `host` is valid hostname or ip address"""
    return isinstance(host, str) and (is_hostname(host) or is_ip(host))
