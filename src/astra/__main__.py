"""Entry point for Astra bot."""

import asyncio
import logging
import os
import sys

# Try to load dotenv, but don't fail if not installed
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from .bot import AstraBot

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
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
