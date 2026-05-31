from ..models.enums import Crop


class R2Client:
    """Cloudflare R2 object storage wrapper. boto3/httpx implementation goes here."""

    async def upload_photo(self, image_bytes: bytes, farmer_id: str | None, crop: Crop) -> str:
        raise NotImplementedError

    async def delete_photo(self, key: str) -> None:
        raise NotImplementedError

    async def schedule_deletion(self, key: str, days: int = 90) -> None:
        raise NotImplementedError
