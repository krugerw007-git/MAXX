"""
GitHub Automation Client for MAXX Project
Handles PR creation, issue management, release automation, and more.
"""

import os
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path
from loguru import logger

try:
    from github import Github, GithubIntegration
    from github.Repository import Repository
    from github.PullRequest import PullRequest
    from github.Issue import Issue
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    logger.warning("PyGithub not installed - GitHub automation will use CLI fallback")


@dataclass
class GitHubConfig:
    """GitHub configuration."""
    token: str = ""
    owner: str = "krugerw007-git"
    repo: str = "MAXX"
    base_branch: str = "main"
    
    @classmethod
    def from_env(cls) -> "GitHubConfig":
        return cls(
            token=os.getenv("GITHUB_TOKEN", ""),
            owner=os.getenv("GITHUB_OWNER", "krugerw007-git"),
            repo=os.getenv("GITHUB_REPO", "MAXX"),
            base_branch=os.getenv("GITHUB_BASE_BRANCH", "main"),
        )


class GitHubClient:
    """GitHub API client with CLI fallback."""
    
    def __init__(self, config: Optional[GitHubConfig] = None):
        self.config = config or GitHubConfig.from_env()
        self._gh = None
        self._repo = None
        
        if self.config.token and GITHUB_AVAILABLE:
            self._gh = Github(self.config.token)
            self._repo = self._gh.get_repo(f"{self.config.owner}/{self.config.repo}")
    
    @property
    def repo(self) -> Optional[Repository]:
        return self._repo
    
    def _run_gh_cli(self, args: List[str]) -> Dict[str, Any]:
        """Run gh CLI command."""
        import subprocess
        cmd = ["gh"] + args
        env = os.environ.copy()
        if self.config.token:
            env["GH_TOKEN"] = self.config.token
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"gh CLI failed: {result.stderr}")
        
        try:
            return json.loads(result.stdout) if result.stdout.strip() else {}
        except json.JSONDecodeError:
            return {"raw": result.stdout}
    
    # ========================================
    # PR MANAGEMENT
    # ========================================
    
    def create_pr(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: Optional[str] = None,
        draft: bool = False,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a pull request."""
        base = base_branch or self.config.base_branch
        
        if self._repo:
            pr = self._repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base,
                draft=draft,
            )
            if labels:
                pr.add_to_labels(*labels)
            if assignees:
                pr.add_to_assignees(*assignees)
            return {"number": pr.number, "url": pr.html_url, "id": pr.id}
        
        # CLI fallback
        args = [
            "pr", "create",
            "--title", title,
            "--body", body,
            "--head", head_branch,
            "--base", base,
        ]
        if draft:
            args.append("--draft")
        if labels:
            args.extend(["--label", ",".join(labels)])
        if assignees:
            args.extend(["--assignee", ",".join(assignees)])
        
        return self._run_gh_cli(args)
    
    def get_pr(self, pr_number: int) -> Dict[str, Any]:
        """Get PR details."""
        if self._repo:
            pr = self._repo.get_pull(pr_number)
            return {
                "number": pr.number,
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "head": pr.head.ref,
                "base": pr.base.ref,
                "url": pr.html_url,
                "merged": pr.merged,
                "mergeable": pr.mergeable,
                "labels": [l.name for l in pr.labels],
                "assignees": [a.login for a in pr.assignees],
            }
        
        return self._run_gh_cli(["pr", "view", str(pr_number), "--json", "number,title,body,state,headRefName,baseRefName,url,merged,mergeable,labels,assignees"])
    
    def merge_pr(
        self,
        pr_number: int,
        method: str = "squash",
        delete_branch: bool = True,
    ) -> Dict[str, Any]:
        """Merge a pull request."""
        if self._repo:
            pr = self._repo.get_pull(pr_number)
            result = pr.merge(merge_method=method, delete_branch=delete_branch)
            return {"merged": result.merged, "sha": result.sha}
        
        return self._run_gh_cli([
            "pr", "merge", str(pr_number),
            "--merge" if method == "merge" else f"--{method}",
            "--delete-branch" if delete_branch else "--no-delete-branch",
        ])
    
    def list_prs(
        self,
        state: str = "open",
        base: Optional[str] = None,
        head: Optional[str] = None,
        limit: int = 30,
    ) -> List[Dict[str, Any]]:
        """List pull requests."""
        if self._repo:
            prs = self._repo.get_pulls(state=state, base=base, head=head)
            return [
                {"number": p.number, "title": p.title, "state": p.state, "head": p.head.ref, "url": p.html_url}
                for p in list(prs)[:limit]
            ]
        
        args = ["pr", "list", "--state", state, "--limit", str(limit), "--json", "number,title,state,headRefName,url"]
        if base:
            args.extend(["--base", base])
        if head:
            args.extend(["--head", head])
        return self._run_gh_cli(args)
    
    # ========================================
    # ISSUE MANAGEMENT
    # ========================================
    
    def create_issue(
        self,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
        milestone: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an issue."""
        if self._repo:
            issue = self._repo.create_issue(
                title=title,
                body=body,
                labels=labels or [],
                assignees=assignees or [],
            )
            if milestone:
                ms = self._repo.get_milestone_by_title(milestone)
                if ms:
                    issue.edit(milestone=ms)
            return {"number": issue.number, "url": issue.html_url, "id": issue.id}
        
        args = ["issue", "create", "--title", title, "--body", body]
        if labels:
            args.extend(["--label", ",".join(labels)])
        if assignees:
            args.extend(["--assignee", ",".join(assignees)])
        if milestone:
            args.extend(["--milestone", milestone])
        return self._run_gh_cli(args)
    
    def get_issue(self, issue_number: int) -> Dict[str, Any]:
        """Get issue details."""
        if self._repo:
            issue = self._repo.get_issue(issue_number)
            return {
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "labels": [l.name for l in issue.labels],
                "assignees": [a.login for a in issue.assignees],
                "url": issue.html_url,
            }
        
        return self._run_gh_cli(["issue", "view", str(issue_number), "--json", "number,title,body,state,labels,assignees,url"])
    
    def close_issue(self, issue_number: int, comment: str = "") -> Dict[str, Any]:
        """Close an issue."""
        if self._repo:
            issue = self._repo.get_issue(issue_number)
            if comment:
                issue.create_comment(comment)
            issue.edit(state="closed")
            return {"closed": True}
        
        args = ["issue", "close", str(issue_number)]
        if comment:
            args.extend(["--comment", comment])
        return self._run_gh_cli(args)
    
    # ========================================
    # RELEASE AUTOMATION
    # ========================================
    
    def create_release(
        self,
        tag_name: str,
        name: str,
        body: str,
        draft: bool = False,
        prerelease: bool = False,
        target_branch: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a release."""
        if self._repo:
            release = self._repo.create_git_release(
                tag=tag_name,
                name=name,
                message=body,
                draft=draft,
                prerelease=prerelease,
                target_commitish=target_branch,
            )
            return {"id": release.id, "url": release.html_url, "tag": release.tag_name}
        
        args = [
            "release", "create", tag_name,
            "--title", name,
            "--notes", body,
        ]
        if draft:
            args.append("--draft")
        if prerelease:
            args.append("--prerelease")
        if target_branch:
            args.extend(["--target", target_branch])
        return self._run_gh_cli(args)
    
    def get_latest_release(self) -> Dict[str, Any]:
        """Get latest release."""
        if self._repo:
            try:
                release = self._repo.get_latest_release()
                return {
                    "tag": release.tag_name,
                    "name": release.title,
                    "body": release.body,
                    "url": release.html_url,
                    "published_at": release.published_at.isoformat() if release.published_at else None,
                }
            except:
                pass
        
        return self._run_gh_cli(["release", "view", "--json", "tagName,name,body,url,publishedAt"])
    
    # ========================================
    # WORKFLOW/RUN MANAGEMENT
    # ========================================
    
    def list_workflow_runs(
        self,
        workflow_id: Optional[str] = None,
        branch: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """List workflow runs."""
        args = ["run", "list", "--limit", str(limit), "--json", "databaseId,name,status,conclusion,headBranch,headSha,url,createdAt"]
        if workflow_id:
            args.extend(["--workflow", workflow_id])
        if branch:
            args.extend(["--branch", branch])
        if status:
            args.extend(["--status", status])
        return self._run_gh_cli(args)
    
    def get_workflow_run(self, run_id: int) -> Dict[str, Any]:
        """Get workflow run details."""
        return self._run_gh_cli(["run", "view", str(run_id), "--json", "databaseId,name,status,conclusion,headBranch,headSha,url,createdAt,jobs"])
    
    def rerun_workflow(self, run_id: int) -> Dict[str, Any]:
        """Rerun a failed workflow."""
        return self._run_gh_cli(["run", "rerun", str(run_id)])
    
    def download_workflow_artifacts(self, run_id: int, path: str = ".") -> Dict[str, Any]:
        """Download workflow artifacts."""
        return self._run_gh_cli(["run", "download", str(run_id), "--dir", path])
    
    # ========================================
    # REPOSITORY OPERATIONS
    # ========================================
    
    def get_file_content(self, path: str, ref: Optional[str] = None) -> Optional[str]:
        """Get file content from repository."""
        if self._repo:
            try:
                content = self._repo.get_contents(path, ref=ref)
                if isinstance(content, list):
                    return None
                return content.decoded_content.decode("utf-8")
            except:
                pass
        
        args = ["api", f"repos/{self.config.owner}/{self.config.repo}/contents/{path}"]
        if ref:
            args.extend(["--jq", f".content | @base64d"])
        result = self._run_gh_cli(args)
        return result.get("content") if isinstance(result, dict) else None
    
    def create_file(
        self,
        path: str,
        content: str,
        message: str,
        branch: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a file in the repository."""
        if self._repo:
            ref = self._repo.get_git_ref(f"heads/{branch or self.config.base_branch}")
            self._repo.create_file(path, message, content, branch=branch)
            return {"created": True}
        
        import base64
        encoded = base64.b64encode(content.encode()).decode()
        return self._run_gh_cli([
            "api", "-X", "PUT",
            f"repos/{self.config.owner}/{self.config.repo}/contents/{path}",
            "-f", f"message={message}",
            "-f", f"content={encoded}",
            *(["-f", f"branch={branch}"] if branch else []),
        ])
    
    def update_file(
        self,
        path: str,
        content: str,
        message: str,
        sha: str,
        branch: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a file in the repository."""
        if self._repo:
            self._repo.update_file(path, message, content, sha, branch=branch)
            return {"updated": True}
        
        import base64
        encoded = base64.b64encode(content.encode()).decode()
        return self._run_gh_cli([
            "api", "-X", "PUT",
            f"repos/{self.config.owner}/{self.config.repo}/contents/{path}",
            "-f", f"message={message}",
            "-f", f"content={encoded}",
            "-f", f"sha={sha}",
            *(["-f", f"branch={branch}"] if branch else []),
        ])
    
    def create_branch(self, branch_name: str, from_branch: Optional[str] = None) -> Dict[str, Any]:
        """Create a new branch."""
        source = from_branch or self.config.base_branch
        if self._repo:
            source_ref = self._repo.get_git_ref(f"heads/{source}")
            self._repo.create_git_ref(f"refs/heads/{branch_name}", source_ref.object.sha)
            return {"created": True}
        
        return self._run_gh_cli([
            "api", "-X", "POST",
            f"repos/{self.config.owner}/{self.config.repo}/git/refs",
            "-f", f"ref=refs/heads/{branch_name}",
            "-f", f"sha={source_ref.object.sha}",
        ])
    
    # ========================================
    # UTILITY
    # ========================================
    
    def check_pr_checks(self, pr_number: int) -> Dict[str, Any]:
        """Check if all PR checks pass."""
        if self._repo:
            pr = self._repo.get_pull(pr_number)
            commits = list(pr.get_commits())
            if commits:
                commit = commits[-1]
                checks = list(commit.get_check_runs())
                return {
                    "all_pass": all(c.conclusion == "success" for c in checks),
                    "checks": [
                        {"name": c.name, "status": c.status, "conclusion": c.conclusion, "url": c.html_url}
                        for c in checks
                    ],
                }
        
        # CLI fallback
        result = self._run_gh_cli(["pr", "checks", str(pr_number), "--json", "name,status,conclusion,detailsUrl"])
        checks = result.get("checks", []) if isinstance(result, dict) else result
        return {
            "all_pass": all(c.get("conclusion") == "success" for c in checks),
            "checks": checks,
        }
    
    def add_pr_labels(self, pr_number: int, labels: List[str]) -> Dict[str, Any]:
        """Add labels to PR."""
        if self._repo:
            pr = self._repo.get_pull(pr_number)
            pr.add_to_labels(*labels)
            return {"added": True}
        
        return self._run_gh_cli(["pr", "edit", str(pr_number), "--add-label", ",".join(labels)])
    
    def close_pr(self, pr_number: int, comment: str = "") -> Dict[str, Any]:
        """Close a PR without merging."""
        if self._repo:
            pr = self._repo.get_pull(pr_number)
            if comment:
                pr.create_issue_comment(comment)
            pr.edit(state="closed")
            return {"closed": True}
        
        return self._run_gh_cli(["pr", "close", str(pr_number)])


# Convenience functions
def create_github_client() -> GitHubClient:
    """Create GitHub client from environment."""
    return GitHubClient()


def auto_pr_for_task(
    task_id: str,
    title: str,
    description: str,
    branch_name: str,
    labels: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Automatically create PR for a completed task."""
    client = create_github_client()
    
    body = f"""## Task: {task_id}
    
{description}

### Changes
- Implemented task requirements
- Added tests
- Updated documentation

### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual verification complete

### Checklist
- [ ] Code follows project standards
- [ ] Documentation updated
- [ ] No breaking changes
"""
    
    return client.create_pr(
        title=f"[{task_id}] {title}",
        body=body,
        head_branch=branch_name,
        labels=labels or ["task", task_id.lower()],
    )


if __name__ == "__main__":
    client = create_github_client()
    print(f"GitHub client ready: {client.config.owner}/{client.config.repo}")
    
    # Test
    prs = client.list_prs(state="open", limit=5)
    print(f"Open PRs: {len(prs)}")