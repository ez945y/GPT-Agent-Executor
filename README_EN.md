# GPT Agent Executor: Enabling Autonomous Collaboration and Continuous Operation

## 🚀 Quick Start

1. **Install Dependencies:** `./install_requirements.sh` (Linux/Mac) or `install_requirements.bat` (Windows)
2. **One-Click Launch:** `./start.sh` (Linux/Mac) or `start.bat` (Windows)



---

# Project Description

[中文版](README.md)

This project aims to build an autonomous agent framework based on GPT, enabling the continuous operation and collaboration of intelligent agents.

Through modular design, we decompose the intelligent agent into three core modules:

* **Think Agent:** Responsible for analyzing goals, planning tasks, and generating action plans.
* **Tool Agent:** Based on the decisions of the Think Agent, it calls external tools or APIs to execute specific tasks.
* **Target Agent:** Observes its own thoughts, determines what tool to use, and returns a target.

Additionally, this project provides a user-friendly interactive interface and supports multiple language model backends such as Ollama, Gemini API, and OpenAI API, allowing you to choose the most suitable model according to your needs.

## Project Features

* **Autonomous Operation:** The intelligent agent can autonomously plan and execute tasks based on goals without human intervention.
* **Modular Design:** The three core modules perform their respective duties, facilitating expansion and maintenance.
* **Multi-Model Support:** Supports multiple language model backends such as Ollama, Gemini API, and OpenAI API, providing flexible choices.
* **Visual Language Model (VLM):** Supports image understanding and analysis, can process image input.
* **Intelligent Tool Integration:** Built-in web search, content summarization, natural expression, and other tools.
* **Command Line Interface:** Provides CLI client and modern command-line interface.
* **Real-time Monitoring:** Real-time display of AI thinking process and conversation status.
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
    * Supported tools: web search, content summarization, natural expression, etc.
* **Target Agent:**
    * Observes its own thoughts, determines what tool to use, and returns a target.
    * Returns the target to the Think Agent.
* **User Interaction:**
    * Provides command-line interface (CLI).
    * Allows users to set goals, view progress, and interact with the intelligent agent.
    * Real-time monitoring of AI thinking process.
* **Model Backend:**
    * Supports Ollama, Gemini API, and OpenAI API.
    * Supports Visual Language Model (VLM) functionality.
    * Allows users to choose models according to their needs.

## Supported Models

### Ollama Models
- Local deployment, no API key required
- Supports VLM models (such as qwen2.5vl)
- Completely offline operation

### Gemini API
- Google's Gemini models
- Requires API key
- Supports text generation

### OpenAI API
- OpenAI's GPT series models
- Supports custom API endpoints (proxy)
- Supports VLM functionality
- Configuration format: `openai@https://your-proxy-url/v1`

## Built-in Tools

### Web Search
- Uses Google Search API
- Automatically retrieves web page content
- Returns title, summary, and full content

### Content Summarization
- Intelligent summarization of long text content
- Extracts key information

### Natural Expression
- Converts AI thinking into natural language expression
- More humanized responses

### Goal Management
- Observes and sets goal lists
- Tracks task progress

## Use Cases

* **Automated Task Execution:** Automatically executes tasks such as data collection, report generation, and code writing.
* **Intelligent Assistant:** Provides services such as personal assistant, customer service, and knowledge Q&A.
* **Image Analysis:** Uses VLM models to analyze image content.
* **Research and Development:** Used to explore intelligent agent behavior and test language model capabilities.

## Installation and Launch

### Step 1: Install Dependencies (Required for First Use)

**macOS/Linux:**
```bash
./install_requirements.sh
```

**Windows:**
```cmd
install_requirements.bat
```

Or install manually:
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables (Optional)

See the "Configuration Instructions" section below for details.

### Step 3: Launch Services

#### Method 1: One-Click Launch (Recommended)

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

These scripts will automatically:
- Check if dependencies are installed
- Check and start the server (in a new window)
- Launch the chat client (in the current window)
- Wait for the server to be ready



#### Method 2: Manual Launch

1.  **Start Server:**
    ```bash
    python start_server.py
    ```

2.  **Use Client:**
    ```bash
    python cli_client.py
    ```

## Interface Features

