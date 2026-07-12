# ==========================================================
# Update
# ==========================================================

from pathlib import Path
import pandas as pd

def update(self, update_dir, keep="last"):

    update_dir = Path(update_dir)

    if not update_dir.exists():
        raise FileNotFoundError(update_dir)

    supported = {
        ".xls",
        ".xlsx",
        ".csv",
        ".txt",
        ".dat"
    }

    files = sorted([
        f for f in update_dir.iterdir()
        if f.suffix.lower() in supported
    ])

    if len(files) == 0:
        print("Nessun file trovato.")
        return {}

    report = {}

    for file in files:

        key = file.stem

        print(f"Aggiornamento {key}...")

        df_new = self._read_file(file)

        parquet_file = self.parquet_dir / f"{key}.parquet"

        if parquet_file.exists():

            df_old = pd.read_parquet(parquet_file)

            df = pd.concat(
                [df_old, df_new],
                ignore_index=True
            )

        else:

            df = df_new

        before = len(df)

        df = self._drop_duplicates(
            df,
            keep=keep
        )

        after = len(df)

        removed = before - after

        perc = 0.0

        if before > 0:
            perc = 100 * removed / before

        self._save_parquet(
            df,
            parquet_file
        )

        if removed > 0:

            print(
                f"Rimosse {removed} ({perc:.2f}%) "
                "delle righe dai dati letti."
            )

        report[key] = {
            "rows_before": before,
            "rows_after": after,
            "duplicates": removed,
            "removed_percent": perc
        }

    self._invalidate_cache()

    return report

def update_from_list(
    self,
    file_list,
    keep="last"
):

    report = {}

    for file in file_list:

        file = Path(file)

        key = file.stem

        print(f"Aggiornamento {key}...")

        df_new = self._read_file(file)

        parquet_file = self.parquet_dir / f"{key}.parquet"

        if parquet_file.exists():

            df_old = pd.read_parquet(parquet_file)

            df = pd.concat(
                [df_old, df_new],
                ignore_index=True
            )

        else:

            df = df_new

        before = len(df)

        df = self._drop_duplicates(
            df,
            keep=keep
        )

        after = len(df)

        removed = before - after

        perc = (
            100 * removed / before
            if before > 0 else 0
        )

        self._save_parquet(
            df,
            parquet_file
        )

        if removed > 0:

            print(
                f"Rimosse {removed} "
                f"({perc:.2f}%) "
                "delle righe dai dati letti."
            )

        report[key] = {
            "rows_before": before,
            "rows_after": after,
            "duplicates": removed,
            "removed_percent": perc
        }

    self._invalidate_cache()

    return report