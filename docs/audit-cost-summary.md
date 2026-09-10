# Claude Code session timing and model inventory

Generated 2026-08-25 from Claude Code session logs under `~/.claude/projects/`.
Read-only extraction; no session file was modified.

**Headline result: the evidence needed to answer the reviewers' person-hours
question does not exist on this machine.** Project A has zero surviving session
logs. Project B has exactly one surviving session log, and it is the
in-progress session that produced this document. The tables below are reported
as computed, but they measure the survival of log files, not the effort spent.

---

## Step 1 — Directory matching

Path-hash rule, per `src/aivs/adapters/claude_code.py:145`
(`ClaudeCodeAdapter._project_dir`): the absolute project path with `/` replaced
by `-`, resolved under `~/.claude/projects/`.

| Target | Expected directory | Result |
|---|---|---|
| A — `/storage/kiran-stuff/IDP_projects/mechanism_classifier` | `-storage-kiran-stuff-IDP_projects-mechanism_classifier` | **absent** |
| B — `/storage/kiran-stuff/aivs` | `-storage-kiran-stuff-aivs` | **matched exactly**, 1 `.jsonl` |

### Project A — what was searched, and on what basis

All 72 directories under `~/.claude/projects/` were listed. No directory matches
`mechanism_classifier` under any normalisation. The directories that do exist for
sibling projects (`-storage-kiran-stuff-IDP-projects-kappa-friction`,
`-storage-kiran-stuff-IDP-projects-ensemble-benchmark`,
`-storage-kiran-stuff-IDP-projects-idrome-candidates`) reveal the CLI's actual
normalisation: `_` and `.` are collapsed to `-` in addition to `/`. So the true
expected name is `-storage-kiran-stuff-IDP-projects-mechanism-classifier`. That
directory does not exist either.

Note this is a real defect in the shipped adapter: `_project_dir` performs only
`str.replace("/", "-")`, so it would fail to locate any project whose path
contains `_` or `.` even when the logs are present. `session_dir_override`
is the existing workaround.

Four independent checks confirm the absence rather than a naming miss:

1. **Fuzzy match over all 72 directories** — no candidate.
2. **Content grep** — `grep -rl "mechanism_classifier"` across the entire
   corpus (1043 `.jsonl` files, ~750 MB) returns only this session's own log and
   an unrelated memory file. No historical session anywhere references the
   project, including under a parent `cwd`.
3. **`cwd`-field scan** — every session directory was opened and its recorded
   `cwd` read. No session reports a `cwd` under `IDP_projects/mechanism_classifier`.
4. **UUID search** — `~/.claude/history.jsonl` names session
   `7d3cd00e-ea4a-45e6-88e1-128d0f99b98d` for this project (4 prompts,
   2026-03-16 20:35 → 21:16 UTC). A filesystem-wide `find` for that UUID
   returns nothing. The transcript is deleted, not misplaced.

Corroborating that sessions *did* run: the MCP log cache
`~/.cache/claude-cli-nodejs/-storage-kiran-stuff-IDP-projects-mechanism-classifier/`
exists with mtime 2026-03-16 15:35 local. Only the MCP side-logs survived; the
session transcripts did not.

### Alternate Claude home

No `CLAUDE_HOME` environment variable is set, so the adapter's default
(`~/.claude`) applies. `/storage/kiran-stuff/.claude/` exists but contains only
`CLAUDE.md` and `settings.local.json` — no `projects/` directory. No session
backups exist in `~/.claude/backups/` (which holds only `.claude.json` copies)
or `~/.claude/local_backup/`.

### Evidence of truncation

Session history is substantially incomplete, and not only for project A:

- **Six of the nine `IDP*` project directories exist but contain zero `.jsonl`
  files** — the directories survived, their contents did not. In total 33 of 72
  project directories are empty.
- **`-storage-kiran-stuff-aivs/` holds exactly one session log**, created
  2026-08-25, which is this session. Every aivs session from the audit
  construction and manuscript preparation period (May–July 2026) is gone.
