import psycopg2
from .config import load_config
from domain.models.ncmipi import NcmIpi

class IpiOperations:
    def __init__(self):
        pass

    def insert_ipi(self, ipi_list: NcmIpi) -> int:
        try:
            sql = self.__mount_sql(ipi_list)
            config = load_config()
            print(f"Inserting {len(ipi_list)} rows in IPI table...")
            with  psycopg2.connect(**config) as conn:
                with  conn.cursor() as cur:
                    cur.execute(sql)             
                    conn.commit()
            print(f"{len(ipi_list)} rows inserted in IPI table!")
            return 0
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error inserting {len(ipi_list)} rows in IPI table: {error}")
            return 1
    
    def __mount_sql(self, ipi_list: NcmIpi) -> str:
        sql = "INSERT INTO public.ipi(ncm, aliquota) values "
        for ipi in ipi_list:
            sql += f"('{ipi.ncm}', {ipi.aliquota}),"
        sql = sql.rstrip(",") + ";"
        return sql