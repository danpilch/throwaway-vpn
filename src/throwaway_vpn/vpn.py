#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import datetime
import digitalocean
import sys

from throwaway_vpn import __version__
from throwaway_vpn.user_data import user_data_core

__author__ = "danpilch"
__copyright__ = "danpilch"
__licence__ = "mit"


class VPNGenerator(object):
    def __init__(self, do_api_token):
        self.token = do_api_token
        self.date = datetime.datetime.now().strftime("%Y-%d-%m")
        self.manager = digitalocean.Manager(token=self.token)

    def generate_user_data(self, gmail_user, gmail_password, gmail_to):
        try:
            email_list = "'" + "\',\'".join(gmail_to.split(',')) + "'"
            user_data = user_data_core.format(gmail_user, gmail_password, email_list)
            return user_data

        except Exception as e:
            raise

    def destroy_vpn(self, args):
        try: 
            vpns = self.manager.get_all_droplets(tag_name=args.destroy)
            if len(vpns) >= 1:                
                for v in vpns:
                    v.destroy()
                    print("Destroying VPN: {0}".format(args.destroy))
            else:
                print("No VPNs match")

        except Exception as e:
            raise
        

    def create_vpn(self, args):
        keys = self.manager.get_all_sshkeys()

        vpn_name = "vpn-{0}".format(self.date)

        self.vpn_user_data = self.generate_user_data(
                args.gmail_user, 
                args.gmail_user_password,
                args.gmail_notify_email_list
        )

        vpn = digitalocean.Droplet(
            token=self.token,
            tags=[vpn_name],
            region=args.do_region,
            name=vpn_name,
            size_slug=args.do_size,
            image="ubuntu-18-04-x64",
            ssh_keys=keys,
            backups=False,
            ipv6=True,
            user_data=self.vpn_user_data,
            private_networking=False,
        )

        vpn.create()
        print("Created VPN: {0}. Please wait for email.".format(vpn_name))


def main(args):
    parser = argparse.ArgumentParser(description="Generate a throwaway VPN via DigitalOcean")
    group_mode = parser.add_mutually_exclusive_group(required=True)
    group_notify = parser.add_argument_group()

    group_mode.add_argument(
        "--create", "-c",
        action="store_true",
        help="Create a VPN"
    )
    
    group_mode.add_argument(
        "--destroy", "-d",
        default=None,
        help="Destroy VPN (name of vpn)"
    )
    
    group_notify.add_argument(
        "--gmail_user", "-u",
        help="Gmail User email address"
    )

    group_notify.add_argument(
        "--gmail_user_password", "-p",
        help="Gmail User email password"
    )

    group_notify.add_argument(
        "--gmail_notify_email_list", "-l",
        help="Comma separated list of receive email addresses"
    )
    
    parser.add_argument(
        "--token", "-t",
        help="DigitalOcean API Token",
        required=True,
    )
    
    parser.add_argument(
        "--do_region", "-r",
        help="DigitalOcean Region",
        default="lon1",
    )
    
    parser.add_argument(
        "--do_size", "-s",
        help="DigitalOcean Droplet Size",
        default="s-1vcpu-1gb",
    )

    args = parser.parse_args()

    run = VPNGenerator(args.token)

    if args.create:
        run.create_vpn(args)
    elif args.destroy is not None:
        run.destroy_vpn(args)

def run():
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
