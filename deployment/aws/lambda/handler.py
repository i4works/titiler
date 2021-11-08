"""AWS Lambda handler."""

import logging

from mangum import Mangum
import base64
from fastapi import Query

from titiler.application.main import app
from titiler.core.factory import TilerFactory 

def DatasetPathParams(
    url: str = Query(..., description="Dataset URL"),
    base64_encoded: bool = Query(None)
) -> str:
    """Create dataset path from args"""
    if base64_encoded:
        url = base64.b64decode(url).decode()
    return url


cog = TilerFactory(path_dependency=DatasetPathParams)

app.include_router(cog.router, prefix="/cog-b64", tags=["Cloud Optimized GeoTIFF"])

logging.getLogger("mangum.lifespan").setLevel(logging.ERROR)
logging.getLogger("mangum.http").setLevel(logging.ERROR)

handler = Mangum(app, lifespan="auto", log_level="error")
