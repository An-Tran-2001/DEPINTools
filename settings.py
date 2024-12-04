"""
Copyright © 2024 [tranandeveloper@gmail.com]
All Rights Reserved.

Licensed under the MIT License. You may obtain a copy of the License at:
    https://opensource.org/licenses/MIT

Author: TranAn
"""

import os
import sys
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
sys.path.append(os.path.dirname(__file__))


# PgAdmin
POSTGRESQL_HOST: str = os.environ.get("POSTGRESQL_HOST")
POSTGRESQL_PORT: int = int(os.environ.get("POSTGRESQL_PORT"))
POSTGRESQL_USER: str = os.environ.get("POSTGRESQL_USER")
POSTGRESQL_PASSWORD: str = os.environ.get("POSTGRESQL_PASSWORD")
POSTGRESQL_DATABASE: str = os.environ.get("POSTGRESQL_DATABASE")