### CLI Client
- **Unified Interface:** Auto-monitoring, real-time status display
- **Simplified Commands:** Use `+` symbol to send messages
- **Monitoring Features:** Real-time display of AI thinking process
- **Complete Functions:** Support all API endpoints

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

### 4. VLM Function Test
```bash
# Test visual language model
python vlm_test.py "https://example.com/image.jpg" "Describe this image"
```

## API Endpoints

### CLI API (`/cli`)
- `POST /cli/start_conversation` - Start conversation
- `POST /cli/send_message` - Send message
- `GET /cli/conversations` - Get conversation list
- `GET /cli/conversation/{id}` - Get conversation content
- `GET /cli/cache_pool` - Get cache pool
- `GET /cli/status` - Get system status
- `POST /cli/stop_conversation` - Stop conversation

### WebSocket API (`/ws`)
- Real-time bidirectional communication
- Supports CLI client



## Monitoring Function Details

### Auto-Monitoring
- Automatically starts background monitoring when client launches
- Real-time display of AI think output
- Does not affect normal command input

### Monitoring Content
- **Normal Mode:** Only displays `{"思考": "content"}` output
- **Verbose Mode:** Displays all cache pool content

For monitoring commands, see the "Command List" section above.

## Configuration Instructions

### Environment Variable Configuration
Create a `.env` file:

```bash
# API Keys
SERP_API_KEY=your-serp-api-key
GEMINI_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key

# Model Configuration
THINK_MODEL_NAME=gemini-flash-2.0
THINK_MODEL_TYPE=gemini
TARGET_MODEL_NAME=gemini-flash-2.0
TARGET_MODEL_TYPE=gemini
TOOL_MODEL_NAME=gemini-flash-2.0
TOOL_MODEL_TYPE=gemini

# Feature Switches
SUPPORT_IMAGE=false

# Interval Settings (seconds)
THINK_INTERVAL=6
TARGET_INTERVAL=60
TOOL_INTERVAL=15
```

### Model Configuration Examples
```bash
# Ollama Model
THINK_MODEL_TYPE=ollama
THINK_MODEL_NAME=qwen2.5vl:3b

# Gemini Model
THINK_MODEL_TYPE=gemini
THINK_MODEL_NAME=gemini-pro
GEMINI_API_KEY=your-api-key

# OpenAI Model
THINK_MODEL_TYPE=openai@https://your-proxy-url/v1
THINK_MODEL_NAME=gpt-4o
OPENAI_API_KEY=your-api-key
```

## Important Notes

1. Ensure the server is running (`uvicorn main:app`)
2. CLI client will automatically check server status
3. Monitoring function runs in background, does not affect command input
4. Use `Ctrl+C` to exit program
5. All conversations and thinking will be logged to log files
6. VLM functionality requires supported models (such as qwen2.5vl)
7. Web search functionality requires SerpAPI key
8. CLI client requires Python environment
9. Environment variable configuration takes precedence over default values in code

## Troubleshooting

### Server Connection Failure
```bash
# Check if server is running
curl http://127.0.0.1:8000/cli/status

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Python Environment Issues
```bash
# Install dependencies
./install_requirements.sh

# Or install manually
pip install -r requirements.txt

# Or use conda
conda install requests fastapi uvicorn
```

### Permission Issues
```bash
# Give execution permission to startup scripts
chmod +x start_chat.sh
```

### VLM Model Issues
```bash
# Check if Ollama model is installed
ollama list

# Install VLM model
ollama pull qwen2.5vl:3b
```


### API Key Issues
- Ensure API keys are correctly configured in `.env` file
- Check network connection and API endpoint availability
- Verify API key validity

### Environment Variable Issues
- Ensure `.env` file is in project root directory
- Check if variable names are correct
- Restart server to load new environment variables

## Future Directions

* Add support for more tools and APIs.
* Optimize the learning and reasoning capabilities of the intelligent agent.
* Develop richer user interaction interfaces.
* Explore multi-agent collaboration.
* Enhance VLM functionality support.

## Contribution Guidelines

* Contributions such as code, documentation, and test cases are welcome.
* Please refer to the contribution guidelines for information on how to participate in the project.

## License

* This project is licensed under the [License Name] license.