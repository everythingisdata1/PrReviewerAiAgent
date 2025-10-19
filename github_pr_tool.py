from typing import Dict, List, Optional

import requests
from loguru import logger


# =====================================================
# GitHub PR Review Processor
# =====================================================

class GitHubPrReviewProcessor:
    def __init__(self,
                 base_url: str = "https://api.github.com",
                 owner: str = "",
                 repo: str = "",
                 auth_token: Optional[str] = None):
        """
        Initialize GitHub PR Review Processor.
        """
        self._base_url = base_url.rstrip("/")
        self._owner = owner
        self._repo = repo
        self._token = auth_token
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/vnd.github+json"
        })
        if self._token:
            self._session.headers.update({
                "Authorization": f"Bearer {self._token}"
            })

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        try:
            resp = self._session.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
            logger.error(f"Request failed [{resp.status_code}]: {resp.text}")
            return None
        except requests.RequestException as ex:
            logger.exception(f"Request error for {url}: {ex}")

    def pull_all_prs(self, state: str = "open") -> List[Dict]:
        endpoint = f"/repos/{self._owner}/{self._repo}/pulls"
        params = {"state": state, "per_page": 100}
        data = self._get(endpoint, params=params)
        return data if data else []

    def get_pull_request_details(self, pr_number: int) -> Dict:
        endpoint = f"/repos/{self._owner}/{self._repo}/pulls/{pr_number}"
        data = self._get(endpoint)
        return data or {}

    def fetch_pull_changes(self, pr_number: int) -> List[Dict]:
        endpoint = f"/repos/{self._owner}/{self._repo}/pulls/{pr_number}/files"
        data = self._get(endpoint)
        return data if data else []

    def pull_pr_diff(self, pr_number: int) -> str:
        url = f"{self._base_url}/repos/{self._owner}/{self._repo}/pulls/{pr_number}"
        headers = {"Accept": "application/vnd.github.v3.diff"}
        try:
            resp = self._session.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.text
            logger.error(f"Diff request failed [{resp.status_code}]: {resp.text}")
            return ""
        except requests.RequestException as ex:
            logger.exception(f"Error fetching diff for PR #{pr_number}: {ex}")
            return ""
