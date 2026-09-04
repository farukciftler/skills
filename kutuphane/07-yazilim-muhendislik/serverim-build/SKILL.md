---
name: serverim-build
description: Drive headless Claude Code runs on Faruk's Linux server through the Serverim MCP connector — writing a spec, launching the build detached in tmux, monitoring it without killing it, resuming it, and independently verifying the result. Use this skill whenever the user wants something built, deployed, audited, refactored or scaffolded on their server ("sunucuda", "serverim", "sunucuya kur", "spec'i uygula", "yeni proje aç", "claude'a yaptır", "deploy et", "docker'a al", "landing page ekle"), whenever a tmux/headless `claude -p` run needs to be started, checked, resumed or debugged, and whenever a previous run's output (SONUC.md, DENETIM.md, containers, ports) needs verifying. Also use it before writing any spec that a headless agent will implement on that host, so the deployment constraints land in the spec instead of being discovered mid-build.
---

# Remote Claude Code builds on Faruk's server

The pattern: **write a precise spec → hand it to a headless Claude Code process running detached on the server → monitor read-only → verify independently → report honestly.** The chat session is the architect and the auditor; the server process is the builder.

The failure modes are almost never "the model can't code." They are: the run gets killed by accident, the run is assumed dead when it's alive, the build collides with the 30+ containers already on that host, or its own completion report is taken at face value. This skill exists to prevent those four.

## Server facts (verify, don't assume — they drift)

- `claude` binary: `/root/.local/bin/claude` — **not** on the PATH of non-login shells that `komut_calistir` uses. Always call it by absolute path.
- The host runs many unrelated production containers (postgres17, redis-glottora, adminer, n8n, mongo, various app backends). Default ports 3000, 5432, 5678, 6379, 8080, 27017 are taken.
- Shell is root. tmux is installed. Docker + compose available.
- Projects live in `/root/projects/<slug>/`.

## Step 1 — Preflight inventory

Before writing the spec's deployment section, look at the actual machine:

```bash
docker ps --format '{{.Names}} | {{.Image}} | {{.Ports}}'
ss -tlnp | grep -E ':(<candidate ports>)\s' || echo "FREE"
df -h / ; free -m
/root/.local/bin/claude --version
```

Pick host ports from the high range (63620+) after confirming they're free. Never propose a default port.

## Step 2 — Spec, then a deployment addendum

Write the spec locally, copy it to `/root/projects/<slug>/spec.md` via `Serverim:dosya_yaz`, then **compare md5 both sides** — large writes are chunked and silent truncation is the one corruption you won't notice by eye:

```bash
md5sum /root/projects/<slug>/spec.md   # must equal the local md5sum
```

Then append a deployment addendum to the spec — constraints belong in the artifact the builder reads, not only in the launch prompt (the prompt is one paragraph the agent may drift from; the spec it re-reads all run). Cover, at minimum:

1. **Inspect before creating** — `docker ps` at build time is truth; the snapshot in the spec may have drifted.
2. **Reuse existing infrastructure.** Name the container (e.g. `postgres17`), tell it to read credentials via `docker inspect`, create a dedicated role + database, connect over `host.docker.internal` with `extra_hosts: ["host.docker.internal:host-gateway"]`, and never touch neighbouring databases. Same for Redis — but require verifying `maxmemory-policy=noeviction` before sharing it with BullMQ, and forbid changing the shared instance's config; fall back to a private container if the check fails.
3. **Exact host ports**, with container-internal ports unchanged, and a note about which defaults are occupied.
4. **Never modify, restart or stop a container it did not create.** Compose project name and `<slug>-*` naming, `restart: unless-stopped`.
5. **Safe defaults on first boot** — outbound channels in dry-run, no real sends, no live credentials.
6. **Finish by writing `SONUC.md`**: ports/URLs, the wiring actually used, migration/seed status, and everything skipped or left incomplete.

## Step 3 — Launch detached

```bash
tmux kill-session -t <slug> 2>/dev/null; sleep 1
tmux new -d -s <slug>
tmux send-keys -t <slug> 'cd /root/projects/<slug> && IS_SANDBOX=1 /root/.local/bin/claude -p "<prompt>" --model claude-opus-4-8 --dangerously-skip-permissions 2>&1 | tee -a claude.log' Enter
sleep 25
pgrep -af 'local/bin/claude' | grep -v '/bin/sh' | head -1
```

Why each piece:

