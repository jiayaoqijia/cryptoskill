import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # Load .env file
from agent import FastKOLAgent

async def main():
    print("--- Starting FastKOL Skill Integration Test ---")
    if not os.path.exists("client_secrets.json") and not os.path.exists("token.json"):
        print("WARNING: YouTube 'client_secrets.json' not found. YouTube upload may fail or trigger interactive login.")
    if not os.path.exists("test_video.mp4"):
        print("Creating dummy test_video.mp4...")
        with open("test_video.mp4", "wb") as f:
            f.write(b"0" * 1024 * 1024)
    agent = FastKOLAgent()
    config = {
        "video_path": "test_video.mp4"
    }    
    try:
        result = await agent.run_workflow(config)
        print("\n--- Workflow Result ---")
        print(result)
        
        if result["status"] == "completed":
            print("\nSUCCESS: Workflow completed successfully.")
        else:
            print("\nFAILURE: Workflow failed.")
            
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
