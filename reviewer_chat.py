import asyncio
import sys

import gradio as gr
from agents import Agent, Runner
from agents.mcp import MCPServerSseParams, MCPServerSse
from dotenv import load_dotenv
from loguru import logger

from src.instructions.instruction import instructions

load_dotenv(override=True)
llm = "gpt-4o-mini"
sse_params = MCPServerSseParams(url="http://127.0.0.1:8000/sse")

# Initialize MCP Server Connection globally So it can persist across the requests
github_mcp_server = MCPServerSse(params=sse_params, client_session_timeout_seconds=40)
pr_review_agent: Agent = None
tools_list = []

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


async def init_agent():
    logger.info("Start PR Reviewer AI Agent....")
    global github_mcp_server, pr_review_agent, tools_list
    await github_mcp_server.connect()

    # list of tool available for debugging
    tools_list = await  github_mcp_server.list_tools()
    for tool in tools_list:
        logger.info(f"Tool :: {tool.name}  :: {tool.description}")

    logger.info("Connected to GitHub PR Review FastMCP server via SSE.")

    logger.info("Define the PR review Agent....")
    pr_review_agent = Agent(
        name="GitHubPrReviewAiAgent",
        instructions=instructions,
        mcp_servers=[github_mcp_server],
        model=llm
    )

    logger.info("Agent initialized and ready to use.")


# Gradio App

async def run_query(messages, history):
    """ Gradio will cal this function in synchronization  """
    logger.info(f"User Message :: {messages}")
    await  init_agent()
    resp = await  Runner.run(pr_review_agent, messages)
    return resp.final_output


if __name__ == '__main__':
    logger.info("Initialize Agent")
    # gr.ChatInterface(run_query, type="messages").launch()
    with gr.Blocks(fill_height=True, css="footer {visibility: hidden}") as demo:
        gr.HTML("<h1>GitHub PRs Reviewer AI Assistant</h1>")
        zc_chatbot = gr.ChatInterface(run_query, type="messages",  fill_height=True )

    if __name__ == "__main__":
        demo.launch()
