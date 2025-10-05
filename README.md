# 🤖 Local AI Chat Agent using Microsoft [Agent Framework ](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview)integrated with [Docker Model Runner (DMR)](https://www.docker.com/blog/run-llms-locally/) local model inference.

A lightweight example demonstrating how to run a **local AI chat agent** powered by [Agent Framework](https://pypi.org/project/agent-framework/) and OpenAI’s Python SDK — fully integrated with **Docker Model Runner (DMR)** for **offline LLM inference**.

This project uses a clean, modular design:
- Configurations stored in a `.env` file  
- Centralized logging via `logger_config.py`  
- Async and streaming chat responses  
- Local inference (**no cloud API required**)

---

## 🧠 Overview

This example shows how to:

- Connect to a **locally hosted LLM** (via Docker Model Runner)  
- Build an **agent** with specific behavioral instructions  
- Execute both **non-streaming** and **streaming** chat interactions  
- Manage configuration and logs in a clean, reusable way  

---

## 🧩 Project Structure

```

📦 local-ai-agent/
├── main.py                # Main script (agent setup + interactions)
├── logger_config.py       # Centralized logging configuration
├── .env                   # Environment configuration (model, URLs, retries, etc.)
├── requirements.txt       # Python dependencies
└── logs/                  # Directory where logs are saved

````

---

## ⚙️ Requirements (my tested environments)

- **Python 3.11**
- **Docker Desktop 4.47.0** (with Model Runner enabled)
- The following Python packages:

```bash
pip install -r requirements.txt
````

**requirements.txt**

```txt
agent-framework
openai
python-dotenv
```

---

## 🔐 Environment Configuration (`.env`)

All app settings are stored in `.env` for easier customization.

```bash
# Docker Model Runner Settings
DMR_BASE_URL=http://localhost:12434/engines/llama.cpp/v1
MODEL_ID=ai/smollm2:latest

# Agent Instructions
AGENT_INSTRUCTIONS=You are good at telling short, simple, and funny jokes.

# Retry Settings
MAX_RETRIES=3
RETRY_DELAY=3

# Logging Settings
LOG_DIR=logs
LOG_FILE=agent.log
```

You can change the model, behavior, or retry settings here without touching the code.

---

## 🐳 Docker Setup

Before running the agent, ensure your **Docker Model Runner (DMR)** is active and a model is available.

```bash
# 1️⃣ Enable Model Runner service
docker desktop enable model-runner --tcp 12434

# 2️⃣ Pull a local model (example: smollm2)
docker model pull ai/smollm2:latest
```

---

## 🚀 Run the Example

Start the app:

```bash
python main.py
```

**Expected Output Example:**

```
Agent created and running with a local model via DMR.
Non-Streaming Invocation:
Why don’t pirates take baths? Because they just wash up on shore!
Streaming Invocation:
Why don’t pirates take baths? Because they just wash up on shore!
```

Logs will also be saved in:

```
logs/agent.log
```

---

## 🧱 How It Works

### 1. Environment Variables Loaded

```python
from dotenv import load_dotenv
load_dotenv()
```

### 2. Local Model Connection

```python
local_client = AsyncOpenAI(
    api_key="dummy_key",
    base_url=os.getenv("DMR_BASE_URL")
)
```

### 3. Agent Setup

```python
chat_client = OpenAIChatClient(
    async_client=local_client,
    model_id=os.getenv("MODEL_ID")
)

async with ChatAgent(
    chat_client=chat_client,
    instructions=os.getenv("AGENT_INSTRUCTIONS")
) as agent:
    result = await agent.run("Tell me a joke about a pirate.")
```

### 4. Logging

All events are logged to both console and `logs/agent.log` via `logger_config.py`.

---

## 🧰 Key Features

| Feature               |                                       Description                                       |
| --------------------- | ------------------------------------------------- |
| 🧠 Agent Framework    | Easy behavioral control with instructions         
| 🐳 Local Inference    | Runs models locally through Docker                |
| ⚡ Async + Streaming   | Real-time response streaming support              |
| 🧩 Modular design     | `.env` for config, `logger_config.py` for logging 
| 🧾 Structured Logging | Console + file logging with timestamps            |

---

## 🧭 Next Steps

* Replace `ai/smollm2:latest` with your preferred model
* Extend the agent with memory or external tool integration
* Add more `.env` configs (e.g., multiple model endpoints)
* Use different agent “roles” for creative applications

---

## 📜 License

**  **.

---

### 💬 Author

**Tarak Chandra Sarkar** — [GitHub](https://github.com/Tarak-Chandra-Sarkar)

---

> 🧠 *“Run your AI locally, stay private, and keep it funny!”*

