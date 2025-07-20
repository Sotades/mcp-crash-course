import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4", temperature=0)

# Use pathlib for cross-platform path handling
server_path = Path("servers/math_server.py").absolute()
stdio_server_params = StdioServerParameters(
    command="python",
    args=[str(server_path)],
)

print(os.getenv("OPENAI_API_KEY"))

async def main():
    print("Hello from mcp-crash-course!")
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Session initialized")
            tools = await load_mcp_tools(session)

            agent = create_react_agent(llm, tools)

            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3?")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
