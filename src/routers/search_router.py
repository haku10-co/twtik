from fastapi import APIRouter, HTTPException
from services.twitter_service import TwitterService
from schemas.search_schema import SearchRequest

router = APIRouter()

@router.post("/search")
async def search_tweets(request: SearchRequest):
    twitter_service = TwitterService()
    try:
        client = await twitter_service.login()
        tweets = await client.search_tweet(request.keyword, 'Top', count=request.count)
        results = [
            {
                "id": tweet.id,
                "user": tweet.user.screen_name,
                "text": tweet.text
            }
            for tweet in tweets
        ]
        return {"status": "success", "tweets": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ツイート検索に失敗: {str(e)}")
    finally:
        if client:
            await client.logout() 