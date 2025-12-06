#!/usr/bin/env python3
import subprocess
import re
from pathlib import Path

# ----------------------- #
# CONFIGURATION
# ----------------------- #

# Folder containing the Dockerfile
DOCKER_CONTEXT = Path("../iot-container")  # <-- change path if needed

# Local image name
LOCAL_IMAGE = "iot-container"

# Artifact Registry image base
REMOTE_IMAGE = (
    "europe-west1-docker.pkg.dev/"
    "iot-containers/"
    "iot-repo-69/"
    "iot-server"
)

# ----------------------- #
# FUNCTIONS
# ----------------------- #

def run(cmd):
    """Run shell command and exit on error."""
    print(">", " ".join(cmd))
    subprocess.run(cmd, check=True)

def get_next_version():
    """Gets next vN tag based on remote registry tags."""
    try:
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Tag}}", REMOTE_IMAGE],
            capture_output=True,
            text=True,
            check=True
        )

        tags = result.stdout.split()
        versions = [
            int(re.match(r"v(\d+)", tag).group(1))
            for tag in tags if re.match(r"v\d+", tag)
        ]

        return f"v{max(versions) + 1}" if versions else "v1"

    except subprocess.CalledProcessError:
        return "v1"


# ----------------------- #
# MAIN
# ----------------------- #

def main():
    version = get_next_version()
    full_tag = f"{REMOTE_IMAGE}:{version}"

    print(f"\n📦 Using version: {version}")

    # Build
    run([
        "docker", "build",
        "-t", LOCAL_IMAGE,
        str(DOCKER_CONTEXT)
    ])

    # Tag
    run([
        "docker", "tag",
        LOCAL_IMAGE,
        full_tag
    ])

    # Push
    run([
        "docker", "push",
        full_tag
    ])

    print("\n✅ Done!")
    print("Pushed image:", full_tag)


if __name__ == "__main__":
    main()

