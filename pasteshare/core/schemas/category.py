from pasteshare.core.schemas import ORMSchema, Schema


class CategorySchemaCreate(Schema):
    name: str
    description: str


class CategorySchemaUpdate(Schema):
    name: str | None = None
    description: str | None = None


class CategorySchemaOut(ORMSchema):
    id: int
    name: str
    description: str


class CategorySchemaDB(Schema):
    name: str
    description: str
