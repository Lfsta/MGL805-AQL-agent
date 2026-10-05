"""
Fichier d'exemple à réviser — le même snippet utilisé dans nos tests manuels.
Contient volontairement : une injection SQL, une connexion non fermée,
une erreur de logique (elif inatteignable), et une boucle non idiomatique.
"""

import sqlite3

def get_user_orders(user_id, db_path="orders.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM orders WHERE user_id = " + user_id
    cursor.execute(query)
    results = cursor.fetchall()

    total = 0
    for i in range(len(results)):
        total += results[i][2]

    discount = 0
    if total > 100:
        discount = 0.1
    elif total > 500:
        discount = 0.2

    final_total = total - (total * discount)
    return final_total
