import subprocess
import sys
from pathlib import Path

# ==========================
# CONFIG
# ==========================
DATABASE_NAME = "iot-database"      # <-- change to your D1 database name
SCHEMA_FILE = "schema.sql"
USE_REMOTE = True          # set False to run against local dev DB
NO_TRANSACTION = True     # usually needed for multi-statement schemas

# ==========================
# SCRIPT
# ==========================
def main():
    schema_path = Path(SCHEMA_FILE)

    if not schema_path.exists():
        print(f"[!] - Schema file not found: {schema_path}")
        sys.exit(1)

    cmd = [
        "npx",
        "wrangler",
        "d1",
        "execute",
        DATABASE_NAME,
        f"--file=./{schema_path}",
    ]

    if USE_REMOTE:
        cmd.append("--remote")

    print("Running command:")
    print(" ".join(cmd))
    print()

    try:
        subprocess.run(cmd, check=True)
        print("\n[x] - Schema executed successfully!")
    except subprocess.CalledProcessError as e:
        print("\n[!] - Failed to execute schema.")
        print(e)
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()
