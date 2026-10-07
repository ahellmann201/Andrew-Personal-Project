from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    """Common configuration for everything parsed from the wilds.mhdb.io API."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        frozen=True,
    )