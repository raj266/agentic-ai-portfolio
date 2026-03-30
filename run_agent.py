from langgraph_agent import build_graph

if __name__ == "__main__":
    print("\n🏠 Agentic AI Portfolio – Priority Multi‑Agent")
    query = input("\nYour query: ").strip()
    if not query:
        query = "Find me a 3BHK in Whitefield under 5 Crore"
    print(f"\n🎯 {query}\n")

    app = build_graph()
    initial_state = {
        "query": query,
        "legal_opinion": "",
        "budget_opinion": "",
        "location_opinion": "",
        "final_answer": ""
    }

    final = app.invoke(initial_state)
    print("\n✅ FINAL ANSWER\n", final["final_answer"])