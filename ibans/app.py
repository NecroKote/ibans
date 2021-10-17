import logging

from fastapi import FastAPI

from .api.v1.router import router as v1_api_router


app = FastAPI(title="iBAN validator", version="1.0.0")
app.include_router(v1_api_router, prefix="/v1")


@app.on_event("startup")
def configure_logging():
    logging.basicConfig(level=logging.INFO)
