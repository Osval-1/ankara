import asyncio
import logging
from typing import Any

import structlog
import uvloop
from arq.worker import Worker

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


# -------- background tasks --------
# Crop Doctor tasks registered here as they are built:
# async def process_diagnosis_image(ctx: Worker, image_ref: str, crop: str) -> dict: ...
# async def delete_expired_photos(ctx: Worker) -> int: ...

# -------- base functions --------
async def startup(ctx: Worker) -> None:
    logging.info("Worker Started")


async def shutdown(ctx: Worker) -> None:
    logging.info("Worker end")


async def on_job_start(ctx: dict[str, Any]) -> None:
    structlog.contextvars.bind_contextvars(job_id=ctx["job_id"])
    logging.info("Job Started")


async def on_job_end(ctx: dict[str, Any]) -> None:
    logging.info("Job Competed")
    structlog.contextvars.clear_contextvars()
