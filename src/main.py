from fastapi import FastAPI
from routers import tweet_router, search_router

app = FastAPI()

# ルーターを追加
app.include_router(tweet_router.router, prefix="/api/v1")
app.include_router(search_router.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 