- **`~/.claude/history.jsonl` is itself rotated.** It attributes 57 aivs prompts
  spanning 2026-05-12 → 2026-07-02 to a single session UUID
  (`c9082132-863d-4627-bc1b-9a196f5d2048`), which cannot be a single session.
  It retains prompt text and timestamps only — no assistant events, no model
  identifiers, no tool calls — so it cannot supply Step 2 or Step 6 fields.

No `cleanupPeriodDays` setting is configured, so the default retention policy
applied and expired the older transcripts.

---

### Step 4 — Project A (mechanism_classifier) phase aggregation

| Phase | Sessions | Raw span (h) | Active 15-min cap (h) | Active 30-min cap (h) | Events |
|---|---:|---:|---:|---:|---:|
| pipeline | 0 | 0.00 | 0.00 | 0.00 | 0 |
| audit | 0 | 0.00 | 0.00 | 0.00 | 0 |
| later | 0 | 0.00 | 0.00 | 0.00 | 0 |
| **total** | **0** | **0.00** | **0.00** | **0.00** | **0** |

**No session logs for project A exist on this machine. All values are zero because there is nothing to measure, not because the effort was zero.**

### Step 5 — Project B (aivs) aggregation

| Subset | Sessions | Raw span (h) | Active 15-min cap (h) | Active 30-min cap (h) | Events |
|---|---:|---:|---:|---:|---:|
| all aivs sessions | 1 | 0.05 | 0.05 | 0.05 | 92 |
| first event >= 2026-06-01 | 1 | 0.05 | 0.05 | 0.05 | 92 |

### Step 6 — Model inventory (from surviving session logs)

| Model identifier | Project(s) | First seen | Last seen | Sessions | Assistant events |
|---|---|---|---|---:|---:|
| `claude-opus-5` | B | 2026-08-25 | 2026-08-25 | 1 | 39 |
The single project B row is session `5636c93c-cccb-4d4c-a28b-5394cb9c1d2e`,
which is the session that generated this file. It was still in progress when
the extraction ran, so its span, active time and event count are a partial
snapshot and describe only this extraction task. It is **not** evidence about
the AIVS audit construction or manuscript preparation, and it should not be
cited as such.

---

## Method and caveats

**Gap-capping rule.** For each session, events were sorted by timestamp and the
intervals between consecutive events summed. Any interval strictly longer than
the threshold was treated as idle and excluded from the sum entirely (not
truncated to the threshold). Both a 15-minute and a 30-minute threshold are
reported so the sensitivity of the estimate is visible. Raw wall-clock span
(last event minus first event) is reported alongside, and over-counts whenever
a session was left open.

**Lower bound on human effort.** These figures cover AI-assisted session time
only. Reading, thinking, offline writing, literature work, running and waiting
on computation outside a session, and any work done in another tool are all
invisible to this method. Any person-hours figure derived from session logs is
therefore a **lower bound** on total human effort, and should be presented as
such.

**Event counting.** `total_events` is the number of parseable JSONL records in
the file, including bookkeeping record types (`queue-operation`, `attachment`,
`last-prompt`) that the AIVS adapter skips during normalisation. It is a measure
of log volume, not of decisions. Records lacking a parseable timestamp are
counted in `total_events` and reported separately in
`events_without_timestamp`; they are excluded from all timing arithmetic.

**Model identifiers** are read from `message.model` on records of type
`assistant`, verbatim, with no normalisation of aliases or version suffixes.

**What could not be located.**

- Project A (`/storage/kiran-stuff/IDP_projects/mechanism_classifier`): **all**
  sessions. Zero rows are reported. Per the extraction brief, no substitute
  figures were derived from git timestamps, from `history.jsonl` prompt counts,
  or from any other proxy. The audited workflow's cost is not recoverable from
  session logs on this machine.
- Project B (`/storage/kiran-stuff/aivs`): all sessions before 2026-08-25,
  which is to say the entire AIVS audit-construction and manuscript-preparation
  period. Only the current in-progress session survives.

**Consequence for the manuscript.** The reviewers' person-hours request cannot
be answered from session telemetry as intended. The two options that remain
honest are (a) report the partial cost metadata in the appendix below with its
limitations stated explicitly, or (b) state that the retrospective audit's cost
was not instrumented at the time and report it from author recollection, marked
as such. Fabricating a reconstructed figure is not an option, and would be
self-refuting in a paper about audit provenance.

