# QAH WS Client

Encrypted client for **QAH WS Server**. Connects over WSS, pairs with a
one-time invite, sends commands and displays live stdout/stderr and the exit
code.

> **Warning.** This client can execute commands on the paired server with that
> server's user account. Connect only to servers you own or administer.

---

## Install

Copy `qah_ws_client/` to:

```text
%USERPROFILE%\QAH\plugins\python_plugins\qah_ws_client\
```

or import `qah_ws_client-1.0.0.qplugin.zip` with **Plugins → Import**. Restart
QAH and open **Plugins → QAH WS Client**.

---

## Pair and connect

1. Get a `QAHWS1:...` invite from the server's **Create pairing invite** button.
2. Open the **Connection** tab, paste it and click **Pair**.
3. The client verifies the server certificate fingerprint from the invite and
   stores the pairing key.
4. Click **Connect** if it does not connect automatically.

If the server is in **permanent auto-approve** mode, the client asks for the
server password. Entering it unlocks auto-approval for that session. Without it,
the server still asks the operator to approve each command.

---

## Console

```text
> echo hello
hello
exit 0 · 0.12s · 6 bytes
```

- **Run** sends the command; output streams live.
- **Cancel** asks the server to kill the process tree.
- The exit line shows code, duration, bytes and whether output was truncated.
- Commands are non-interactive: no PTY, so full-screen programs and prompts do
  not work.
- Timeout: 300 seconds in the UI; the server caps at 600.
- Output capped at 16 MB per command.

---

## Security model

- WSS with a self-signed server certificate pinched by SHA-256 fingerprint.
- Pairing secret + HMAC authentication; stored key in
  `%USERPROFILE%\QAH\qah_ws_client\client.json` (0600 on Linux/macOS).
- Commands and output are AES-256-GCM encrypted inside the TLS stream.
- The server password (if permanent mode is enabled) is verified on the server;
  the client does not store it.
- The client cannot change server policy or approve its own commands.

---

## Settings

- Client name (shown on the server).
- **Clear pairing** removes the server URL, fingerprint and key. You must pair
  again.

Data file:

```text
%USERPROFILE%\QAH\qah_ws_client\client.json
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Fingerprint mismatch | The invite belongs to a different server/certificate. Get a new invite. |
| Invalid or expired invite | Invites are single-use and expire after one hour. Create a new one. |
| Authentication failed | Pairing key was cleared/revoked on the server. Pair again. |
| Password rejected | Permanent mode uses the server's current password. |
| Command denied | Server is disarmed, client is not unlocked, or the command is in the destructive guard. |
| Connection drops | Server stopped, firewall/port forwarding changed, or WSS certificate replaced. |
| No output | Some programs buffer when stdout is a pipe; use non-interactive flags. |

---

## Files

```text
manifest.json
__init__.py
ws_common.py        WSS, TLS certificate, crypto, invite helpers
client_core.py      pairing, authentication, execute/cancel, output
client_ui.py        PySide6 UI
icon.svg
README.md
LICENSE.md
tests/test_integration.py
```
