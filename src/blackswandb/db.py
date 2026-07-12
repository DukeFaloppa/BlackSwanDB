from pathlib import Path
import duckdb
import pandas as pd

from . import utils as bs_utils
from . import sql as bs_sql
from . import io as bs_io
from . import update as bs_update

class BlackSwanDB:

    def __init__(self, root="./blackswan"):

        self.root = Path(root)
        self.parquet_dir = self.root / "parquet"
        self.db_path = self.root / "database.duckdb"

        self.parquet_dir.mkdir(parents=True, exist_ok=True)

        self.con = duckdb.connect(str(self.db_path))

        # cache
        self._keys = None
        self._columns = None

    ########### update

    def update(self,update_dir, keep="last"):
        return bs_update.update(self, update_dir, keep)
    
    def update_from_list(self,file_list,keep="last"):
        return bs_update.update_from_list(self,file_list,keep)


    ########### utils
    
    def refresh(self):
        return bs_utils.refresh(self)
    
    def __enter__(self):
        return bs_utils.__enter__(self)
    
    def __exit__(self):
        return bs_utils.__exit__(self)
    
    def __len__(self):
        return bs_utils.__len__(self)
    
    def __repr__(self):
        return bs_utils.__repr__(self)
    
    def vacuum(self):
        return bs_utils.vacuum(self)
    
    def close(self):
        return bs_utils.close(self)
    
    def _dataset_sql(self):
        return bs_sql._dataset_sql(self)

    def _execute(self,sql):
        return bs_sql._execute(self,sql)

    def _invalidate_cache(self):
        return bs_utils._invalidate_cache(self)

    ########### io

    def _read_file(self,file):
        return bs_io.read_file(self,file)
    
    def _drop_duplicates(self,df,keep="last"):
        return bs_io.drop_duplicates(self,df,keep)
    
    def _save_parquet(self,df,filename):
        return bs_io.save_parquet(self,df,filename)
    
    ########### sql

    def keys(self):
        return bs_sql.keys(self)

    def schema(self):
        return bs_sql.schema(self)

    def columns(self):
        return bs_sql.columns(self)
    
    def count(self, keys=None):
        return bs_sql.count(self,keys)

    def head(self, key=None,n=10):
        return bs_sql.head(self,key,n)

    def describe(self,columns=None,keys=None):
        return bs_sql.describe(self,columns,keys)

    def sql(self,sql):
        return bs_sql.sql(self,sql)

    def select(self,columns=None,keys=None,
               where=None,order_by=None,limit=None):
        return bs_sql.select(self,columns,keys,where,order_by,limit)