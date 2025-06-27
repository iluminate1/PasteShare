from pydantic import BaseModel, ConfigDict


class Schema(BaseModel): ...


class ORMSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
