GitHub PR Review FastMCP Tool

A FastMCP-based AI tool that allows LLM agents or developers to interact with GitHub Pull Requests in real time.
It enables agents to list PRs, fetch details, inspect changed files, and view diffs — all through the Model Context Protocol (MCP) interface.

🚀 Features

🔐 Authenticate with a GitHub Personal Access Token (PAT)

📋 List all open/closed pull requests for a repository

🔍 Get detailed PR information (title, author, branches, etc.)

🧾 Fetch file changes and PR diffs

🧠 Integrate with GitHub Copilot Agents or OpenAI Agents via MCP

🧩 Architecture Overview
┌────────────────────┐
│  FastMCP Server    │  ←– your code
├────────────────────┤
│ Tools:             │
│  • init_github_repo│
│  • list_pull_request│
│  • get_pull_request_details│
│  • get_pull_request_files_changed│
│  • get_pull_request_changed_diff│
└────────┬───────────┘
         │
         ▼
   GitHub REST API


📦 Installation

Clone the repository and install dependencies:

git clone https://github.com/<your-username>/github-pr-review-fastmcp.git
cd github-pr-review-fastmcp
pip install -r requirements.txt


Or install directly using Poetry:

poetry install

⚙️ Configuration

Set up your environment variables or pass them through FastMCP initialization:

export GITHUB_PAT="your_github_personal_access_token"

🧰 Available Tools
Tool Name	Description	Example
init_github_repo	Initialize a GitHub repository context	init_github_repo(base_url, owner, repo, auth)
list_pull_request	List pull requests for a repo	list_pull_request(state="open")
get_pull_request_details	Get detailed info for a PR	get_pull_request_details(pr_number=42)
get_pull_request_files_changed	List files changed in a PR	get_pull_request_files_changed(pr_number=42)
get_pull_request_changed_diff	Get raw PR diff	get_pull_request_changed_diff(pr_number=42)
🧪 Example Run
python main.py


Expected log output:

🚀 Starting FastMCP GitHub PR Review Tool...
INFO | Initialized GitHub repo openai/gpt-repo
INFO | Fetched 5 open PRs.
INFO | PR #42: Improve diff viewer API
INFO | Files changed: 3

🧠 Integration with OpenAI Agent / Copilot MCP

Once running, you can register this FastMCP server in your Agent configuration (SSE or stdio transport):

{
  "id": "github_pr_review_tool",
  "name": "GitHub PR Review Tool",
  "version": "1.0.0",
  "transport": {
    "type": "sse",
    "url": "http://localhost:8000/sse"
  }
}


Then your agent can directly call:

list_pull_request or get_pull_request_details
through the MCP runtime.

🧩 Project Structure
github-pr-review-fastmcp/
│
├── src/
│   └── pr_processor/
│       └── github_pr_tool.py      # GitHub API processor
│
├── main.py                        # FastMCP entry point
├── requirements.txt
└── README.md

🛠 Requirements

Python 3.9+

FastMCP (pip install fastmcp)

Requests

Loguru

📄 License

MIT License © 2025 Bharat Singh

✨ Author

Bharat Singh
🏗️ 13+ years in Java & Cloud Engineering
☁️ AWS | Python | Java | MCP | AI Agents
📧 bharatmca2010@gmail.com

📍 India

💡 Future Enhancements

✅ Add caching for repeated PR fetches

🕒 Enable real-time webhook integration (GitHub Events → MCP)

🧩 Add support for PR reviews and comments

🤖 Integrate into Copilot MCP-based AI workflows