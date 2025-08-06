Autocommit-Agent

Author: Roni Herschmann

A simple Python-based agent that autonomously makes multiple daily commits to its own GitHub repository.

Features
	•	Schedules 5–10 commits per day by default
	•	Appends a timestamp comment to its own code for each commit
	•	Stages, commits, and pushes changes to the configured branch
	•	Runs continuously once launched (no repository creation)

Prerequisites
	•	Python 3.6 or higher
	•	Git installed and available on your PATH
	•	A local clone of this repository
	•	A GitHub personal access token with repo scope

Installation
	1.	Clone the repository (if not already):

cd ~/Desktop
git clone https://github.com/roniherschmann/Autocommit-Agent.git
cd Autocommit-Agent


	2.	Ensure you have dependencies installed in your active Python environment:

pip install GitPython


	3.	Place the script (if you have it separately) into the repo root:

mv ~/Downloads/auto_commit_agent.py .



Configuration

You can adjust behavior via environment variables. By default, the agent does 7 commits/day between 09:00 – 17:00 on the main branch.

Variable	Description	Default
COMMIT_COUNT	Number of commits per day	7
START_HOUR	Earliest hour for commits (0–23)	9
END_HOUR	Latest hour for commits (0–23)	17
BRANCH	Branch name to push commits to	main

Example:

export COMMIT_COUNT=5
export START_HOUR=8
export END_HOUR=18
export BRANCH=develop

Usage

Run the agent in your terminal:

python auto_commit_agent.py

Upon startup, you’ll see a schedule printed, e.g.:

Today's commit schedule: 09:13, 10:45, 12:02, 14:28, 16:55, ...

Then the script will:
	1.	Append a timestamp comment (# Auto-updated at YYYY-MM-DDTHH:MM:SSZ) to itself
	2.	Stage, commit, and push that change
	3.	Repeat at each scheduled time

Running in the Background

To keep the agent running continuously, consider one of:
	•	screen or tmux session:

screen -S autocommit
python auto_commit_agent.py
# detach with Ctrl+A, D


	•	nohup:

nohup python auto_commit_agent.py &> agent.log &


	•	systemd (Linux) or launchd (macOS) service for auto-start on boot.

Contributing
	1.	Fork the repository
	2.	Create a feature branch
	3.	Submit a pull request with your changes

License

This project is released under the MIT License. See LICENSE for details.
