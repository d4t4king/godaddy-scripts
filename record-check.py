#!/usr/bin/env python3

import argparse
import sys
import os
from termcolor import cprint, colored
from godaddypy import Client, Account
import keyring
import pprint
import json


def main():
    pp = pprint.PrettyPrinter(indent=4)

    my_acct = Account(api_key=keyring.get_password('godaddy', 'apikey'), \
                api_secret=keyring.get_password('godaddy', 'apisecret'))
    client = Client(my_acct)

    domains = client.get_domains()
    print("{}".format(domains))

    for dom in domains:
        r = client.get_domain_info(dom)
        print("{}:".format(r['domain']), end=" ")
        if r['status'] == 'CANCELLED':
            cprint("{}".format(r['status']), "red")
        elif r['status'] == 'ACTIVE':
            cprint("{}".format(r['status']), "green")
            records = client.get_records(r['domain'])
            #pp.pprint(records)
            has_caa = False
            has_mxs = False
            has_soa = False
            has_cnames = False
            has_as = False
            has_nss = False
            for R in records:
                if R['type'] == 'A':
                    has_as = True;
                elif R['type'] == 'SOA':
                    has_soa = True;
                elif R['type'] == 'CAA':
                    has_caa = True
                elif R['type'] == 'CNAME':
                    has_cnames = True
                elif R['type'] == 'NS':
                    has_nss = True
                elif R['type'] == 'MX':
                    has_mxs = True
                else:
                    cprint("Unrecognized type: {}".format(R['type']), \
                            "magenta")
            print("\tA: {}, CNAME: {}, SOA: {}, CAA: {}, MX: {}, NS: {}"\
                    .format(has_as, has_cnames, has_soa, has_caa, has_mxs, \
                        has_nss))
        else:
            print("Unrecognized domain status: {}: {}".format(\
                r['domain'], r['status']))



if __name__=='__main__':
    main()

