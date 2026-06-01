"""
My Skill — template for creating new tools.

Copy this directory, rename it, update manifest.yaml, and implement execute().
"""

import structlog

from ..base import BaseTool, ToolResult
from ..registry import register_tool

log = structlog.get_logger()


@register_tool
class MySkillTool(BaseTool):
    """Example tool — replace with your implementation."""

    @property
    def name(self) -> str:
        return "my_skill_action"

    @property
    def description(self) -> str:
        return "Describe what this tool does. Claude reads this to decide when to use it."

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The input to process",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results to return",
                    "default": 10,
                },
            },
            "required": ["query"],
        }

    def credential_keys(self) -> list[str]:
        # Must match the keys in manifest.yaml credentials section.
        # These are fetched from Infisical and available via self.get_credential().
        return ["MY_API_KEY"]

    async def execute(self, query: str, limit: int = 10, **kwargs) -> ToolResult:
        """
        Execute the tool.

        Credentials are available via self.get_credential("MY_API_KEY").
        Session context is available via self._session_id and self._gatekeeper_url
        (for tools that need to call gatekeeper endpoints directly).
        Grant metadata is available via self.get_grant_metadata("key").
        """
        api_key = self.get_credential("MY_API_KEY")

        log.info("my_skill_execute", query=query, limit=limit)

        # --- Your implementation here ---

        return ToolResult.ok({
            "results": [],
            "query": query,
            "message": "Replace this with real results",
        })
