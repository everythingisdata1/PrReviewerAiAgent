import os
from typing import Optional, List, Dict

from fastmcp import FastMCP
from loguru import logger

from mcp_tools import GitHubPrReviewProcessor


mcp = FastMCP(
    name="github_pr_review_tool",
    version="v1.0.0"
)

# =====================================================
# =========== GitHub PR Review Server =================
# =====================================================

_processor: Optional[GitHubPrReviewProcessor] = None


def init_github_repo(base_url, owner: str, repo: str, auth: str = None) -> str:
    """
    Initialize GitHub repository context for PRs
    :param owner:
    :param repo:
    :param auth:
    :return:
    """
    global _processor
    _processor = GitHubPrReviewProcessor(base_url=base_url, owner=owner, repo=repo, auth_token=auth)

    return f"Initialized Github repo {owner}/{repo}."


@mcp.tool("list_pull_request")
async def list_pull_request(state: str = "open") -> List[Dict]:
    """
    List all the pull request for the configured respsitory
    :param state:
    :return:
    """
    if not _processor:
        raise RuntimeError("Repository not initialized. Call init_github_repo first.")
    return _processor.pull_all_prs(state=state)


@mcp.tool(name="get_pull_request_details")
async def get_pull_request_details(pr_number: int) -> Dict:
    """
    Get details of a specific pull request by number.
    """
    if not _processor:
        raise RuntimeError("Repository not initialized.")
    return _processor.get_pull_request_details(pr_number)


@mcp.tool("get_pull_request_files_changed")
async def get_pull_request_files_changed(pr_number: int) -> List[Dict]:
    """
    List files changed in a pull request.
    """
    if not _processor:
        raise RuntimeError("Repository not initialized.")
    return _processor.fetch_pull_changes(pr_number)


@mcp.tool(name="get_pull_request_changed_diff",
          description="Please help in pr for the given pr number")
async def get_pull_request_changed_diff(pr_number: int) -> str:
    """
    Get the raw diff of a pull request.
    """
    if not _processor:
        raise RuntimeError("Repository not initialized.")
    return _processor.pull_pr_diff(pr_number)


if __name__ == "__main__":
    logger.info("Starting FastMCP GitHub PR Review Tool...")
    init_github_repo(
        base_url=os.getenv("BASE_URL_REPOS_1"),
        repo="ai_agent_github_pr_review",
        owner="everythingisdata1"
    )
    mcp.run(transport="sse")
