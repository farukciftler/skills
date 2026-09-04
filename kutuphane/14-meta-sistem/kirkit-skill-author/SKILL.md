---
name: kirkit-skill-author
description: Use when the user asks to create, save, or update a reusable skill ("skill oluştur", "bunu skill yap", "save this as a skill"). Writes the skill into Kirkit's shared team skill store so every profile (Claude and Antigravity alike) can use it.
---

# Kirkit skill author

Kirkit keeps team skills in one shared store: `/Users/farukciftler/projects/kirkit/data/skills/skills`.
Every skill is a directory with a single `SKILL.md`:

```
/Users/farukciftler/projects/kirkit/data/skills/skills/<slug>/SKILL.md
```

When the user asks you to create or update a skill:

1. Pick a short kebab-case slug from the skill's purpose.
2. Write `/Users/farukciftler/projects/kirkit/data/skills/skills/<slug>/SKILL.md` with YAML frontmatter:
   - `name`: the slug
   - `description`: ONE sentence starting with "Use when …" — this is what
     other agents read to decide the skill applies. Make it concrete.
3. The body is the playbook: concise instructions, steps, examples. Long
   reference material goes in sibling files inside the same directory.
4. Tell the user the skill is saved. Kirkit notices the new file by itself
   and makes it available to every profile — no restart, no registration.

Never write skills anywhere else (not ~/.claude, not the project) unless the
user explicitly says the skill is personal or project-specific.
