# QAH WS Server

Encrypted **remote command console** for Quantum Analysis Helper.

The server listens for paired QAH WS Client installations over **WSS**, runs
commands on this computer, and streams stdout, stderr and the exit code back.

> **Warning.** This is remote command execution. A paired client can run commands
> with your Windows user account. Do not expose it to the internet unless you
> understand port forwarding, firewalls and the password/arming model. There is
> no autostart; the server listens only after you click **Start server**.

## Headless server CLI (1.3.0)

`qah_ws_server_cli.py` runs the same encrypted server without Qt. It is useful
on Linux or for agent-to-agent coordination.

```bash
python3 qah_ws_server_cli.py \
  --bind 0.0.0.0 \
  --public-host <tailscale-or-LAN-IP> \
  --auto-minutes 60 \
  --invite-file invite.txt
```

It supports direct WSS and relay mode (`--transport relay --relay-host ...`).
The invite file is written with mode `0600`. Stop it with `Ctrl+C`; do not
leave it running after the task. Use `--approve-all` only if you understand
the risk; timed auto-approve is safer.

## Documentation tab

The plugin includes an offline **Documentation** tab with:

- the recommended Tailscale setup for private remote access,
- same-LAN and public port-forwarding notes,
- Cloudflare Tunnel requirements and current limitations,
- the planned relay mode (L4 TCP vs L7 WebSocket),
- security checklist, troubleshooting table, data paths and invite contents.

---

## Install

Copy `qah_ws_server/` to:

```text
%USERPROFILE%\QAH\plugins\python_plugins\qah_ws_server\
```

or import `qah_ws_server-1.0.0.qplugin.zip` with **Plugins → Import**. Restart
QAH and open **Plugins → QAH WS Server**.

---

## Quick start

### On the server computer

1. Open **QAH WS Server**.
2. Check **Bind address**, **Port** and **Public host** in Settings.
   - `0.0.0.0` exposes the port on all interfaces.
   - `127.0.0.1` is local-only (use an SSH tunnel for remote access).
3. Click **Start server**.
4. Click **Create pairing invite** and send the `QAHWS1:...` code to the client
   through a trusted channel. It expires after one hour and is single-use.
5. Leave the server running.

### On the client computer

1. Open **QAH WS Client**.
2. Paste the invite in **Connection → Pair**.
3. The client connects and pins the server certificate fingerprint.
4. Use the **Console** tab to run commands; output is streamed live.

The server starts **disarmed**: every command opens an approval dialog showing
the exact command, client and working directory. Choose **Allow once** or
**Deny**.

---

## Relay mode (no inbound port)

Relay mode makes the server connect **outbound** to a rendezvous relay. The
relay copies TLS bytes, so certificate pinning, pairing and application
encryption stay end-to-end. Direct mode is still the default.

1. Copy `relay_server.py` to a machine with a public TCP port and run:

   ```powershell
   python relay_server.py --host 0.0.0.0 --port 45901
   ```

2. Open TCP `45901` in that machine's firewall.
3. In **QAH WS Server → Relay**, select **Relay**, enter the relay host and
   port, generate a room and token, and save.
4. Start the server, create a pairing invite, and send it to the client.
5. The client imports the relay details from the invite automatically.

The **Waiting slots** setting controls how many clients can be paired at the
same time. The relay sees only connection metadata; it cannot read commands or
output.

## Auto-approve modes

### Timed arm

**Policy → Duration → Arm auto-approve**

- Choose a window from **1 to 1440 minutes** (default 30).
- A visible countdown shows the remaining time.
- While armed, commands from paired clients run without a dialog.
- **Disarm now** stops auto-approval immediately.
- Destructive commands still require confirmation.

### Permanent (password protected)

- Set a server password (minimum 8 characters) under **Policy**.
- Click **Enable permanent**.
- Every client session must then enter the server password in the client
  **unlock** prompt. The password is verified on the server with scrypt; it is
  never stored in plaintext in the client.
- Without unlocking, commands still open an approval dialog on the server.
- **Disable permanent** requires the password.

The mode is stored in the server settings. After a restart, permanent mode
remains enabled but clients must unlock again; the server still only listens
after **Start server**.

### Destructive-command guard

Even when auto-approve is armed, patterns such as `format`, `diskpart`,
`bcdedit`, `shutdown`, `reg delete`, recursive `del /s`, encoded PowerShell and
pipe-to-shell are forced through the approval dialog. This guard cannot be
disabled from the UI.

---

## WSS and pairing

- Self-signed certificate generated on first run at:

  ```text
  %USERPROFILE%\QAH\qah_ws_server\cert.pem
  %USERPROFILE%\QAH\qah_ws_server\key.pem
  ```

- The client pins the certificate SHA-256 fingerprint from the invite. A
  different certificate is rejected before any command is sent.
- Pairing uses a random 32-byte secret; the client proves knowledge with HMAC.
- The derived key is stored in `clients.json` (server) and `client.json`
  (client), mode 0600 on Linux/macOS.
- Every command/output frame is AES-256-GCM encrypted inside the WSS stream.

### Ports and firewall

- TCP port **45900** by default (configurable).
- For internet use:
  1. forward the port on the router,
  2. allow it in Windows Firewall,
  3. set **Public host** to the DNS name or `host:port` used in invites.
- Prefer a VPN (WireGuard/Tailscale) over direct port forwarding.

---

## Execution model

- Commands run through the shell (`cmd.exe /c` on Windows).
- stdout and stderr stream in ~4 KB chunks; exit code and duration are sent at
  the end.
- This is **not a PTY**: interactive programs (`vim`, full-screen apps, password
  prompts, Python REPL) will not behave like a terminal.
- Working directory defaults to the server user's home; the client can send one.
- Timeout: 1–600 seconds (client default 300).
- Output is capped at 16 MB per command; the result is marked `truncated`.
- Cancel kills the process tree (`taskkill /T /F` on Windows).

---

## Data files

```text
%USERPROFILE%\QAH\qah_ws_server\
    cert.pem          self-signed certificate
    key.pem           private key (0600)
    settings.json     bind/port/public host, policy, password hash
    clients.json      paired clients and derived keys (0600)
    pending.json      unused invites
    audit.jsonl       command audit log
```

The audit log records client, command, working directory, decision, whether it
was auto-approved, exit code, duration and output size. It does not record
output content.

---

## Limits and security notes

- No full PTY, no interactive input.
- Commands run with the same privileges as QAH; UAC prompts are not visible.
- A paired client is equivalent to that user's shell. Revoke a client in the
  **Clients** tab; this closes its active connection and deletes its key.
- Removing a client does not remove the audit log.
- Do not share the server password or invite. The invite is a bearer secret.
- No autostart, no service installation, no hidden mode.
- Keep the port closed when not in use: **Stop server**.

---

## Files

```text
manifest.json
__init__.py
ws_common.py        WSS, TLS certificate, crypto, invite, relay client helpers
server_core.py      pairing, clients, policy, execution, audit, relay transport
server_ui.py        PySide6 UI
qah_ws_server_cli.py headless Linux/script server CLI
documentation.py    offline Documentation tab
relay_server.py     standalone outbound rendezvous relay
icon.svg
README.md
LICENSE.md
tests/test_integration.py
```
