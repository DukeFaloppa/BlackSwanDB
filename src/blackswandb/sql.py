# ==========================================================
# Metadata
# ==========================================================

def _execute(self, sql):

    sql = sql.replace("FROM data", f"FROM {self._dataset_sql()} AS data")

    return self.con.execute(sql)

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


def keys(self):

    if self._keys is None:

        q = """
        SELECT DISTINCT key
        FROM data
        ORDER BY key
        """

        self._keys = [
            r[0]
            for r in self._execute(q).fetchall()
        ]

    return self._keys.copy()

def schema(self):

    q = """
    DESCRIBE
    SELECT *
    FROM data
    """

    return self._execute(q).df()

def columns(self):

    if self.columns is None:

        self.columns = list(
            self.schema()["column_name"]
        )

    return self.columns.copy()

def count(self, keys=None):

    where = ""

    if keys is not None:

        keys_sql = ",".join(
            f"'{k}'"
            for k in keys
        )

        where = f"""
        WHERE key IN ({keys_sql})
        """

    q = f"""
    SELECT COUNT(*)
    FROM data
    {where}
    """

    return self._execute(q).fetchone()[0]

# ==========================================================
# Query
# ==========================================================

def select(
    self,
    columns=None,
    keys=None,
    where=None,
    order_by=None,
    limit=None
):

    cols = "*"

    if columns is not None:
        cols = ", ".join(columns)

    clauses = []

    if keys is not None:

        keys_sql = ",".join(
            f"'{k}'"
            for k in keys
        )

        clauses.append(
            f"key IN ({keys_sql})"
        )

    if where:

        clauses.append(
            f"({where})"
        )

    where_sql = ""

    if clauses:

        where_sql = (
            "WHERE "
            + " AND ".join(clauses)
        )

    order_sql = ""

    if order_by:

        order_sql = (
            f"ORDER BY {order_by}"
        )

    limit_sql = ""

    if limit is not None:

        limit_sql = (
            f"LIMIT {limit}"
        )

    q = f"""
    SELECT {cols}
    FROM data
    {where_sql}
    {order_sql}
    {limit_sql}
    """

    return self._execute(q).df()

def head(self, key=None, n=5):

    if key is None:

        return self.select(
            limit=n
        )

    return self.select(
        keys=[key],
        limit=n
    )

def describe(
    self,
    columns=None,
    keys=None
):

    df = self.select(
        columns=columns,
        keys=keys
    )

    return df.describe(include="all")

def sql(self, sql):

    return self._execute(sql).df()