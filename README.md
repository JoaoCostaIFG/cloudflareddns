# CloudflareDDNS

This repo contains a python script that will update/create DNS record in
Cloudflare. It uses a versatile [config file](./sample-config.json) to do so.

## Features

- Can create and update Cloudflare DNS records;
- All requests are HTTPS;
- Checks IPs using a zero-log provider (see
  [Obtaining IPs section](#obtaining-ips));
- Has optional field, so it can be used to just update the remote record info
  (without touching TTL, and proxy settings);
- Support both IPv4 and IPv6;
- Only logs information when it changing something remotely: cron only send an
  e-mail notification when there are changes;
- Has a docker container for those interested.

## Running

### Cronjob

I recommend using [cron](https://github.com/cronie-crond/cronie) to run the
script every 5 minutes or so. Something along the line of:

```sh
*/5 * * * * python /cfddns.py
```

### Docker container

If you don't want to run the python script in your machine (_natively_), you can
run it in a docker container. I've provided an example
[docker compose file](./docker-compose.yml), so you can specify your
configuration file path (it gets copied into the container).

## Configuration file

The repo includes a [sample config file](./sample-config.json). It contains a
list of **zones**, and an option specifying whether or to use IPv4 and IPv6.
Consideration on creating a zone:

- Provide an `authentication` method. Either `api_token`, or `api_key`. These
  are explained in the [authentication section](#authentication);
- Provide a `zone_id` or a `zone_name`. You can provide both, but it isn't
  necessary;
- Provide the list of `subdomains` to update/create. The **empty subdomain**
  (`""`) corresponds to the _base_ subdomain, e.g.: `joaocosta.dev`;
- The `ttl` file is optional. If not specified, it will take the value of the
  corresponding remote (in Cloudflare DNS) record, or `auto` if such a record
  doesn't exist;
- The `proxied` file is optional. If not specified, it will take the value of
  the corresponding remote (in Cloudflare DNS) record, or `False` if such a
  record doesn't exist.

You can provide multiple zones.

## Authentication

You can use either of the following:

- API token (**recommended**) - This token only needs permission to write to the
  needed zones;
- API key + email address (**not recommended**) - This option gives access to
  everything in your acount, so it is not recommended.

## Depends on

- [python-cloudflare lib](https://github.com/cloudflare/python-cloudflare)
- [Requests python lib](https://github.com/psf/requests)

## Implementation details

### Obtaining IPs

We use [Cloudflare cnd-cgi trace](https://www.cloudflare.com/cdn-cgi/trace), to
obtain the machine's IPv4 and IPv6 address.

## Credits

Some ideas were taken from
[timothymiller's cloudflare-ddns repo](https://github.com/timothymiller/cloudflare-ddns).
It is a bigger repo with more contributers, so you should probably use that one
if it fits your needs.
