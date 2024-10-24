from fastapi import FastAPI
from fastapi import Request
from app.api.review import router as review_router
from app.settings import logger

app = FastAPI(title="CodeReviewAI")

app.include_router(review_router)


@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application is starting up.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application is shutting down.")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(
        f"Completed request: {request.method} {request.url} - Status code: {response.status_code}"
    )
    return response
