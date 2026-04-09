"""Entry point for Astra bot."""
import asyncio
import logging
import os

from dotenv import load_dotenv

from .bot import AstraBot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Run the Astra bot."""
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        return

    bot = AstraBot()
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("Shutting down Astra...")
        await bot.close()
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
