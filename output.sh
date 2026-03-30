# Sequential mode
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Find me a 3BHK in Whitefield under 5 Crore", "mode": "sequential"}'

# Parallel mode
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Find me a 3BHK in Whitefield under 5 Crore", "mode": "parallel"}'