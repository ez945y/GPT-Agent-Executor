# GPT Agent Executor: Enabling Autonomous Collaboration and Continuous Operation

# Project Description

[中文版](README.md)

This project aims to build an autonomous agent framework based on GPT, enabling the continuous operation and collaboration of intelligent agents.

Through modular design, we decompose the intelligent agent into three core modules:

* **Think Agent:** Responsible for analyzing goals, planning tasks, and generating action plans.
* **Tool Agent:** Based on the decisions of the Think Agent, it calls external tools or APIs to execute specific tasks.
* **Target Agent:** Observes its own thoughts, determines what tool to use, and returns a target.

Additionally, this project provides a user-friendly interactive interface and supports multiple language model backends such as Ollama and Gemini API, allowing you to choose the most suitable model according to your needs.

## Project Features

* **Autonomous Operation:** The intelligent agent can autonomously plan and execute tasks based on goals without human intervention.
* **Modular Design:** The three core modules perform their respective duties, facilitating expansion and maintenance.
* **Multi-Model Support:** Supports multiple language model backends such as Ollama and Gemini API, providing flexible choices.
* **User Interaction:** Provides a user-friendly interactive interface for convenient interaction between users and the intelligent agent.
* **Continuous Learning:** The intelligent agent can continuously learn and evolve through interaction with the environment.
* **One-Click Launch:** Provides convenient startup scripts that automatically launch the server and client.

## Project Architecture

* **Think Agent:**
    * Responsible for goal analysis, task planning, and action decision-making.
    * Utilizes language models to generate thought processes and action plans.
* **Tool Agent:**
    * Based on the decisions of the Think Agent, it calls external tools or APIs.
    * Responsible for executing specific tasks and returning the results to the Think Agent.
* **Target Agent:**
    * Observes its own thoughts, determines what tool to use, and returns a target.
    * Returns the target to the Think Agent.
* **User Interaction:**
    * Provides a command-line interface or web interface.
    * Allows users to set goals, view progress, and interact with the intelligent agent.
* **Model Backend:**
    * Supports Ollama and Gemini API.
    * Allows users to choose models according to their needs.

## Use Cases

* **Automated Task Execution:** Automatically executes tasks such as data collection, report generation, and code writing.
* **Intelligent Assistant:** Provides services such as personal assistant, customer service, and knowledge Q&A.
* **Research and Development:** Used to explore intelligent agent behavior and test language model capabilities.

## Installation and Launch

### Method 1: One-Click Launch (Recommended)

**macOS/Linux:**
```bash
./start_chat.sh
```

**Windows:**
```cmd
start_chat.bat
```

These scripts will automatically:
- Check and start the server (in a new window)
- Launch the chat client (in the current window)
- Wait for the server to be ready

### Method 2: Manual Launch

1.  **Install Conda:**
    * If you don't have Conda installed on your computer, please download and install Anaconda or Miniconda from the Anaconda official website.
2.  **Create Conda Environment:**
    * Use the following command to create a Conda environment:
        * `conda create --name continuous-gpt-ai-agent --file requirements.txt`
    * Alternatively, you can use the following command to create an environment from the `requirements.txt` file:
        * `conda env create -f environment.yml`
3.  **Activate Conda Environment:**
    * Use the following command to activate the Conda environment:
        * `conda activate continuous-gpt-ai-agent`
4.  **Start the Server:**
    * `python start_server.py`
5.  **Start the Client:**
    * `python cli_client.py`

## AI Chat Application

This is an AI chat application based on FastAPI and React, supporting multiple interaction methods.

## Features

- 🤖 Multi-Agent System: ThinkAgent, ToolAgent, TargetAgent
- 💬 Multiple Clients: Web interface, CLI client
- 🔄 Real-time Monitoring: Automatically monitor AI thinking process
- 🛠️ Tool Integration: Support for web search and other functions
- 📊 Logging: Complete chat and thinking logs
- 🚀 One-Click Launch: Automatically launch server and client

## Quick Start

### Method 1: One-Click Launch (Recommended)

**macOS/Linux:**
```bash
./start_chat.sh
```

**Windows:**
```cmd
start_chat.bat
```

This will automatically open two windows:
- **Server Window:** Running FastAPI server
- **Client Window:** Running CLI chat client

### Method 2: Manual Launch

#### 1. Start the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python start_server.py
```

#### 2. Use the Client

#### Web Interface
Visit http://localhost:3000 to use the React frontend interface

#### CLI Client (Recommended)
```bash
# Interactive mode (default auto-monitoring)
python cli_client.py

# Verbose mode (display all monitoring content)
python cli_client.py -v

# Command line mode
python cli_client.py start
python cli_client.py send "Hello"
python cli_client.py monitor
```

## CLI Client Features

### Unified Interface
- **Auto-Monitoring:** Automatically starts monitoring think output after launch
- **Real-time Status:** Displays chat status (🟢/🔴) and monitoring status (👀)
- **Simplified Commands:** Use `+` symbol to send messages
- **Complete Functions:** Support all API endpoints

### Monitoring Features
- **Auto-Monitoring:** Automatically starts background monitoring on launch
- **Think Output:** Real-time display of AI thinking process
- **Verbose Mode:** Use `-v` or `monitor-verbose` to display all content
- **Manual Control:** Can start/stop monitoring at any time

### Command List
```bash
# Basic commands
start          - Start conversation
close/stop     - Close conversation
+ <text>       - Send message (simplified mode)
send <text>    - Send message (complete mode)
status         - Check status
cache          - View cache pool

# Monitoring commands
monitor        - Start real-time monitoring
monitor-verbose - Start verbose monitoring (display all content)
stop-monitor   - Stop monitoring

# Advanced commands
list           - Conversation list
conv <id>      - View conversation content
help           - Display help information
quit/exit      - Exit program
```

## Usage Examples

### 1. Basic Usage
```bash
# Start client
python cli_client.py

# In the client:
🟢👀 > start
🟢👀 > + Hello, I want to know today's weather
🟢👀 > status
🟢👀 > close
```

### 2. Verbose Monitoring
```bash
# Start verbose mode
python cli_client.py -v

# Or manually switch to verbose monitoring
🟢👀 > stop-monitor
🟢 > monitor-verbose
🟢👀 > + Hello
```

### 3. Command Line Mode
```bash
# Execute commands directly
python cli_client.py start
python cli_client.py send "Hello"
python cli_client.py monitor
python cli_client.py status
```

## Future Directions

* Add support for more tools and APIs.
* Optimize the learning and reasoning capabilities of the intelligent agent.
* Develop richer user interaction interfaces.
* Explore multi-agent collaboration.

## Contribution Guidelines

* Contributions such as code, documentation, and test cases are welcome.
* Please refer to the contribution guidelines for information on how to participate in the project.

## License

* This project is licensed under the [License Name] license.