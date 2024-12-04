"""
Copyright © 2024 [tranandeveloper@gmail.com]
All Rights Reserved.

Licensed under the MIT License. You may obtain a copy of the License at:
    https://opensource.org/licenses/MIT

Author: TranAn
"""

from providers.postgresql.orm_client import SqlalChemyClient
from settings import (POSTGRESQL_DATABASE, POSTGRESQL_HOST,
                      POSTGRESQL_PASSWORD, POSTGRESQL_PORT, POSTGRESQL_USER)

database_uri = SqlalChemyClient.create_url(
    user=POSTGRESQL_USER,
    password=POSTGRESQL_PASSWORD,
    host=POSTGRESQL_HOST,
    port=POSTGRESQL_PORT,
    database=POSTGRESQL_DATABASE,
)

pgadmin_orm = SqlalChemyClient.get_instance(database_uri=database_uri)
BaseModel = pgadmin_orm.get_base()
