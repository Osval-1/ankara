from pydantic import BaseModel


class ExtensionWorkerRead(BaseModel):
    id: int
    name: str
    region: str
    phone: str
    whatsapp_available: bool
    crops: list[str]
    active: bool

    model_config = {"from_attributes": True}