- `IS_SANDBOX=1` — without it, `--dangerously-skip-permissions` refuses to run as root ("cannot be used with root/sudo privileges"). This is the single most common launch failure.
- `--model claude-opus-4-8` — pin the version explicitly; `--model opus` floats to whatever is newest.
- `tee -a` (append, and a fresh log name per phase if you want them separate) — `tee` without `-a` erases the previous run's log on resume.
- `2>&1` — otherwise the interesting failures go nowhere.
- **ASCII-only prompt text.** `send-keys` mangles Turkish characters; write the prompt in ASCII Turkish (`calistir`, `duzelt`) and use only single quotes outside, double quotes inside — no nesting beyond that.
- Confirm the PID after ~25 s. A launch that failed on permissions dies instantly and silently from the caller's point of view.

## Step 4 — Monitor without killing it

**Never `tmux attach`.** Anything typed — including a pasted monitoring command — lands in the running process's terminal, and a stray Ctrl-C ends a 40-minute build. This has already happened once; it cost a half-finished deploy.

Read-only checks, all safe from a separate shell:

```bash
tmux capture-pane -pt <slug> -S -60          # last 60 lines of the pane
pgrep -af 'local/bin/claude' | grep -v '/bin/sh'
ls -la /root/projects/<slug>/                 # file mtimes = real progress
docker ps -a --format '{{.Names}} | {{.Status}} | {{.Ports}}' | grep <slug>
ls /root/projects/<slug>/SONUC.md              # exists ⇒ finished
```

`claude -p` buffers its output until the end, so **`claude.log` staying at 0 bytes means nothing.** Judge liveness by the process and by file mtimes, and say so when reporting — otherwise the user reasonably concludes it hung.

Give the user this exact set when they ask how to watch it, with the "don't attach" warning attached. It's the part people get wrong.

## Step 5 — Resume, don't restart

`claude -c -p "<prompt>"` continues the previous session in that directory with its context intact. Use it for every follow-up phase (fix the bugs, add the landing page, run an audit) — a fresh `-p` re-reads the whole spec from zero and tends to re-litigate finished decisions.

When resuming after an interruption, state the remaining work explicitly as a numbered list, including anything the previous phase reported as broken. Don't say "devam et" alone.

## Step 6 — Verify independently

The build agent writes its own report. Read it, then check the claims yourself — not out of distrust, but because the two most useful things you can tell the user are "this claim is true" and "this one isn't, here's what's actually there."

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:<web port>/
curl -s http://127.0.0.1:<api port>/healthz
docker ps -q | wc -l                                    # foreign containers all still up?
docker exec <db container> psql -U postgres -tAc "select datname from pg_database where datname='<slug>'"
docker exec <db container> psql -U postgres -d <slug> -tAc "select count(*) from information_schema.tables where table_schema='public'"
docker logs --tail 20 <slug>-worker 2>&1 | grep -i err
```

Look specifically for things a self-report tends to omit: jobs stuck in `queued`, containers in `Exited (0)`, hardcoded public IPs in user-facing URLs, secrets written into the repo, and any drift from the addendum's rules.

Then report in this shape: **what works (verified) → what the agent itself flagged as incomplete → what you found that it didn't mention → the one thing worth doing next.** Don't bury a real defect under a success summary, and don't inflate a clean run with hedges.

## Failure playbook

| Symptom | Cause | Fix |
|---|---|---|
| `--dangerously-skip-permissions cannot be used with root` | running as root | prefix `IS_SANDBOX=1` |
| `claude: command not found` | non-login shell PATH | absolute path `/root/.local/bin/claude` |
| Log empty, no output for minutes | `-p` buffers to the end | check `pgrep` + file mtimes, not the log |
| Process vanished mid-run | someone attached to tmux and typed | relaunch with `-c`, never attach |
| Container name collision / port in use | stale check | `docker ps -a`, `ss -tlnp`, pick a free high port |
| Env value parsed with its trailing comment | `KEY=value  # note` in `.env` via compose | comments on their own line + trim in the config loader |
| Spec looks truncated on the server | chunked write | rewrite the missing chunk, re-verify md5 |

## Housekeeping

Record durable outcomes in memory as they're decided: project slug and path, the host ports assigned, which shared services it reuses. Ports and wiring are exactly what future-you needs and exactly what nobody writes down twice.

Keep secrets out of chat and out of the repo: read generated passwords with `grep` on the server when needed, don't echo them into the conversation.
