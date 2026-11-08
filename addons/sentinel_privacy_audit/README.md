# Sentinel Privacy Audit

Static privacy/PII audit:

- hard-coded Windows/Unix user paths;
- email addresses;
- credential-file and credential-API references;
- logging/printing of passwords, tokens, secrets and API keys;
- clipboard access;
- hard-coded temp paths and environment username use.

No credential file is opened as a credential and no data is transmitted.
