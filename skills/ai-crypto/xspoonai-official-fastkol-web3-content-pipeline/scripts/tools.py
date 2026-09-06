import os
import asyncio
import json
from typing import Dict, Any, List
import httpx
from spoon_ai_stub import MCPTool
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class RealPolymarketTool(MCPTool):
    def __init__(self):
        super().__init__("polymarket", "Fetch Trending Markets from Polymarket", {})
        self.gamma_api_url = "https://gamma-api.polymarket.com/events"

    async def execute(self, limit: int = 5, **kwargs) -> List[Dict[str, Any]]:
        limit = int(os.getenv("POLYMARKET_EVENTS_LIMIT", limit))
        
        print(f"[RealPolymarket] Fetching top {limit} trending events from Gamma API...")
        
        params = {
            "limit": limit,
            "active": "true",
            "closed": "false",
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.gamma_api_url, params=params)
                resp.raise_for_status()
                data = resp.json()
                
                markets = []
                for item in data:
                    markets.append({
                        "id": str(item.get("id")),
                        "title": item.get("title"),
                        "volume": item.get("volume", 0), 
                        "category": item.get('category'),
                        "slug": item.get("slug")
                    })
                markets.sort(key=lambda x: float(x.get("volume") or 0), reverse=True)
                
                print(f"[RealPolymarket] Successfully fetched and sorted {len(markets)} markets.")
                return markets[:limit]

        except Exception as e:
            print(f"[RealPolymarket] Error fetching data: {e}")
            raise e

class RealYouTubeTool(MCPTool):
    def __init__(self):
        super().__init__("youtube_uploader", "Upload Video to YouTube", {})
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS", "client_secrets.json")
        self.TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "token.json")
        self.api_service_name = "youtube"
        self.api_version = "v3"

    def _get_authenticated_service(self):
        creds = None
        
        if os.path.exists(self.TOKEN_FILE):
             try:
                creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
             except Exception as e:
                print(f"[RealYouTube] Invalid token file: {e}")

        if not creds or not creds.valid:
             client_id = os.getenv("YOUTUBE_CLIENT_ID")
             client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
             refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
             
             if client_id and client_secret and refresh_token:
                 print("[RealYouTube] Using Environment Credentials...")
                 from google.oauth2.credentials import Credentials
                 creds = Credentials(
                     None, 
                     refresh_token=refresh_token,
                     token_uri="https://oauth2.googleapis.com/token",
                     client_id=client_id,
                     client_secret=client_secret,
                     scopes=self.SCOPES
                 )

                 try:
                     creds.refresh(Request())
                     with open(self.TOKEN_FILE, 'w') as token:
                        token.write(creds.to_json())
                 except Exception as e:
                     print(f"[RealYouTube] Failed to refresh env credentials: {e}")
                     creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("[RealYouTube] Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.CLIENT_SECRETS_FILE):
                    raise FileNotFoundError(f"Missing {self.CLIENT_SECRETS_FILE} and Environment Vars. Cannot authenticate.")
                
                print("[RealYouTube] No valid token found. Initiating OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        return build(self.api_service_name, self.api_version, credentials=creds)

    async def execute(self, video_path: str, title: str, description: str, **kwargs) -> Dict[str, Any]:
        print(f"[RealYouTube] Preparing to upload video: {video_path}")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        try:
            youtube = await asyncio.to_thread(self._get_authenticated_service)
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': ['FastKOL', 'SpoonOS', 'Crypto', 'AI'],
                    'categoryId': '28' 
                },
                'status': {
                    'privacyStatus': 'private', 
                    'selfDeclaredMadeForKids': False,
                }
            }

            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

            print("[RealYouTube] Uploading...")
            
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            response = await asyncio.to_thread(request.execute)

            print(f"[RealYouTube] Upload Complete! Video ID: {response.get('id')}")
            return {
                "status": "success",
                "video_id": response.get('id'),
                "url": f"https://www.youtube.com/watch?v={response.get('id')}",
                "channel_id": response.get("snippet", {}).get("channelId")
            }

        except Exception as e:
            print(f"[RealYouTube] Upload Failed: {e}")
            raise e


class ToolsFactory:
    @staticmethod
    def get_polymarket_tool() -> MCPTool:
        return RealPolymarketTool()

    @staticmethod
    def get_youtube_tool() -> MCPTool:
        return RealYouTubeTool()
