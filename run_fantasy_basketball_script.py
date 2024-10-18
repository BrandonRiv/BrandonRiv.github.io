import subprocess
import time
import os

# Step 1: Run the existing fantasy basketball program
def run_fantasy_basketball_script():
    print("Running the fantasy basketball game script...")
    subprocess.run(["python", "fantasy_basketball_game.py"], check=True)  # Assuming your program is saved as 'fantasy_basketball_game.py'

# Step 2: Wait for 1 minute
def wait_one_minute():
    print("Waiting for 1 minute...")
    time.sleep(60)  # Wait for 60 seconds

# Step 3: Add, commit, and push changes to GitHub
def push_to_github():
    # Navigate to your project directory
    repo_directory = "C:/Users/Admin/Desktop/BrandonRiv.github.io"  # Replace with your actual repo path
    os.chdir(repo_directory)

    print("Adding changes to git...")
    subprocess.run(["git", "add", "."], check=True)

    print("Committing changes...")
    subprocess.run(["git", "commit", "-m", "Automated commit after running fantasy basketball game script"], check=True)

    print("Pushing to GitHub...")
    subprocess.run(["git", "push"], check=True)  # Assumes you have git configured to use HTTPS/SSH for pushing

# Main function to run the steps
def main():
    run_fantasy_basketball_script()
    wait_one_minute()
    push_to_github()
    print("Script execution completed and changes pushed to GitHub.")

# Run the main function
if __name__ == "__main__":
    main()
