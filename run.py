import os
import subprocess
import sys


def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    # Install the requirements
    print("📦 Installing the requirements...")
    run_command("pip install -r requirements.txt")

    # Format the code with black
    print("🖌 Formatting the code with black...")
    run_command("black .")

    # Run tests with pytest
    print("🧪 Running tests with pytest...")
    run_command("pytest")

    # Run the main script
    print("🚀 Running the main script...")
    run_command("python main.py")


if __name__ == "__main__":
    main()
