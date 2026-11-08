# Sentinel Network Audit

Static, read-only network audit of QAH plugins.

## Checks

- network imports (`socket`, `requests`, `httpx`, `aiohttp`, `urllib`,
  `paramiko`, `websocket`, `smtplib`, `ftplib`, `grpc`, and more);
- HTTP/WebSocket/SSH/FTP endpoints and IP literals;
- declared `network` capability vs actual imports;
- undeclared network usage;
- localhost/example endpoints separated from external endpoints.

It never opens a socket or sends data. Dynamic URLs built at runtime may not be
visible to a static scan.
