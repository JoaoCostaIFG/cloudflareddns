# CloudflareDDNS

## Authentication

You can use either of the following (refer to
[Cloudflare's repo](https://github.com/cloudflare/python-cloudflare#using-shell-environment-variables)
for more information):

- `CF_API_KEY` if you're using an API token (**recommended**). This
  token only needs permission to write to the needed zones;
- `CF_API_KEY` and `CF_EMAIL` if you're using an API key (**not
  recommended**). This option gives access to everything in your acount.

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
