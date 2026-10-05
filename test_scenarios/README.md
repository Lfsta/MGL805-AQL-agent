# Scénarios de test — notre repo comme sujet de test

Faute d'accès à une instance Jira, nous utilisons les **Issues GitHub de ce repo**
comme substitut aux tickets. Chaque scénario ci-dessous correspond à une Issue
réelle à créer dans l'onglet *Issues*, avec une PR liée (conforme ou non) pour
valider que l'agent détecte correctement les écarts.

## Comment ajouter un scénario

1. Créez une Issue avec le gabarit `ticket-simule` (voir `.github/ISSUE_TEMPLATE/`).
2. Créez une branche, modifiez/ajoutez un fichier Python illustrant le scénario.
3. Ouvrez une PR qui référence l'Issue (`Closes #<numéro>` dans la description).
4. Ajoutez une entrée dans `attendus.md` décrivant ce que l'agent *devrait* trouver.
5. Lancez `python agents.py <fichier>` et comparez le résultat à `attendus.md`.

## Scénarios fournis au démarrage

| # | Fichier | Exigence simulée | Ce qui doit être détecté |
|---|---|---|---|
| 1 | `scenario_01_injection_sql.py` | "Récupérer les commandes d'un client par ID" | Injection SQL (sécurité, critique) |
| 2 | `scenario_02_logique_remise.py` | "Appliquer une remise croissante selon le montant total" | Branche `elif` inatteignable (qualité, majeur) |
| 3 | `scenario_03_conforme.py` | "Valider qu'un courriel est bien formé avant inscription" | Aucun problème majeur — sert à mesurer les faux positifs |

Le scénario 3 est volontairement propre : un bon agent ne doit rien signaler
de critique dessus. C'est votre test de référence pour le taux de faux positifs.
