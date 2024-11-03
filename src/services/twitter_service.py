from twikit import Client
from fastapi import HTTPException

class TwitterService:
    def __init__(self):
        self.client = Client('ja')

    async def login(self):
        try:
            await self.client.login(
                auth_info_1='manokrod@addrin.uk',
                auth_info_2='@nagi_tips',
                password='!naginagi?'
            )
            print("ログインに成功しました。")
            return self.client
        except Exception as e:
            print(f"認証エラー: {str(e)}")
            raise HTTPException(status_code=401, detail="Twitter認証に失敗しました") 