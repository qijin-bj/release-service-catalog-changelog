name: Run Ollama AI Agent

on:
  workflow_dispatch:
  pull_request:
    branches: [development]

jobs:
  ollama-agent:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Cache Ollama models
        uses: actions/cache@v3
        with:
          path: ~/.ollama
          key: ollama-models-${{ runner.os }}

      - name: Set up Docker
        uses: docker/setup-buildx-action@v3

      - name: Pull Ollama image
        run: docker pull ollama/ollama

      - name: Start Ollama container
        run: |
          docker run -d --name ollama \
            -p 11434:11434 \
            -v ~/.ollama:/root/.ollama \
            ollama/ollama

      - name: Wait for Ollama to be ready
        run: |
          echo "Waiting for Ollama to start..."
          for i in {1..20}; do
            curl -s http://localhost:11434/api/tags && break || sleep 3
          done

      - name: Pull model
        run: curl http://localhost:11434/api/pull -d '{"name": "llama3"}' -H "Content-Type: application/json"

      - name: Install Python dependencies
        run: pip install requests

      - name: Run LLM agent
        run: python ollama_prompt.py

