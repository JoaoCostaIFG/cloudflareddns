# CloudflareDDNS

## Authentication

You can use either of the following:

- API token (**recommended**) - This token only needs permission to write to the
  needed zones;
- API key + email address (**not recommended**) - This option gives access to
  everything in your acount, so it is not recommended.

## Obtaining IPs

We use [Cloudflare cnd-cgi trace](https://www.cloudflare.com/cdn-cgi/trace), to
obtain the machine's IPv4 and IPv6 address.

## Depends on

- [python-cloudflare lib](https://github.com/cloudflare/python-cloudflare)
- [Requests python lib](https://github.com/psf/requests)

## Credits

Some ideas were taken from
[timothymiller's cloudflare-ddns repo](https://github.com/timothymiller/cloudflare-ddns).
It is a bigger repo with more contributers, so you should probably use that one
if it fits your needs.
