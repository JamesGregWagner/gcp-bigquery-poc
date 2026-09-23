import pandas as pd

def transform_orders(df):

    df = df.copy()

    duplicates_lines_dropped = 0
    missing_values_dropped = 0

    # Renommer les colonnes pour correspondre aux conventions de nommage
    df = renaming_columns(df)

    # Standardiser les types de données
    df = standardize_data_types(df)

    # Standardiser les valeurs des colonnes de texte
    df = standardize_values(df)

    # Supprimer les doublons
    df, duplicates_lines_dropped = drop_duplicated_values(df)

    # Supprimer les lignes avec des valeurs manquantes
    df, missing_values_dropped = drop_missing_values(df)

    # Créer une nouvelle colonne "revenue"
    df = create_revenue_column(df)

    # Arrondir les colonnes numériques à 2 décimales
    df = round_numeric_columns(df)

    return df, duplicates_lines_dropped, missing_values_dropped

def renaming_columns(df):

    df = df.copy()

    COLUMN_MAPPING = {
        "order_id": "order_identifier",
        "customer_id": "customer_identifier",
        "product_id": "product_identifier",
        "category": "product_category"
    }

    df = df.rename(columns=COLUMN_MAPPING)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        )

    return df

def standardize_data_types(df):

    df = df.copy()

    # Convertir les colonnes en types de données appropriés
    df["order_date"] = pd.to_datetime(df["order_date"], errors='coerce')
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors='coerce')
    df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce')

    return df

def standardize_values(df):

    df = df.copy()

    # Standardiser les valeurs des colonnes de texte
    text_columns = [
    "product_name",
    "product_category",
    "country"
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    # Standardiser les valeurs de la colonne "country" 
    # en mettant la première lettre en majuscule et le reste en minuscule
    df["country"] = df["country"].str.title()

    return df

def drop_duplicated_values(df):

    df = df.copy()

    # Supprimer les doublons
    rows_before = len(df)

    df = df.drop_duplicates()

    rows_after = len(df)

    duplicates_removed = rows_before - rows_after

    # Afficher le nombre de doublons supprimés
    print(f"Nombre de doublons supprimés : {duplicates_removed}")

    return df, duplicates_removed

def drop_missing_values(df):

    df = df.copy()

    # Définir les colonnes obligatoires pour l'analyse de qualité des données
    mandatory_columns = [
    "order_identifier",
    "order_date",
    "customer_identifier",
    "product_identifier",
    "quantity",
    "unit_price"
    ]

    # Supprimer les lignes avec des valeurs manquantes
    rows_before = len(df)

    df = df.dropna(subset=mandatory_columns)

    rows_after = len(df)

    missing_values_removed = rows_before - rows_after

    # Afficher le nombre de lignes supprimées
    print(f"Nombre de lignes supprimées avec des valeurs manquantes : {missing_values_removed}")

    return df, missing_values_removed

def create_revenue_column(df):

    df = df.copy()

    # Créer une nouvelle colonne "revenue" en multipliant "unit_price" par "quantity"
    df["revenue"] = df["unit_price"] * df["quantity"]

    return df

def round_numeric_columns(df):

    df = df.copy()

    columns = ["unit_price", "revenue"]

    # Arrondir les colonnes numériques spécifiées à un certain nombre de décimales
    for column in columns:
        if column in df.columns:
            df[column] = df[column].round(2)

    return df

def run_staging_quality_checks(df, duplicates_lines_dropped, missing_values_dropped):

    report = {}

    # Construire le rapport de qualité des données pour la couche STAGING
    report["rows"] = len(df)
    report["layer"] = "STAGING"
    report["columns"] = len(df.columns)
    report["duplicates"] = int(df.duplicated().sum())
    report["missing_values"] = int(df.isnull().any(axis=1).sum())
    report["invalid_prices"] = int((df["unit_price"] < 0).sum())
    report["invalid_quantities"] = int((df["quantity"] <= 0).sum())
    report["invalid_dates"] = int(df["order_date"].isnull().sum())
    report["duplicates_lines_dropped"] = duplicates_lines_dropped
    report["missing_values_removed"] = missing_values_dropped

    return report