#!/usr/bin/python3
"""
CIDR calculating functions

Note(s):
    1. Python 3.x
"""
import argparse
import ipaddress

class CIDR(object):
    """ A class to wrap up cidr calculations """
    def __init__(self, verbose=False):
        self.verbose = verbose

    def show(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    @staticmethod
    def _mask(bits):
        mask = 0
        for n in range(32):
            mask = (mask << 1) | (1 if n < bits else 0)
        return mask

    def cidr_subnets(self, iprange, sub_bits, offset=None):
        ''' return the list of subnet addresses within the cidr range '''
        cidr_address, cidr_prefix = iprange.split('/')
        cidr_prefix = int(cidr_prefix)
        cidr_bits = 32 - cidr_prefix
        cidr_size = 2 ** cidr_bits
        num_subs = 2 ** sub_bits
        sub_offset = int(cidr_size / num_subs)

        cidr_base = int(ipaddress.IPv4Address(cidr_address)) & CIDR._mask(cidr_prefix)
        sub_base = ipaddress.IPv4Address(cidr_base)
        subnets = [str(sub_base + (sub_offset * n)) for n in range(0, num_subs)]

        self.show("CIDR {} subnet /{} has {} subnets".format(iprange,
                                                             sub_bits,
                                                             len(subnets)))
        return subnets[offset] if offset else subnets

    def cidr_addresses(self, base, prefix):
        ''' return the list of addresses from the given base/prefix '''
        cidr = '/'.join([base, str(prefix)])
        exploded = [str(a) for a in ipaddress.IPv4Network(cidr)]
        self.show("Subnet {}/{} has {} addresses".format(base,
                                                         prefix,
                                                         len(exploded)))
        return exploded


def main(params):
    cidr = params['cidr']
    bits = params['bits']
    subnets = CIDR().cidr_subnets(cidr, bits)
    print("CIDR {} subnet /{}: ({} subnets)".format(cidr, bits, len(subnets)))
    if params['offset']:
        print("{}".format(subnets[params['offset']]))
    else:
        for sn in subnets:
            print("  {}".format(sn))


if __name__ == "__main__":
    """
    main entry: parse arguments and call main function
    """
    example_use = "example: cidr.py -o 192.168.50.10/28 -b 2"
    parser = argparse.ArgumentParser(allow_abbrev=True,
                                     epilog=example_use)
    parser.add_argument("-b", "--bits", type=int,
                        required=True,
                        help="subnet bits")
    parser.add_argument("-c", "--cidr",
                        required=True,
                        help="cidr block (ie: 192.168.10.80/28)")
    parser.add_argument("-o", "--offset", type=int,
                        help="subnet offset selector")

    args = parser.parse_args()
    params = {'cidr': args.cidr,
              'bits': args.bits,
              'offset': args.offset,
             }
    main(params)
