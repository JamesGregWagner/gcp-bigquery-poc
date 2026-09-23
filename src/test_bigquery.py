
from google.cloud import bigquery

# Création du client BigQuery
client = bigquery.Client()

print("Connexion à BigQuery réussie !")
print(f"Projet utilisé : {client.project}")

# Requête SQL de test
query = """
SELECT
    1 AS test_value,
    CURRENT_DATE() AS execution_date
"""

# Exécution de la requête
query_job = client.query(query)

# Récupération du résultat
results = query_job.result()

# Affichage du résultat
for row in results:
    print(f"Valeur de test : {row.test_value}")
    print(f"Date d'exécution : {row.execution_date}")
