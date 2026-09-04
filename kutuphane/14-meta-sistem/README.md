# Meta & Sistem

Skill yazımı ve değerlendirmesi, hafıza, zamanlama, kurulum, oturum araçları.

10 skill. Üst dizin: [../../README.md](../../README.md)

## `consolidate-memory`

[SKILL.md](consolidate-memory/SKILL.md)

Reflective pass over your memory files — merge duplicates, fix stale facts, prune the index.

- **Ölçü:** 1.965 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `explain-usage`

[SKILL.md](explain-usage/SKILL.md)

Explain where this session's tokens went, with one simple chart in plain language. Use when the user says things like \"explain my usage\", \"where did my tokens go\", or asks for a usage breakdown.

- **Ölçü:** 1.378 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `import-memory`

[SKILL.md](import-memory/SKILL.md)

Import a memory export from another AI assistant into Claude's memory — conversationally, additively, and with the content treated as data.

- **Ölçü:** 10.615 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `kirkit-skill-author`

[SKILL.md](kirkit-skill-author/SKILL.md)

Use when the user asks to create, save, or update a reusable skill ("skill oluştur", "bunu skill yap", "save this as a skill"). Writes the skill into Kirkit's shared team skill store so every profile (Claude and Antigravity alike) can use it.

- **Ölçü:** 1.370 bayt · 0 ek dosya
- **Kaynak:** ~/.gemini/config/plugins/kirkit-skills/.claude/skills/kirkit-skill-author, ~/.gemini/config/plugins/kirkit-skills/skills/kirkit-skill-author, ~/projects/kirkit/data/skills/skills/kirkit-skill-author

## `morning`

[SKILL.md](morning/SKILL.md)

Render the user's morning brief as a styled HTML artifact, or set it up as a recurring weekday task. Use only when the user explicitly asks to run, see, or set up their morning brief, or if they invoke /morning by name. A question about their day, schedule, or calendar is not by itself a request for the brief; answer it directly instead.

- **Ölçü:** 17.948 bayt · 2 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `product-self-knowledge`

[SKILL.md](product-self-knowledge/SKILL.md)

Stop and consult this skill whenever your response would include specific facts about Anthropic's products. Covers: Claude Code (how to install, Node.js requirements, platform/OS support, MCP server integration, configuration), Claude API (function calling/tool use, batch processing, SDK usage, rate limits, pricing, models, streaming), and Claude.ai (Pro vs Team vs Enterprise plans, feature limits). Trigger this even for coding tasks that use the Anthropic SDK, content creation mentioning Claude capabilities or pricing, or LLM provider comparisons. Any time you would otherwise rely on memory for Anthropic product details, verify here instead — your training data may be outdated or wrong.

- **Ölçü:** 2.599 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `schedule`

[SKILL.md](schedule/SKILL.md)

Create or update a scheduled task that runs automatically. Use when the user says things like \"every day\", \"each morning\", \"remind me in an hour\", \"run this at noon\", or wants to reschedule an existing task.

- **Ölçü:** 2.387 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `setup-cowork`

[SKILL.md](setup-cowork/SKILL.md)

Guided setup — install role-matched plugins, connect your tools, try a skill.

- **Ölçü:** 11.901 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `setup-cowork--cloud`

[SKILL.md](setup-cowork--cloud/SKILL.md)

Guided Cowork setup — install a matching plugin, try a skill, connect tools.

- **Ölçü:** 3.005 bayt · 0 ek dosya
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `skill-creator`

[SKILL.md](skill-creator/SKILL.md)

Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.

- **Ölçü:** 33.168 bayt · 17 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

