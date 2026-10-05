# Exigence simulée (ticket) : "Récupérer les commandes d'un client par ID"
# Attendu : l'agent sécurité doit signaler une injection SQL critique.

import sqlite3

def get_user_orders(user_id, db_path="orders.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM orders WHERE user_id = " + user_id
    cursor.execute(query)
    return cursor.fetchall()
