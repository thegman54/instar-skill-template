# Instar Skill Template

A starter template for building new skills for [Project Instar](https://github.com/thegman54/project-instar). Use this as a base to create tools your bot can use — API integrations, data lookups, automations, or anything else.

## What's a Skill?

A skill is a package of one or more tools that your Instar bot can execute. Each tool is gated by passphrases through the Gatekeeper — different passphrases unlock different tools, giving you granular permission control.

## Quick Start

### 1. Copy and Rename

```bash
git clone https://github.com/thegman54/instar-skill-template.git my_skill
cd my_skill
```

Rename references in:
- `manifest.yaml` — name, display_name, description, category
- `__init__.py` — import your tool classes
- `tool.py` — rename to match your tool, update the class

### 2. Update manifest.yaml

```yaml
name: my_skill              # lowercase, underscores
display_name: My Skill      # human-readable
description: What this skill does
category: Other              # Profile, Memory, Email, GitHub, etc.
version: "1.0"

credentials:
  - key: MY_API_KEY          # secrets fetched from Infisical at runtime
    description: API key for the service
```

### 3. Implement Your Tool

Edit `tool.py` (or create multiple tool files):

```python
from ..base import BaseTool, ToolResult
from ..registry import register_tool

@register_tool
class MyReadTool(BaseTool):
    @property
    def name(self) -> str:
        return "my_skill_read"

    @property
    def description(self) -> str:
        return "What this tool does"

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"],
        }

    def credential_keys(self) -> list[str]:
        return ["MY_API_KEY"]  # or [] if no credentials needed

    async def execute(self, query: str, **kwargs) -> ToolResult:
        api_key = self.get_credential("MY_API_KEY")
        # Do your thing...
        return ToolResult.ok({"result": "data"})
```

### 4. Add Instructions (Optional)

Create `instructions.md` — an operating guide shown to the bot when this skill is active. Tell the bot how to use the tools, what to watch out for, preferred behavior, etc.

### 5. Install in Instar

**Option A — Admin UI upload:**
1. Zip the directory
2. Upload via **Tools** > **Upload** in the Admin UI

**Option B — Manual:**
```bash
cp -r my_skill/ /path/to/project-instar/tool-executor/src/tools/my_skill/
```

## Naming Convention

Use the `{skill}_{action}` pattern for tool names:
- `my_skill_read` — read-only access
- `my_skill_write` — write/submit (may require approval)
- `my_skill_propose` — changes that need owner approval

Split read and write into separate tools so they can be granted independently.

## File Structure

```
my_skill/
├── manifest.yaml      # Required — metadata, credentials, category
├── __init__.py         # Required — imports tool classes
├── tool.py             # Your tool implementation
├── instructions.md     # Optional — bot operating guide
├── data/               # Optional — editable content (declared in manifest)
└── migrations/         # Optional — SQL migrations (if database: true)
```

## Publishing to BotGlaze

1. Push your repo to GitHub
2. Add the topic **`botglaze`** to your repo
3. Ensure `manifest.yaml` is at the repo root
4. Your skill will appear in BotGlaze search automatically

## License

MIT
