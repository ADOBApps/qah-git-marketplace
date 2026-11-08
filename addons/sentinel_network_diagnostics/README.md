# Sentinel Network Diagnostics

Category: Sentinel addon - Version 1.0.0

Checks whether the HTTPS endpoints used by QAH are reachable from this machine
and reports status plus latency. It is the reference example for the `network`
capability.

## Defaults

```text
https://api.github.com
https://github.com
https://pypi.org/simple/
```

## Configuration

```json
{
  "endpoints": ["https://api.github.com", "https://pypi.org/simple/"],
  "timeout": 5
}
```

- Only `https://` URLs are accepted; credentials in the URL are rejected.
- At most 8 endpoints and 15 seconds per endpoint.
- The addon sends `HEAD` requests only with a fixed user agent. It never sends
  credentials, cookies, files, query strings or request bodies.
- Unreachable endpoints are `high` findings; HTTP 5xx is a `warning`.

## Use it when

- The marketplace or update check fails on one machine but not another.
- You need to document egress requirements for a lab or corporate network.
- You want to compare DNS/TLS latency before and after a VPN change.

Network access is granted only because this addon declares the `network`
capability. Undeclared network use by any addon is blocked by the addon host.
