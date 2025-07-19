# math_server.py
from mcp.server.fastmcp import FastMCP
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

try:
    mcp = FastMCP("Math")
    logger.info("Created FastMCP instance")

    @mcp.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        logger.info(f"Adding {a} and {b}")
        return a + b

    @mcp.tool()
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        logger.info(f"Multiplying {a} and {b}")
        return a * b

    if __name__ == "__main__":
        logger.info("Starting Math server...")
        try:
            # Try stdio transport first
            logger.info("Attempting to start with stdio transport...")
            mcp.run(transport="stdio")
        except Exception as e:
            logger.error(f"Error with stdio transport: {e}")
            # Fall back to websocket if stdio fails
            logger.info("Falling back to websocket transport...")
            mcp.run(transport="websocket", host="localhost", port=8000)
except Exception as e:
    logger.error(f"Fatal error: {e}")
    raise