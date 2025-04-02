import os
import time
import hashlib
import requests
import sys

# GitHub raw URL to the bot script
GITHUB_RAW_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/bot.py"
CHECK_INTERVAL = 60  # Time in seconds between update checks
BOT_FILENAME = "bot.py"  # The script being updated

def get_remote_script():
    """Fetch the latest version of the bot script from GitHub."""
    response = requests.get(GITHUB_RAW_URL)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch the bot script. Status code:", response.status_code)
        return None

def get_local_script():
    """Read the current version of the bot script."""
    if not os.path.exists(BOT_FILENAME):
        return ""  # If bot.py doesn't exist yet, treat it as an empty file
    with open(BOT_FILENAME, "r", encoding="utf-8") as f:
        return f.read()

def hash_content(content):
    """Generate a hash for comparison."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def update_script(new_script):
    """Update bot.py with the new version."""
    with open(BOT_FILENAME, "w", encoding="utf-8") as f:
        f.write(new_script)

def restart_script():
    """Restart the bot script."""
    print("Restarting bot script...")
    python = sys.executable
    os.execl(python, python, BOT_FILENAME, *sys.argv[1:])

def main():
    """Main function that checks for updates in a loop."""
    while True:
        print("Checking for updates...")
        remote_script = get_remote_script()
        if remote_script:
            local_script = get_local_script()
            if hash_content(remote_script) != hash_content(local_script):
                print("Update found! Updating bot script...")
                update_script(remote_script)
                restart_script()
            else:
                print("No updates found.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    """Ensures that the updater runs only when executed directly."""
    main()