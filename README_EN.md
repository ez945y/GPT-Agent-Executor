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

## Installation

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
4.  **Run the Project:**
    * `python main.py`

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