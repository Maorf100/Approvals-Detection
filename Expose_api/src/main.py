from fastapi import FastAPI
from approvals.router import router
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import uvicorn

app = FastAPI()

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)