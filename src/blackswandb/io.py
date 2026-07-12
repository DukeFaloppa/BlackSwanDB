# ==========================================================
# I/O
# ==========================================================
import pandas as pd

def read_file(self, file):

    ext = file.suffix.lower()

    if ext in [".xls", ".xlsx"]:

        df = pd.read_excel(file)

    elif ext == ".csv":

        df = pd.read_csv(file,sep=';')

    elif ext in [".txt", ".dat"]:

        try:

            df = pd.read_csv(file)

        except Exception:

            df = pd.read_csv(
                file,
                sep=None,
                engine="python"
            )

    else:

        raise ValueError(
            f"Formato non supportato: {ext}"
        )

    return df.convert_dtypes()

def drop_duplicates(
    self,
    df,
    keep="last"
):

    return df.drop_duplicates(
        keep=keep,
        ignore_index=True
    )

def save_parquet(
    self,
    df,
    filename
):

    df.to_parquet(
        filename,
        engine="pyarrow",
        compression="snappy",
        index=False
    )