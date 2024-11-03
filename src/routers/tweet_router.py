from fastapi import APIRouter, HTTPException
from services.twitter_service import TwitterService
from schemas.tweet_schema import TweetRequest

router = APIRouter()

@router.post("/tweet")
async def create_tweet(request: TweetRequest):
    twitter_service = TwitterService()
    try:
        client = await twitter_service.login()
        await client.create_tweet(text=request.text)
        return {"status": "success", "message": "ツイートを投稿しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ツイート投稿に失敗: {str(e)}")
    finally:
        if client:
            await client.logout() 