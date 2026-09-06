import asyncio
import os
from spoon_ai_stub import SpoonReactMCP, ChatBot
from tools import ToolsFactory


class FastKOLAgent(SpoonReactMCP):
    """
    FastKOL Agent that manages the content generation workflow.
    Workflow: Data (Polymarket) -> Script (LLM) -> Video (Placeholder) -> Distribution (YouTube)
    """
    def __init__(self, **kwargs):
        self.polymarket = ToolsFactory.get_polymarket_tool()
        self.youtube_tool = ToolsFactory.get_youtube_tool()
        super().__init__(tools=[self.polymarket, self.youtube_tool])
        self.llm = ChatBot("gpt-4")


    async def run_workflow(self, config: dict, status_callback=None) -> dict:
        """
        Executes the modified workflow: Market Data -> Content -> YouTube
        """
        result = {"status": "started", "stages": {}}
        
        async def update_status(stage, status, data=None, error=None):
            print(f"[{stage}] {status}")
            if status_callback:
                await status_callback({
                    "stage": stage,
                    "status": status,
                    "data": data,
                    "error": error
                })

        try:
            await update_status("Market Snapshot", "running")
            markets = await self.polymarket.execute(limit=3)
            result["stages"]["market_data"] = markets
            await update_status("Market Snapshot", "completed", data=markets)
            await update_status("Key Insights", "running")
            if markets and len(markets) > 0:
                top_market = markets[0]
                script = await self._generate_script(top_market)
                result["stages"]["script"] = script
                await update_status("Key Insights", "completed", data=script)
            else:
                 raise Exception("No markets found from Polymarket API")
            video_path = config.get("video_path", "test_video.mp4")
            if not os.path.exists(video_path):
                 print(f"Video {video_path} not found. Creating dummy for demo/test.")
                 with open(video_path, "wb") as f:
                     f.write(b"0" * 1024)

            await update_status("Narration Script", "running")
            youtube_res = await self.youtube_tool.execute(
                video_path=video_path,
                title=script["title"],
                description=script["body"]
            )
            
            result["stages"]["publish"] = youtube_res
            await update_status("Narration Script", "completed", data=youtube_res)

            result["status"] = "completed"

        except Exception as e:
            print(f"Workflow Failed: {e}")
            result["status"] = "failed"
            result["error"] = str(e)
            await update_status("Workflow", "failed", error=str(e))
        
        return result

    async def _generate_script(self, market_data):
        """LLM script generation based on real market data. In production, connect to OpenAI."""
        await asyncio.sleep(1)
        title = market_data['title']
        volume = market_data.get('volume', 'N/A')
        return {
            "title": f"Crypto Alert: {title}",
            "body": f"Big moves in {title}! Volume: {volume}. \n\n#Crypto #SpoonOS",
            "visual_prompt": f"Data viz of {title}"
        }

