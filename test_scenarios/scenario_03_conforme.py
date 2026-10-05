# Exigence simulée (ticket) : "Valider qu'un courriel est bien formé avant inscription"
# Attendu : code volontairement propre. L'agent ne devrait rien signaler de
# critique ou majeur ici — ce scénario sert à mesurer le taux de faux positifs.

import re

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$")

def est_courriel_valide(courriel: str) -> bool:
    if not courriel:
        return False
    return bool(EMAIL_PATTERN.match(courriel))
