from pasteshare.core.schemas import ORMSchema, Schema


class LanguageSchemaCreate(Schema):
    name: str
    code: str
    file_extension: str


class LanguageSchemaUpdate(Schema):
    name: str | None = None
    code: str | None = None
    file_extension: str | None = None


class LanguageSchemaOut(ORMSchema):
    id: int
    name: str
    code: str
    file_extension: str


class LanguageSchemaDB(Schema):
    name: str
    code: str
    file_extension: str
