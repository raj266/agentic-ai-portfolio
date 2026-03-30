from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.constants import Send
from tools import search_listings, calculate_total_cost, check_connectivity, check_legal_status
from prompts import legal_prompt, budget_prompt, location_prompt
from call_ollama import call_ollama

class AgentState(TypedDict):
    query: str
    legal_opinion: str
    budget_opinion: str
    location_opinion: str
    final_answer: str

def legal_node(state: AgentState):
    print("\n⚖️ Entering LEGAL node")
    location = "Whitefield"
    legal_status = check_legal_status(location)
    prompt = legal_prompt(legal_status, state["query"])
    opinion = call_ollama(prompt, node_name="LEGAL")
    return {"legal_opinion": opinion}

def budget_node(state: AgentState):
    print("\n💰 Entering BUDGET node")
    listings = search_listings(2, 5, 3)
    if listings:
        top = listings[0]
        cost = calculate_total_cost(top["price_cr"])
        factual = f"Example property: {top['name']} at ₹{top['price_cr']} Cr. Total cost with taxes: ₹{cost['total']} Cr."
    else:
        factual = "No properties found in the given budget range."
    prompt = budget_prompt(factual, state["query"])
    opinion = call_ollama(prompt, node_name="BUDGET")
    return {"budget_opinion": opinion}

def location_node(state: AgentState):
    print("\n📍 Entering LOCATION node")
    location = "Whitefield"
    connectivity = check_connectivity(location)
    prompt = location_prompt(connectivity, state["query"])
    opinion = call_ollama(prompt, node_name="LOCATION")
    return {"location_opinion": opinion}

def resolver_node(state: AgentState):
    print("\n🔧 Entering RESOLVER node")
    legal = state["legal_opinion"]
    budget = state["budget_opinion"]
    location = state["location_opinion"]

    if "LEGAL VETO:" in legal:
        final = f"❌ LEGAL VETO:\n{legal.split('LEGAL VETO:')[-1].strip()}"
    else:
        final = f"""**Legal Opinion:** {legal}

**Budget Opinion:** {budget}

**Location Opinion:** {location}

**Conclusion:** Based on the above, review all factors before making a decision."""
    return {"final_answer": final}

# ------------------------------------------------------------------
# Parallel fan‑out
# ------------------------------------------------------------------
def fan_out_to_specialists(state: AgentState):
    return [
        Send("legal", state),
        Send("budget", state),
        Send("location", state),
    ]

def build_graph(mode: str = "parallel"):
    """
    Build a LangGraph that can run specialists sequentially or in parallel.
    mode = "sequential" or "parallel"
    """
    graph = StateGraph(AgentState)

    # Add all nodes
    graph.add_node("legal", legal_node)
    graph.add_node("budget", budget_node)
    graph.add_node("location", location_node)
    graph.add_node("resolver", resolver_node)

    if mode == "sequential":
        graph.set_entry_point("legal")
        graph.add_edge("legal", "budget")
        graph.add_edge("budget", "location")
        graph.add_edge("location", "resolver")
        graph.add_edge("resolver", END)

    elif mode == "parallel":
        graph.add_node("start", lambda s: s)   # dummy node
        graph.set_entry_point("start")
        graph.add_conditional_edges(
            "start",
            fan_out_to_specialists,
            ["legal", "budget", "location"]
        )
        graph.add_edge("legal", "resolver")
        graph.add_edge("budget", "resolver")
        graph.add_edge("location", "resolver")
        graph.add_edge("resolver", END)

    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'sequential' or 'parallel'.")

    return graph.compile()