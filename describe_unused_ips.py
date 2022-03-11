import sys
import boto3
import ipaddress
from typing import List

USAGE = """
**USAGE**
python describe_unused_ips.py {subnet-id} [lb]
"""

ec2_client = boto3.client("ec2")


def main(subnet_id: str, mode: str):
    print(f"{subnet_id=} {mode=}")

    # get cidr ips
    cidr = get_cidr(subnet_id=subnet_id)
    cidr_ips = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
    cidr_ips.sort(key=ipaddress.IPv4Address)

    # extract reserved ips
    #  The first four IP addresses and the last IP address in each subnet CIDR block
    #  are not available for you to use, and cannot be assigned to an instance.
    reserved_ips = cidr_ips[0:4] + [cidr_ips[-1]]
    reserved_ips.sort(key=ipaddress.IPv4Address)

    # get used ips
    used_ips = get_used_ips(subnet_id=subnet_id)
    used_ips.sort(key=ipaddress.IPv4Address)

    # extract unused ips
    unused_ips = list(set(cidr_ips) - set(used_ips) - set(reserved_ips))
    unused_ips.sort(key=ipaddress.IPv4Address)

    # output
    print(f"{cidr=}")
    print_list("cidr_ips", cidr_ips, mode)
    print("-----------")
    print_list("reserved_ips", reserved_ips, mode)
    print("-----------")
    print_list("used_ips", used_ips, mode)
    print("-----------")
    print_list("unused_ips", unused_ips, mode)
    print("-----------")
    print("cidr={} cidr_ips={} reserved={} used={} unused={}".format(
        cidr,
        len(cidr_ips), len(reserved_ips), len(used_ips), len(unused_ips)
    ))


def print_list(label: str, target_list: List, mode: str):
    if mode == "lb":
        print(f"{label}=")
        for t in target_list:
            print(f"{t}")
    else:
        print(f"{label}={target_list}")


def get_cidr(subnet_id: str) -> str:
    """
    Get Subnet CIDR
    :param subnet_id:VPC subnet-id
    :return: The IPv4 CIDR block
    """
    paginator = ec2_client.get_paginator('describe_subnets')
    for subnets in paginator.paginate(SubnetIds=[subnet_id]):
        for subnet in subnets["Subnets"]:
            return subnet['CidrBlock']
    raise Exception(f"{subnet_id=} has no CidrBlock.")


def get_used_ips(subnet_id: str) -> List[str]:
    """
    Get used ips from NetworkInterfaces(primary and secondary private IP address)
    :param subnet_id:
    :return: [IP address, ...]
    """
    private_ips = []
    paginator = ec2_client.get_paginator('describe_network_interfaces')
    for nw_ifs in paginator.paginate(
            Filters=[{'Name': 'subnet-id', 'Values': [subnet_id]}, ]
    ):
        for nw_if in nw_ifs["NetworkInterfaces"]:
            ips = [ip["PrivateIpAddress"] for ip in nw_if['PrivateIpAddresses']]
            private_ips.extend(ips)
    return private_ips


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        main(subnet_id=args[1], mode="normal")
        sys.exit(0)
    elif len(args) == 3:
        main(subnet_id=args[1], mode=args[2])
        sys.exit(0)
    else:
        print("incorrect argument")
        print(USAGE)
        sys.exit(1)
