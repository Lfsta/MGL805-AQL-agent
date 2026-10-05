"""
Prototype minimal : 2 agents spécialistes (qualité, sécurité) orchestrés avec LangGraph,
exécutés sur un modèle local via Ollama. Chaque agent charge ses instructions depuis
un fichier .md séparé dans skills/ — c'est notre équivalent "skill" pour un modèle local.

Usage :
    python agents.py sample_pr.py
"""

import os
import sys
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END

# Loads .env if it exists
load_dotenv()

# Configurable par variable d'environnement pour que chaque coéquipier puisse
# utiliser le modèle installé sur sa propre machine sans modifier le code.
MODEL_NAME = os.environ.get("AQL_MODEL", "qwen3:8b")

# IMPORTANT : Ollama tronque silencieusement le contexte à une valeur par
# défaut souvent trop petite (2048-4096 tokens) pour un diff de PR réel.
# On la fixe explicitement ici. Augmenter cette valeur consomme plus de VRAM
# (le cache KV grandit avec le contexte) — 8192 est un compromis raisonnable
# pour une carte 6-8 Go. Ajustez via la variable d'environnement au besoin.
NUM_CTX = int(os.environ.get("AQL_NUM_CTX", "8192"))

# Adresse du serveur Ollama — utile si Ollama ne tourne pas en local par défaut
# (ex. machine d'un coéquipier sur le réseau, port personnalisé).
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

SKILLS_DIR = Path(__file__).parent / "skills"


def load_skill(name: str) -> str:
    return (SKILLS_DIR / name).read_text(encoding="utf-8")


# --- État partagé entre les nœuds du graphe ---
class ReviewState(TypedDict):
    code: str
    rapport_qualite: str
    rapport_securite: str


# --- Un seul LLM, réutilisé par les deux agents (juste le prompt système change) ---
llm = ChatOllama(model=MODEL_NAME, temperature=0.1, num_ctx=NUM_CTX, base_url=OLLAMA_HOST)


def agent_qualite(state: ReviewState) -> dict:
    system_prompt = load_skill("qualite.md")
    messages = [
        ("system", system_prompt),
        ("human", f"Voici le code à réviser :\n\n```python\n{state['code']}\n```"),
    ]
    response = llm.invoke(messages)
    return {"rapport_qualite": response.content}


def agent_securite(state: ReviewState) -> dict:
    system_prompt = load_skill("securite.md")
    messages = [
        ("system", system_prompt),
        ("human", f"Voici le code à réviser :\n\n```python\n{state['code']}\n```"),
    ]
    response = llm.invoke(messages)
    return {"rapport_securite": response.content}


# --- Construction du graphe : les deux agents tournent indépendamment, en parallèle ---
graph = StateGraph(ReviewState)
graph.add_node("agent_qualite", agent_qualite)
graph.add_node("agent_securite", agent_securite)

graph.set_entry_point("agent_qualite")
graph.set_entry_point("agent_securite")
graph.add_edge("agent_qualite", END)
graph.add_edge("agent_securite", END)

app = graph.compile()


def main():
    if len(sys.argv) < 2:
        print("Usage : python agents.py <fichier_a_reviser.py>")
        sys.exit(1)

    code_path = Path(sys.argv[1])
    code = code_path.read_text(encoding="utf-8")

    result = app.invoke({"code": code, "rapport_qualite": "", "rapport_securite": ""})

    print("\n" + "=" * 60)
    print("RAPPORT — AGENT QUALITÉ")
    print("=" * 60)
    print(result["rapport_qualite"])

    print("\n" + "=" * 60)
    print("RAPPORT — AGENT SÉCURITÉ")
    print("=" * 60)
    print(result["rapport_securite"])


if __name__ == "__main__":
    main()
