from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class BaseValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)



