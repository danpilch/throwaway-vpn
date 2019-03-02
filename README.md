# throwaway-vpn
Generate a throwaway VPN via DigitalOcean

## Installation
`pip install throwaway-vpn`

## Usage
throwaway-vpn

```
usage: throwaway-vpn [-h] (--create | --destroy DESTROY)
                     [--gmail_user GMAIL_USER]
                     [--gmail_user_password GMAIL_USER_PASSWORD]
                     [--gmail_notify_email_list GMAIL_NOTIFY_EMAIL_LIST]
                     --token TOKEN [--do_region DO_REGION] [--do_size DO_SIZE]

Generate a throwaway VPN via DigitalOcean

optional arguments:
  -h, --help            show this help message and exit
  --create, -c          Create a VPN
  --destroy DESTROY, -d DESTROY
                        Destroy VPN (name of vpn)
  --token TOKEN, -t TOKEN
                        DigitalOcean API Token
  --do_region DO_REGION, -r DO_REGION
                        DigitalOcean Region
  --do_size DO_SIZE, -s DO_SIZE
                        DigitalOcean Droplet Size

  --gmail_user GMAIL_USER, -u GMAIL_USER
                        Gmail User email address
  --gmail_user_password GMAIL_USER_PASSWORD, -p GMAIL_USER_PASSWORD
                        Gmail User email password
  --gmail_notify_email_list GMAIL_NOTIFY_EMAIL_LIST, -l GMAIL_NOTIFY_EMAIL_LIST
                        Comma separated list of receive email addresses
```

Example:

`throwaway-vpn -c -t digitalocean_api_token -u from_email -p email_password -l "receiving_email_address" -h`
