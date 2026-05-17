import pandas as pd


def merge_datasets(df_cpcb, df_gee):

    # ---------------------------------
    # Standardize district names
    # ---------------------------------
    df_cpcb["district"] = (
        df_cpcb["district"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df_gee["district"] = (
        df_gee["district"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # ---------------------------------
    # Standardize dates
    # ---------------------------------
    df_cpcb["date"] = pd.to_datetime(
        df_cpcb["date"],
        errors="coerce"
    ).dt.date

    df_gee["date"] = pd.to_datetime(
        df_gee["date"],
        errors="coerce"
    ).dt.date

    # ---------------------------------
    # Drop redundant columns from CPCB
    # ---------------------------------
    # We want to keep GEE's coordinates (lat/lon)
    df_cpcb = df_cpcb.drop(columns=["lat", "lon"], errors="ignore")

    # ---------------------------------
    # LEFT MERGE
    # KEEP ALL GEE ROWS
    # ---------------------------------
    merged_df = pd.merge(
        df_gee,          # LEFT DATASET = KEEP ALL ROWS
        df_cpcb,
        on=["district", "date"],
        how="left"       # KEEP ALL SATELLITE ROWS
    )

    # ---------------------------------
    # Save output
    # ---------------------------------
    merged_df.to_csv(
        "data/final/merged_dataset.csv",
        index=False
    )

    print("\nDatasets merged successfully!")
    print(f"Final rows: {len(merged_df)}")
    print(f"Columns: {list(merged_df.columns)}")

    return merged_df