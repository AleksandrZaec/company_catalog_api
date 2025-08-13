from fastapi import FastAPI
from src.api import organization
from src.config.logger import setup_logging, logger
import time

app = FastAPI(title="Catalog")

setup_logging()


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Started {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logger.info(f"Completed {request.method} {request.url} with status {response.status_code} in {duration:.2f}ms")
    return response


app.include_router(organization.router, prefix="/organizations", tags=["Organizations"])