This is itself a finding worth reporting in the paper: a retrospective audit is
hostage to the retention policy of the tools it audits. Default Claude Code
session retention silently expired the primary evidence for both the audited
workflow and the audit of it. An `honest-omission` gap of exactly this kind is
what the AIVS schema is designed to surface rather than hide.

---

## Appendix — corroborating cost metadata (NOT from session JSONL)

`~/.claude.json` retains a per-project summary of the **most recent session
only**. These are real recorded values, not estimates. They are reported here
because they bear directly on the manuscript's AI-use disclosure gap, but they
**cannot** support the per-session, phase-level, or active-time figures
requested in Steps 2–5, and they describe one session per project rather than
the full history.

### A — `/storage/kiran-stuff/IDP_projects/mechanism_classifier`

Last session `7d3cd00e-ea4a-45e6-88e1-128d0f99b98d`; project files first
indexed 2026-03-16 20:35 UTC — the date of the numerical/statistical audit.

- `lastCost`: **USD 4.11**
- `lastDuration`: 11,157,142 ms (**3.10 h** wall-clock)
- `lastAPIDuration`: 1,247,311 ms (**20.8 min** of model time)
- `lastToolDuration`: 348,664 ms (5.8 min)
- lines added / removed: 668 / 51
- tokens: 27,064 in / 72,037 out; 423,323 cache-create; 4,222,098 cache-read

| Model | Input | Output | Cache read | Cost USD |
|---|---:|---:|---:|---:|
| `claude-opus-4-6[1m]` | 8,029 | 43,710 | 2,764,935 | 3.47 |
| `claude-haiku-4-5-20251001` | 19,035 | 28,327 | 1,457,163 | 0.64 |

### B — `/storage/kiran-stuff/aivs`

Last session before the current one: `c9082132-863d-4627-bc1b-9a196f5d2048`;
last start time recorded 2026-06-30 06:11 UTC.

- `lastCost`: **USD 108.16**
- `lastDuration`: 186,529,761 ms (**51.8 h** wall-clock; this figure spans an
  editor left open across days and is not active time)
- `lastAPIDuration`: 7,255,463 ms (**2.02 h** of model time)
- `lastToolDuration`: 707,655 ms (11.8 min)
- lines added / removed: 2,527 / 535
- tokens: 315,390 in / 487,955 out; 5,767,179 cache-create; 81,923,517 cache-read
- 14 web-search requests

| Model | Input | Output | Cache read | Cost USD |
|---|---:|---:|---:|---:|
| `claude-opus-4-7` | 13,368 | 408,521 | 79,194,403 | 102.62 |
| `claude-opus-4-7[1m]` | 15,549 | 76,059 | 2,729,114 | 5.10 |
| `claude-haiku-4-5-20251001` | 286,473 | 3,375 | 0 | 0.44 |

**Reading this appendix carefully.** `lastAPIDuration` is the most defensible
of these quantities — it is measured model-inference time and is a hard lower
bound on session activity. `lastDuration` is wall-clock for the session process
and over-counts badly (project B's 51.8 h cannot be active work). Neither is a
person-hours figure. If any number from this appendix is used in the
manuscript, it must be attributed to Claude Code's own per-project telemetry,
scoped to a single session, and labelled a lower bound.

### Models to name in the AI-use disclosure

Every model identifier observed on this machine for these two projects, from
all sources (session logs plus `.claude.json` telemetry):

| Model identifier | Project | Source |
|---|---|---|
| `claude-opus-4-6[1m]` | A | `.claude.json` telemetry |
| `claude-haiku-4-5-20251001` | A, B | `.claude.json` telemetry |
| `claude-opus-4-7` | B | `.claude.json` telemetry |
| `claude-opus-4-7[1m]` | B | `.claude.json` telemetry |
| `claude-opus-5` | B | session log (this session only) |

Claude Code CLI version currently in use: **2.1.245**
(`~/.local/share/claude/versions/2.1.245`). The version in use during the
audited work is not recoverable; `.claude.json` records `lastVersionBase`
**2.1.198** for project B.
