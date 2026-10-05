# Exigence simulée (ticket) : "Appliquer une remise de 10% pour un achat > 100$
# et de 20% pour un achat > 500$"
# Attendu : l'agent qualité doit signaler que la branche elif (> 500) est
# inatteignable, car la condition précédente (> 100) la capture toujours en premier.

def calculer_remise(total):
    discount = 0
    if total > 100:
        discount = 0.1
    elif total > 500:
        discount = 0.2
    return total - (total * discount)
