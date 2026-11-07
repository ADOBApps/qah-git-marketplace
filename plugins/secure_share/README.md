# Secure Share

Encrypted exchange of **text, files and folders** between Quantum Analysis
Helper computers.

Two transports, one UI:

| Transport | When to use | Needs |
|---|---|---|
| **LAN** | Both computers on the same Wi-Fi/LAN | Open firewall ports (or allow the QAH prompt) |
| **Git relay** | Different networks, asynchronous send/receive | A private GitHub repository + token |

Every message is encrypted with **AES-256-GCM** using a pairwise key derived from
X25519 and a one-time pairing secret. The relay and the LAN only ever see
ciphertext.

**Printable guide:** `Secure_Share_Guide.pdf` (included in the plugin package).

---

## Install

Copy `secure_share/` to:

```text
%USERPROFILE%\QAH\plugins\python_plugins\secure_share\
```

or import `secure_share.qplugin.zip` through **Plugins → Import**.

Restart QAH, scan plugins, then open **Plugins → Secure Share**.

---

## Pair two devices

1. On computer A: **Peers → Pair a device... → Create invite**.
2. Copy the `QAHPAIR1:...` invite and transfer it to computer B through a
   trusted channel (password manager, USB, in person). It contains a one-time
   secret and expires after **one hour**.
3. On computer B: **Peers → Pair a device... → Import invite**, paste it and
   click **Import and pair**.
4. B derives the pairwise key and sends an encrypted handshake:
   - over the LAN if A's address in the invite is reachable, otherwise
   - through the Git relay if it is enabled.
5. A accepts the handshake and both devices show each other in the peer list.

Treat the invite like a password until it is used: anyone who has it can pair
with A. Pairing is single-use; the pending invite is removed after the
handshake.

---

## Send and receive

### Text

**Send** tab → choose a peer → type/paste text → **Send text**.

Received text appears in **Inbox** and is copied to the clipboard when
*Copy received text to the clipboard* is enabled (default).

### Files

**Send → Send file(s)...** selects one or more files. The receiver saves them to
its inbox under a per-peer folder, with the original name and a timestamp.

### Folders

**Send → Send folder...** zips the folder in memory, encrypts it, and sends one
envelope. The receiver extracts it safely (no absolute paths, `..` or symlinks)
into the inbox.

### Inbox

Received items are listed in **Inbox**. Double-click or **Open** to open a file
or folder; **Copy text** copies a received message. **Clear history** does not
delete files already saved in the inbox.

Inbox default:

```text
%USERPROFILE%\QAH\secure_share\inbox\<peer-id>\
```

Change it in **Settings → Inbox folder**.

---

## LAN transport

- UDP discovery on port **45872**; encrypted TCP on port **45873** (if busy, the
  next free port is used and advertised).
- Windows may show a firewall prompt the first time. Allow QAH on private
  networks.
- Devices must be paired before messages are accepted.
- Discovery packets contain the device name, random device id and TCP port.
  They do not contain keys or message content.
- If discovery is blocked, Git relay is the fallback.

---

## Git relay (optional)

Useful when the computers are not on the same network, or when the other device
is offline.

1. Create a **private** GitHub repository, e.g. `ADOBApps/qah-secure-relay`.
2. Create a fine-grained token with **Contents: Read and write** on that
   repository (or a classic `repo` token).
3. In **Git relay**, enable it and fill in owner, repository, branch, token, path
   prefix (default `secure_share`) and poll interval.
4. **Test connection**, then **Check now** on the receiving computer.

Each envelope is committed as:

```text
secure_share/<recipient-device-id>/<timestamp>-<message-id>.json
```

The receiver downloads, decrypts, saves and deletes the file. The repository is
private and the content is encrypted, but Git history and file names still
reveal random device ids and timestamps.

Token resolution:

1. token saved in Secure Share settings,
2. `QAH_SECURE_SHARE_TOKEN`,
3. `GITHUB_TOKEN` / `GH_TOKEN`.

The settings file is stored with mode 0600 on Linux/macOS and user-profile ACL on
Windows. Do not commit it.

---

## Security model

- **Identity:** each installation has an X25519 keypair and an Ed25519 keypair in
  `%USERPROFILE%\QAH\secure_share\identity.json`.
- **Pairing:** the invite contains a random 32-byte secret. Both sides derive the
  same key with X25519 + HKDF-SHA256 (salt = pairing secret).
- **Messages:** AES-256-GCM with a random 96-bit nonce per envelope. The
  associated data covers version, type, sender, recipient, message id and
  timestamp, so headers cannot be altered.
- **Replay protection:** message ids are recorded in `seen.json`; duplicates are
  rejected.
- **No plaintext on the wire:** LAN frames and Git relay files contain only
  ciphertext and routing metadata.
- **Inbox/history are plaintext:** received files and text history are stored
  locally for the user. Use disk encryption if the machine is shared.

### Limitations

- **No forward secrecy.** The pairwise key is long-lived. If a device key or
  `peers.json` is stolen, captured ciphertext could be decrypted. Re-pair and
  remove the peer if a device is lost.
- The pairing invite is a bearer secret. Transfer it only through a trusted
  channel and do not leave it in chat history.
- LAN discovery metadata is not encrypted.
- Files are encrypted in memory; very large transfers use memory. Limits:
  **100 MB per file**, **200 MB per folder**.
- No chunking/resume; a failed large LAN transfer must be retried.
- No automatic updates, no central server, no accounts.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Peer not shown as online | Same LAN? Firewall allows QAH? Try **Refresh peers**; use Git relay. |
| Pairing handshake not delivered | The other computer must be running Secure Share with LAN on, or relay enabled. |
| LAN port busy | The next free port is used; the invite advertises the actual port. |
| Relay 401/403 | Token invalid or missing Contents read/write on the private repo. |
| Relay 404 | Wrong owner/repo/branch, or token has no access. |
| Folder rejected | It exceeds 200 MB or contains a symlink/unsafe path. |
| Text not on clipboard | Enable **Copy received text to the clipboard** in Settings. |

---

## Files

```text
manifest.json
__init__.py
secure_share_core.py      Qt-free crypto, pairing, LAN, relay, inbox
secure_share_ui.py        PySide6 UI
icon.svg
README.md
Secure_Share_Guide.pdf
LICENSE.md
tests/test_core.py
```
