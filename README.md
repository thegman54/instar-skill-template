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

## Skill Types

### Simple Skill (default)

Tools run directly inside the tool executor. Good for API calls, database queries, file operations. No Docker needed.

### Database Skill

Add `database: true` to your manifest and include SQL files in a `migrations/` directory. Migrations run automatically on upload and on startup.

```yaml
database: true
```

```
my_skill/
├── manifest.yaml
├── __init__.py
├── tool.py
└── migrations/
    ├── 001_create_table.sql
    └── 002_add_index.sql
```

### Stack Skill (Docker)

For tools that need isolated infrastructure (VPN tunnels, dedicated services, background processes), include a `stack/` directory with a `docker-compose.yml`. On upload, the `stack/` directory is automatically deployed to the stack manager's tools path.

```
my_skill/
├── manifest.yaml          # Skill metadata + credentials
├── __init__.py            # Tool exports
├── tool.py                # Tool bridge — HTTP calls to stack API
├── base.py                # Shared HTTP client to stack
└── stack/                 # Auto-deployed on upload
    ├── docker-compose.yml # Defines the isolated stack
    ├── Dockerfile         # Custom API container
    ├── requirements.txt   # Python deps for stack API
    └── src/
        ├── __init__.py
        ├── api.py         # REST API the tool bridge calls
        └── handler.py     # Core logic
```

**How it works:**
1. Upload the skill zip via Admin UI
2. Tool files go to `src/tools/<name>/` (the skill bridge)
3. `stack/` contents go to `$TOOLS_PATH/<name>/` (the Docker stack)
4. Stack manager auto-discovers the new stack and starts/stops it on demand
5. Your tool bridge makes HTTP calls to the stack API (e.g., `http://<name>-api:8086`)

**The skill bridge pattern:**

```python
import httpx

STACK_API_URL = "http://my-skill-api:8086"

async def call_stack_api(method, endpoint, **kwargs):
    async with httpx.AsyncClient() as client:
        resp = await getattr(client, method)(
            f"{STACK_API_URL}{endpoint}", timeout=30.0, **kwargs
        )
        return resp.status_code == 200, resp.json()
```

Your tools call `call_stack_api()` instead of doing work directly. The stack handles the heavy lifting in its own containers.

**Credentials** for stack skills are fetched from Infisical and passed as environment variables to `docker-compose up`. Declare them in your manifest like any other credential.

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
├── migrations/         # Optional — SQL migrations (if database: true)
└── stack/              # Optional — Docker stack (auto-deployed on upload)
```

## Publishing to BotGlaze

1. Push your repo to GitHub
2. Add the topic **`botglaze`** to your repo
3. Ensure `manifest.yaml` is at the repo root
4. Your skill will appear in BotGlaze search automatically

## License

MIT
