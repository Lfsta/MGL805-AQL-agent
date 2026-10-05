# Agents de revue de code libres de droits (LangGraph + Ollama)

Prototype d'agents de revue de code assistée par IAG, construit exclusivement
avec des modèles et outils libres de droits (licences MIT/Apache 2.0), dans le
cadre du cours MGL805. 

## Le projet en une phrase

Deux agents spécialistes (qualité, sécurité), chacun piloté par un fichier
`.md` indépendant agissant comme "skill", orchestrés avec LangGraph et
exécutés **entièrement en local** via Ollama — sans dépendance à une API
payante.

## Prérequis

- Python 3.10+
- [Ollama](https://ollama.com) installé et lancé
- ~6 Go de VRAM libre (voir [note matériel](#note-matériel) plus bas)

## Installation

```bash
git clone https://github.com/Lfsta/MGL805-AQL-agent.git
cd MGL805-AQL-agent

python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt

ollama pull qwen3:8b

cp .env.example .env    # ajustez AQL_MODEL/AQL_NUM_CTX au besoin
```

## Utilisation

```bash
python agents.py test_scenarios/scenario_01_injection_sql.py
```

Vous obtenez deux rapports indépendants (qualité, sécurité). Testez aussi les
scénarios 2 et 3 dans `test_scenarios/` pour voir la détection d'un bug de
logique et la gestion d'un cas sans problème (contrôle du taux de faux positifs).

### Changer de modèle ou de taille de contexte

Modifiez votre `.env` (recommandé, persiste entre les runs) :
```
AQL_MODEL=qwen2.5-coder:7b
AQL_NUM_CTX=16384
```

Ollama tronque silencieusement le contexte à une valeur par défaut trop petite (souvent 4096 tokens) pour un diff de PR réel — le code fixe `num_ctx`
explicitement pour éviter ce piège. Augmenter cette valeur coûte de la VRAM.

## Structure du dépôt

```
agents.py              Graphe LangGraph (2 agents en parallèle)
skills/
  qualite.md            Instructions de l'agent qualité
  securite.md            Instructions de l'agent sécurité
test_scenarios/         Cas de test + grille de résultats attendus
.github/
  ISSUE_TEMPLATE/        Gabarit de "ticket simulé" (substitut Jira)
  pull_request_template.md
```

## Pourquoi pas Jira ?

Faute d'accès étudiant gratuit à une instance Jira, ce projet utilise les
**Issues de ce dépôt GitHub** comme substitut aux tickets. Le dépôt sert donc
à la fois de code source du projet et de sujet de test pour valider le
mécanisme de vérification « cohérence ticket ↔ implémentation » décrit dans
le rapport d'équipe. Voir `test_scenarios/README.md` pour la méthodologie
complète et comment ajouter un nouveau scénario.

## Note matériel

Testé sur RTX 3070 (6 Go et 8 Go VRAM) avec `qwen3:8b`
(~5-6 Go VRAM). 

## Pour continuer ce projet

- [ ] Ajouter plus d'agents (Analyse Jira/github issues, analyse de code, conformité fonctionnelle)
- [ ] Ajouter un nœud de synthèse qui fusionne les rapports qualité/sécurité/autres
- [ ] Automatiser le déclenchement via GitHub Actions sur ouverture de PR
- [ ] Étendre `test_scenarios/` et automatiser le calcul précision/rappel/faux positifs
