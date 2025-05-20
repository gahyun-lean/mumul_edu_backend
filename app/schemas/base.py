# schemas/base.py
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes      = True,
        validate_by_name     = True,
        alias_generator      = lambda x: x
    )
