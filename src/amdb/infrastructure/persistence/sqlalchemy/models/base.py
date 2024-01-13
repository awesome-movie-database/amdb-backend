from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TIMESTAMP


class Model(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }
