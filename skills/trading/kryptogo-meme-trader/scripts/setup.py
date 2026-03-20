#!/usr/bin/env python3
"""
KryptoGO Meme Trader - Agent Wallet Setup

This script:
  1. Checks Python 3.10+ and installs required packages (solders, requests)
  2. Generates a Solana keypair if SOLANA_PRIVATE_KEY is not already in .env
  3. Saves the private key (base58) and public key to .env
  4. Sets .env permissions to chmod 600
  5. Prints the public address for the user to fund

Usage:
  python3 scripts/setup.py            # Normal setup (preserves existing key)
  python3 scripts/setup.py --force    # Regenerate keypair (backs up old key)

SECURITY:
  - The private key is stored in .env with restricted permissions (600).
  - NEVER share, log, or commit the .env file.
  - The private key never leaves the local machine during trading.
"""

import argparse
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# 1. Check Python version
# ---------------------------------------------------------------------------

MIN_PYTHON = (3, 10)

if sys.version_info < MIN_PYTHON:
    sys.exit(
        f"ERROR: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required. "
        f"You have Python {sys.version_info.major}.{sys.version_info.minor}."
    )

print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} -- OK")

# ---------------------------------------------------------------------------
# 2. Parse CLI arguments
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(
    description="KryptoGO Meme Trader - Agent Wallet Setup"
)
parser.add_argument(
    "--force",
    action="store_true",
    help="Force regenerate the Solana keypair even if one already exists. "
    "The old key is backed up to .env.backup.<timestamp> before overwriting.",
)
args = parser.parse_args()

# ---------------------------------------------------------------------------
# 3. Install required packages
# ---------------------------------------------------------------------------

REQUIRED_PACKAGES = ["solders", "requests"]


