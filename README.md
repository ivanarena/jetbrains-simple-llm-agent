# Simple LLM-based agent

[![Pylint Score](https://img.shields.io/badge/pylint-10-brightgreen.svg)](https://pylint.pycqa.org)

<!-- [![Mypy Status](https://img.shields.io/badge/mypy-passed-brightgreen.svg)](http://mypy-lang.org) -->

# Requirements

To set up and run the server, you need the following:

- Python 3.8 or higher
- Poetry for dependency management

# Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd jetbrains-simple-llm-agent
   ```

2. **Install dependencies using Poetry:**

   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

# Running the Server

1. **Start the FastAPI server:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **The server will be running at:**
   ```
   http://0.0.0.0:8000/
   ```

# Usage

To interact with the agent, send a POST request to `/agent` with a JSON payload containing the `msg` field. For example:

```bash
curl -X POST "http://0.0.0.0:8000/agent" -H "Content-Type: application/json" -d '{"msg": "What directory are you in?"}'
```
