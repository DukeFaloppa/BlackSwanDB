# ==========================================================
# Utilities
# ==========================================================

def close(self):
    self.con.close()

def _dataset_sql(self):

    return f"""
    (
        SELECT *,
                regexp_extract(filename,'([^/]+)\\.parquet$',1) AS key
        FROM read_parquet(
            '{self.parquet_dir.as_posix()}/*.parquet',
            filename=true
        )
    )
    """

def _execute(self, sql):

    sql = sql.replace("FROM data", f"FROM {self._dataset_sql()} AS data")

    return self.con.execute(sql)

def _invalidate_cache(self):

    self._keys = None
    self._columns = None

# ==========================================================
# Cache
# ==========================================================

def refresh(self):
    """
    Invalida la cache interna.
    """

    self._invalidate_cache()


# ==========================================================
# Context manager
# ==========================================================

def __enter__(self):

    return self

def __exit__(self, exc_type, exc_value, traceback):

    self.close()

# ==========================================================
# Magic methods
# ==========================================================

def __len__(self):

    return self.count()

def __repr__(self):

    try:

        nkeys = len(self.keys())
        nrows = self.count()
        ncols = len(self.columns())

    except Exception:

        return "BlackSwanDB(empty)"

    return (
        "BlackSwanDB("
        f"keys={nkeys}, "
        f"columns={ncols}, "
        f"rows={nrows}"
        ")"
    )

# ==========================================================
# Maintenance
# ==========================================================

def vacuum(self):
    """
    Compatta il database DuckDB.
    """

    self.con.execute("VACUUM")