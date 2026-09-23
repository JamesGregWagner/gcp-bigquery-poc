from google.cloud import bigquery


def load_dataframe_to_bigquery(
    df,
    project_id,
    dataset_id,
    table_id
):

    client = bigquery.Client(
        project=project_id
    )

    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=(
            bigquery.WriteDisposition.WRITE_TRUNCATE
        )
    )

    load_job = client.load_table_from_dataframe(
        df,
        table_ref,
        job_config=job_config
    )

    load_job.result()

    print(
        f"Chargement terminé : {table_ref}"
    )

    table = client.get_table(table_ref)

    print(
        f"Nombre de lignes dans BigQuery : "
        f"{table.num_rows}"
    )