def install_packages():
    """Install missing packages."""
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
            print(f"  {pkg} -- already installed")
        except ImportError:
            print(f"  {pkg} -- installing...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"  {pkg} -- installed")


print("\nChecking dependencies...")
install_packages()

# Now import after ensuring packages are installed
from solders.keypair import Keypair  # noqa: E402

# ---------------------------------------------------------------------------
# 4. Load or create .env
# ---------------------------------------------------------------------------

ENV_FILE = os.path.expanduser("~/.openclaw/workspace/.env")
# Store credentials in the OpenClaw workspace root — NOT the skill directory.
# This ensures heartbeat/cron sessions can find the .env automatically.


def load_env(path):
    """Load .env file into a dict, preserving order and comments."""
    lines = []
    values = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                lines.append(line)
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and "=" in stripped:
                    key, _, val = stripped.partition("=")
                    values[key.strip()] = val.strip()
    return lines, values


def save_env(path, lines):
    """Write .env lines back to file."""
    with open(path, "w") as f:
        f.writelines(lines)
    # Restrict permissions: owner read/write only
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


print(f"\n.env location: {ENV_FILE}")
lines, env_values = load_env(ENV_FILE)

# ---------------------------------------------------------------------------
# 5. Check API key
# ---------------------------------------------------------------------------

api_key = env_values.get("KRYPTOGO_API_KEY", "")
if not api_key or api_key == "sk_live_your_key_here":
    print(
        "\nWARNING: KRYPTOGO_API_KEY is not set in .env.\n"
        "  Get your API key at: https://www.kryptogo.xyz/account\n"
        "  Then add it to .env:  KRYPTOGO_API_KEY=sk_live_..."
    )
else:
    # Do not print any part of the key — even masked suffixes can leak info
    print("KRYPTOGO_API_KEY: set ✓")

# ---------------------------------------------------------------------------
# 6. Generate Solana keypair (or load existing one)
# ---------------------------------------------------------------------------

existing_private_key = env_values.get("SOLANA_PRIVATE_KEY", "")


def _derive_address(base58_private_key):
    """Reconstruct a Keypair from a base58-encoded private key and return the public address."""
    kp = Keypair.from_base58_string(base58_private_key)
    return str(kp.pubkey())


def _backup_env(env_path):
    """Copy the current .env to .env.backup.<UTC timestamp>."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = f"{env_path}.backup.{ts}"
    shutil.copy2(env_path, backup_path)
    # Preserve restricted permissions on the backup
    os.chmod(backup_path, stat.S_IRUSR | stat.S_IWUSR)
    return backup_path


def _write_keypair_to_env(new_private_key, new_public_key, env_lines, env_path):
    """Write a keypair into the .env file, updating existing entries or appending."""
    found_private = False
    found_public = False
    new_lines = []

    for line in env_lines:
        stripped = line.strip()
        if stripped.startswith("SOLANA_PRIVATE_KEY="):
            new_lines.append(f"SOLANA_PRIVATE_KEY={new_private_key}\n")
            found_private = True
        elif stripped.startswith("SOLANA_WALLET_ADDRESS="):
            new_lines.append(f"SOLANA_WALLET_ADDRESS={new_public_key}\n")
            found_public = True
        else:
            new_lines.append(line)

    if not found_private:
        new_lines.append(f"SOLANA_PRIVATE_KEY={new_private_key}\n")
    if not found_public:
        new_lines.append(f"SOLANA_WALLET_ADDRESS={new_public_key}\n")

    # If .env didn't exist at all, also add API key placeholder
    if not env_lines:
        new_lines.insert(0, "KRYPTOGO_API_KEY=sk_live_your_key_here\n")

    save_env(env_path, new_lines)


if existing_private_key and not args.force:
    # ---- Existing key detected: load it, derive address, skip generation ----
    derived_address = _derive_address(existing_private_key)

    # Ensure SOLANA_WALLET_ADDRESS is consistent (auto-heal if missing/stale)
    stored_address = env_values.get("SOLANA_WALLET_ADDRESS", "")
    if stored_address != derived_address:
        print(f"\nRepairing SOLANA_WALLET_ADDRESS (was: '{stored_address}', expected: '{derived_address}')")
        _write_keypair_to_env(existing_private_key, derived_address, lines, ENV_FILE)

    print(f"\nSolana wallet already configured: {derived_address}")
    print("  Private key: present in .env (unchanged)")
    print(f"\n  To regenerate, re-run with --force:")
    print(f"    python3 scripts/setup.py --force")

elif existing_private_key and args.force:
    # ---- Force regeneration: warn, back up, then create new key ----
    old_address = _derive_address(existing_private_key)
    print(
        f"\n{'='*60}\n"
        f"  WARNING: --force flag detected.\n"
        f"  This will REPLACE the existing Solana keypair.\n"
        f"  Old wallet address: {old_address}\n"
        f"\n"
        f"  ANY FUNDS on the old address will become INACCESSIBLE\n"
        f"  unless you restore from the backup.\n"
        f"{'='*60}"
    )

    # Back up current .env before overwriting
    backup_path = _backup_env(ENV_FILE)
    print(f"\n  Old .env backed up to: {backup_path}")

    keypair = Keypair()
    new_private_key = str(keypair)  # base58-encoded private key
    new_public_key = str(keypair.pubkey())

    _write_keypair_to_env(new_private_key, new_public_key, lines, ENV_FILE)

    print(f"\n  New private key: saved to .env (NEVER share this)")
    print(f"  New public address: {new_public_key}")
    print(f"\n  .env permissions set to 600 (owner read/write only)")
    print(f"\n  Fund this address with SOL to start trading:")
    print(f"    {new_public_key}")
    print(f"\n  To restore the old key, copy the backup back:")
    print(f"    cp '{backup_path}' '{ENV_FILE}'")

else:
    # ---- No existing key: first-time generation ----
    print("\nGenerating new Solana keypair...")
    keypair = Keypair()
    new_private_key = str(keypair)  # base58-encoded private key
    new_public_key = str(keypair.pubkey())

    _write_keypair_to_env(new_private_key, new_public_key, lines, ENV_FILE)

    print(f"  Private key: saved to .env (NEVER share this)")
    print(f"  Public address: {new_public_key}")
    print(f"\n  .env permissions set to 600 (owner read/write only)")
    print(f"\n  Fund this address with SOL to start trading:")
    print(f"    {new_public_key}")

# ---------------------------------------------------------------------------
# 7. Summary
# ---------------------------------------------------------------------------

print("\n--- Setup complete ---")
print("Next steps:")
print("  1. Fund the agent wallet with SOL (min 0.1 SOL for gas + trading capital)")
print("  2. Set KRYPTOGO_API_KEY in .env if not already done")
print("  3. Tell the agent to scan for opportunities, or set up heartbeat — see SKILL.md")
