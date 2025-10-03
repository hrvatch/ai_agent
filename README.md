# AI Agent Guided Project

This repository is a small guided project inspired by [boot.dev](https://boot.dev), created to better understand how AI agents work and how they can interact with their environment.

The project demonstrates how an agent can:
- List directory contents
- Edit files
- Read file contents
- Execute a file

These capabilities form the basic "toolbox" that an AI agent can use to interact with a simple project environment.

## Project Structure

Inside the main project, there is a nested project: a simple calculator written in Python.  
The calculator contains a deliberate bug. The goal is to let an AI agent (for example Gemini) use the provided functions to explore the codebase, identify the bug, and fix it.

This setup creates a controlled sandbox for experimenting with autonomous or semi-autonomous agents.

## Key Functions

The following functions are exposed to the AI agent:

1. List directory contents  
   Allows the agent to explore the filesystem.

2. Read file contents  
   Lets the agent inspect the code inside any file.

3. Edit file contents  
   Enables the agent to patch or fix bugs in code.

4. Execute a file  
   Runs Python files so the agent can test whether the changes worked.

Together, these simulate a minimal but powerful development environment for an agent.

## Example Workflow

1. Start the project  
2. Give the agent the task: "Fix the bug in the calculator"  
3. The agent will:  
   - Explore the directory  
   - Open and read the calculator code  
   - Identify the bug  
   - Edit the file to patch the bug  
   - Re-run the calculator to test the fix

## Getting Started

### Prerequisites
- Python 3.10+
- Recommended: virtual environment (venv or conda)
