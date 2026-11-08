# Sentinel Crypto Audit

Static crypto hygiene audit:

- MD5 and SHA1;
- DES/3DES/RC4/Blowfish;
- AES ECB mode;
- disabled TLS verification and unverified contexts;
- hard-coded keys/IVs/salts;
- non-cryptographic randomness for secrets.

Static only. It does not validate keys or decrypt data.
