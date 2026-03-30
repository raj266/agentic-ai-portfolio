import requests
import time

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi3:mini"          # or llama3.2:3b
TIMEOUT = 360
DEBUG = False

def call_ollama(prompt, node_name="unknown"):
    print(f"🐛 [{node_name}] Calling Ollama...", flush=True)
    start = time.time()
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": 0, "num_predict": 128}
            },
            timeout=TIMEOUT
        )
        elapsed = time.time() - start
        print(f"🐛 [{node_name}] Ollama responded in {elapsed:.2f}s", flush=True)
        return resp.json()["message"]["content"]
    except Exception as e:
        elapsed = time.time() - start
        print(f"🐛 [{node_name}] Error after {elapsed:.2f}s: {e}", flush=True)
        return f"Error: {e}"