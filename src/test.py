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
    try:
        client = Client('ja')
        print("クライアント作成完了")  # デバッグログ追加
        
        await client.login(
            auth_info_1='manokrod@addrin.uk',
            auth_info_2='@nagi_tips',
            password='!naginagi?'
        )
        print("ログイン処理完了")  # デバッグログ追加
        return client
    except Exception as e:
        print(f"認証エラーの詳細: {str(e)}")  # より詳細なエラー情報
        print(f"エラーの種類: {type(e)}")     # エラーの型を表示
        raise HTTPException(status_code=401, detail=f"Twitter認証に失敗しました: {str(e)}")

@app.post("/tweet")
async def create_tweet(request: TweetRequest):
    client = await twitter_login()
    try:
        print(f"ツイート投稿開始: {request.text}")  # デバッグログ追加
        tweet = await client.create_tweet(text=request.text)
        print("ツイート投稿完了")  # デバッグログ追加
        return {
            "status": "success",
            "tweet_id": tweet.id,
            "text": request.text
        }
    except Exception as e:
        print(f"ツイート投稿エラーの詳細: {str(e)}")  # より詳細なエラー情報
        print(f"エラーの種類: {type(e)}")            # エラーの型を表示
        raise HTTPException(status_code=500, detail=f"ツイート投稿に失敗: {str(e)}")
    finally:
        try:
            await client.logout()
            print("ログアウト完了")  # デバッグログ追加
        except Exception as e:
            print(f"ログアウトエラー: {str(e)}")

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
    uvicorn.run(app, host="0.0.0.0", port=8000)