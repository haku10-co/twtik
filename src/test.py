import os
from twikit import Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 環境変数から認証情報を取得
TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

class TweetRequest(BaseModel):
    text: str
    media_paths: list[str] = []  # オプショナルな画像パスのリスト

class SearchRequest(BaseModel):
    keyword: str
    count: int = 10

@app.post("/tweet")
async def create_tweet(request: TweetRequest):
    client = await twitter_login()
    try:
        # 画像がある場合はアップロード
        media_ids = []
        if request.media_paths:
            for media_path in request.media_paths:
                if not os.path.exists(media_path):
                    raise HTTPException(status_code=400, detail=f"画像が見つかりません: {media_path}")
                media_id = await client.upload_media(media_path)
                media_ids.append(media_id)
        
        # ツイートを投稿
        tweet = await client.create_tweet(
            text=request.text,
            media_ids=media_ids if media_ids else None
        )
        
        return {
            "status": "success",
            "tweet": {
                "id": tweet.id,
                "text": tweet.text,
                "user": tweet.user.screen_name
            }
        }
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

async def twitter_login():
    try:
        client = Client('ja')
        logger.info("クライアント作成完了")
        
        await client.login(
            auth_info_1=TWITTER_EMAIL,
            auth_info_2=TWITTER_USERNAME,
            password=TWITTER_PASSWORD
        )
        logger.info("ログイン処理完了")
        return client
    except Exception as e:
        logger.error(f"認証エラー: {str(e)}", exc_info=True)
        raise HTTPException(status_code=401, detail=f"Twitter認証に失敗しました: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)