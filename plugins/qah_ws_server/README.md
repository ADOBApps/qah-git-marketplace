# QAH WS Server

Encrypted **remote command console** for Quantum Analysis Helper.

The server listens for paired QAH WS Client installations over **WSS**, runs
commands on this computer, and streams stdout, stderr and the exit code back.

> **Warning.** This is remote command execution. A paired client can run commands
> with your Windows user account. Do not expose it to the internet unless you
> understand port forwarding, firewalls and the password/arming model. There is
> no autostart; the server listens only after you click **Start server**.

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

## Auto-approve modes

### Timed arm

**Policy → Arm auto-approve (30 min)**

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
ws_common.py        WSS, TLS certificate, crypto, invite helpers
server_core.py      pairing, clients, policy, execution, audit
server_ui.py        PySide6 UI
icon.svg
README.md
LICENSE.md
tests/test_integration.py
```
