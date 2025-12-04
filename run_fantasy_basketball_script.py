import subprocess
import time
import os

# Step 1: Run the existing fantasy basketball program
def run_fantasy_basketball_script():
    print("Running the fantasy basketball game script...")
    subprocess.run(["python", "fantasy_basketball_game.py"], check=True)

# Step 2: Wait for 1 minute
def wait_one_minute():
    print("Waiting for 1 minute...")
    time.sleep(60)

# Step 3: Add, commit, and push changes to GitHub
def push_to_github():
    repo_directory = r"C:\Users\brand\Desktop\FantasyBasketball\BrandonRiv.github.io"  # FIXED PATH
    os.chdir(repo_directory)

    print("Adding changes to git...")
    subprocess.run(["git", "add", "."], check=True)

    print("Committing changes...")
    # SAFE COMMIT: won't crash if no changes
    subprocess.run(
        ["git", "commit", "-m", "Automated commit after running fantasy basketball game script", "--allow-empty"],
        check=True
    )

    print("Pushing to GitHub...")
    subprocess.run(["C:/Program Files/Git/bin/git.exe", "push"], check=True)

def main():
    # Navigate to repo first
    repo_directory = r"C:\Users\brand\Desktop\FantasyBasketball\BrandonRiv.github.io"
    os.chdir(repo_directory)

    run_fantasy_basketball_script()
    wait_one_minute()
    push_to_github()

    print("Script execution completed and changes pushed to GitHub.")

if __name__ == "__main__":
    main()
