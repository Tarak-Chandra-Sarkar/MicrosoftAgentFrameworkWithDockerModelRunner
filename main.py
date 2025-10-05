import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from logger_config import get_logger

# Load environment variables from .env file
load_dotenv()

# ==============================
# CONFIGURATION
# ==============================
DMR_BASE_URL = os.getenv("DMR_BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")
INSTRUCTIONS = os.getenv("AGENT_INSTRUCTIONS", "You are a helpful assistant.")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "3"))

logger = get_logger("JokeAgent")

# ==============================
# MAIN LOGIC
# ==============================
async def create_openai_client() -> AsyncOpenAI:
    """Initialize a local AsyncOpenAI client with retry and logging."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client = AsyncOpenAI(api_key="dummy_key", base_url=DMR_BASE_URL)
            logger.info("✅ Connected to Docker Model Runner")
            return client
        except Exception as e:
            logger.warning(f"Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY} seconds...")
                await asyncio.sleep(RETRY_DELAY)
            else:
                logger.error("❌ Failed to connect to DMR after several attempts.")
                raise

async def main():
    logger.info("🚀 Starting Local AI Agent Example")
    logger.debug(f"Model: {MODEL_ID} | DMR URL: {DMR_BASE_URL}")

    local_client = await create_openai_client()
    chat_client = OpenAIChatClient(async_client=local_client, model_id=MODEL_ID)

    async with ChatAgent(chat_client=chat_client, instructions=INSTRUCTIONS) as agent:
        logger.info("✅ Agent initialized successfully")

        # ---- Non-streaming Example ----
        try:
            logger.info("🗣️ Non-Streaming Invocation")
            result = await agent.run("Tell me a joke about a pirate.")
            print("\n--- Non-Streaming Result ---")
            print(result.text)
        except Exception as e:
            logger.exception(f"Error during non-streaming run: {e}")

        # ---- Streaming Example ----
        try:
            logger.info("💬 Streaming Invocation")
            print("\n--- Streaming Result ---")
            async for update in agent.run_stream("Tell me a joke about a pirate."):
                if update.text:
                    print(update.text, end="", flush=True)
            print("\n")
        except Exception as e:
            logger.exception(f"Error during streaming run: {e}")

# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    print("This script requires Docker Desktop and Docker Model Runner to be configured.")
    print("Run these commands first:")
    print("1. docker desktop enable model-runner --tcp 12434")
    print("2. docker model pull ai/smollm2:latest")
    print("-" * 50)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user. Exiting gracefully.")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        logger.info("📝 Logs saved to %s/%s", os.getenv("LOG_DIR"), os.getenv("LOG_FILE"))
