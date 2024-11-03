import asyncio
import os
from twikit import Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TweetRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    keyword: str
    count: int = 10

async def twitter_login():
    client = Client('ja')
    try:
        await client.login(
            auth_info_1='manokrod@addrin.uk',
            auth_info_2='@nagi_tips',
            password='!naginagi?'
        )
        print("ログインに成功しました。")
        return client
    except Exception as e:
        print(f"認証エラー: {str(e)}")
        raise HTTPException(status_code=401, detail="Twitter認証に失敗しました")

@app.post("/tweet")
async def create_tweet(request: TweetRequest):
    client = await twitter_login()
    try:
        await client.create_tweet(text=request.text)
        return {"status": "success", "message": "ツイートを投稿しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ツイート投稿に失敗: {str(e)}")
    finally:
        await client.logout()

@app.post("/search")
async def search_tweets(request: SearchRequest):
    client = await twitter_login()
    try:
        tweets = await client.search_tweet(request.keyword, 'Top', count=request.count)
        results = []
        for tweet in tweets:
            results.append({
                "id": tweet.id,
                "user": tweet.user.screen_name,
                "text": tweet.text
            })
        return {"status": "success", "tweets": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ツイート検索に失敗: {str(e)}")
    finally:
        await client.logout()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)