"""Intercept points for this skill  (project-instar → skill).

Every method below is a place project-instar can call INTO this skill when it is part
of the active bot profile — a file was uploaded, a turn is about to run, a conversation
was flagged for learning. They are all NO-OPs here. Override the ones you want; leave the
rest — the empty stubs are intentional so the available intercept points stay OBVIOUS.

The contract (what each hook receives + what to return) lives in the framework:
`tool-executor/src/tools/base.py` → `SkillHooks`. The loader finds this `Hooks` class
and the dispatcher fires it (as a barrier, before the bot's turn).
"""

from ..base import SkillHooks


class Hooks(SkillHooks):

    async def on_file(self, ctx, file):
        """A file arrived with the user's message (name/mime/encoding/data|path).
        Return {"offer": "what I'd do with it"} to bid to handle it, {"staged": {...}}
        for safe pre-processing, or None to ignore."""
        return None

    async def on_ingest(self, ctx, payload):
        """Generic non-file data ingest (paste, webhook). Same contract as on_file."""
        return None

    async def pre_hook(self, ctx, turn):
        """Before the bot acts — return {"context": "guidance/constraints"} to inject, or None."""
        return None

    async def post_hook(self, ctx, turn, draft):
        """Before the bot emits — return {"verdict": "redirect", "reason": "..."} to
        course-correct, or None to allow."""
        return None

    async def on_learn(self, ctx, transcript):
        """A conversation was flagged for learning — return proposals/notes, or None."""
        return None
