# Tagging and Zenodo minting — Job 3b

2026-09-08, host `boron`. CiSE-2026-06-0105.

## STATUS: COMPLETE except step 6 (license metadata)

> **Resolved 2026-09-10.** Zenodo recovered and both webhooks were redelivered.
> Both version DOIs are minted and both archives verified. See *Addendum —
> minting completed* at the end of this document. The status section below is
> the record of the outage as it stood on 2026-09-08 and is retained unchanged.

## (2026-09-08) STOPPED AT STEP 5 — Zenodo is down

**Steps 1 through 4 completed. Both repositories are merged, pushed, tagged and
released. No Zenodo record was minted, because zenodo.org is returning HTTP 504
and every GitHub webhook delivery failed.**

**There are no new version DOIs. Job 5 step 3 remains blocked.** Nothing was
invented to fill that gap.

---

## Step 1 — branches landed

| Repo | Before | After | Merge |
|---|---|---|---|
| idp | `f72f008` | **`196d59f`** | `cise-r1-figures`, fast-forward, no conflict |
| aivs | `0e47e2a` | **`183dfb5`** | `cise-r1-audit-record`, fast-forward, no conflict |

Both pushed. No rebase, no force-push.

### One defect found and fixed during this step

The aivs checkout initially aborted, which surfaced a real problem:
`var_manuscript.docx` and `var_manuscript.pdf` were tracked at **both** the
repository root **and** `legacy/`. Commit `2e1c43c` had added the `legacy/`
copies but never staged the root deletions, because those two files were moved
with plain `mv` rather than `git mv`.

Left alone, the archive would have shipped **two copies of the superseded
Patterns manuscript** — the exact outcome step 2c exists to prevent. Fixed in
`de63d95`. `var_manuscript.md` was moved with `git mv` and was not affected.

Also committed: the author's response-matrix **row 3.10** (`183dfb5`), which was
present in the working tree and would otherwise not have been in the archive.

## Step 2 — the three cleanups

All three were completed during Job 2 and landed on `master` via the step 1
merge. Verified on `master` rather than redone:

| Item | Check | Result |
|---|---|---|
| 2a | `.gitignore` present | yes |
| 2a | tracked `__pycache__/*.pyc` | **0** (was 16) |
| 2b | `pyproject.toml` version | **`0.2.2`** |
| 2b | other version strings disagree? | **no** |
| 2c | `legacy/` tracked contents | 6 files |
| 2c | Patterns-era files at root | **none** |

On 2b: `src/aivs/vocabulary/v0_1.py` declares `VOCABULARY_VERSION = "0.1.0"`.
That is **correct and was not changed** — the vocabulary genuinely is at 0.1.0
and is deliberately near-empty. It is a different quantity from the package
version, not a disagreement.

## Step 3 — pre-tag verification

### idp — PASS

| Item | Count | Status |
|---|---|---|
| Variant dataset (core) | 13/13 | PRESENT |
| EVE data | 14/14 | PRESENT |
| Analysis scripts 01-21 | 21/21 | PRESENT |
| Figure scripts | 10/10 | PRESENT |
| Figure outputs | 26/26 | PRESENT |
| Environment manifest | 1/1 | PRESENT |
| README / LICENSE | 1/1, 1/1 | PRESENT |
| Vendored `src/` module | 3/3 | PRESENT |
| Named data tables | 13/13 | PRESENT |
| kdense_predictors | 8/8 | PRESENT |

**263 tracked files, zero absent** (260 at Job 1 step 4, plus the three
vendored `src/` files).

- Regenerated Figure 2 is the tracked copy: `master` blob and working copy both
  md5 `c2b48288c37b…`
- `table_s1_regions.csv` on `master`: **0** HTT rows
- `16_supplementary_tables.py` on `master`: `EXCLUDED_GENES` present, 3
  occurrences (definition + two applications)

### aivs — PASS

| Check | Expected | Actual |
|---|---|---|
| `mechanism_classifier_audit.json` md5 | `1e6f79d0…` | `1e6f79d0…` |
| `..._published.json` md5 | `82585f43…` | `82585f43…` |
| `capture_tier_achieved` | TIER_1 | **1** |
| adapters | manual/git at tier 1 | `[('manual',1),('git',1)]` |
| `pytest tests/` | 45 | **45 passed** |

`AIVS-VAR` on `master` — five occurrences, all in the deliberate set, none
load-bearing:

| File | n | Why retained |
|---|---:|---|
| `docs/cise-r1-response-matrix.md` | 1 | verbatim reviewer question, row 5.9 |
| `HISTORY.md` | 1 | dated decision log |
| `legacy/README.md` | 1 | states the term is retired |
| `legacy/apply_qss_revisions.py` | 6 | superseded Patterns-era artefact |
| `legacy/var_manuscript.md` | 8 | superseded Patterns-era manuscript |

Zero occurrences in `README.md`, `examples/`, `src/`, `schema/`, or either
audit record.

## Step 4 — tags and releases created

| Repo | Tag | Commit | Release |
|---|---|---|---|
| idp | `v1.0-cise-r1` | `196d59f` | https://github.com/khatvangi/idp-mechanism-classifier/releases/tag/v1.0-cise-r1 |
| aivs | `v0.2.2-paper` | `183dfb5` | https://github.com/khatvangi/aivs/releases/tag/v0.2.2-paper |

Both annotated tags, both releases published (not drafts), created
2026-09-08T23:01:11Z and 23:01:23Z.

## Step 5 — BLOCKED: Zenodo outage

### The service is down

```
https://zenodo.org/api/records/20723560   -> HTTP 504 Gateway Time-out
https://doi.org/10.5281/zenodo.20723560   -> HTTP 504
```

TCP connects and the TLS handshake completes (`SSL certificate verify ok`,
connected to 188.184.98.114:443), then **zero bytes are returned** until
timeout. This is server-side, not local: `api.crossref.org` and
`api.github.com` both returned HTTP 200 from this host in the same minute.

### Every webhook delivery failed — nothing is queued

The Zenodo integration webhook is active on both repositories and correctly
subscribed to `release`. GitHub attempted delivery and **gave up after one
attempt each**:

| Repo | Delivery id | Action | Code |
|---|---|---|---|
| aivs | `3841651795600417000` | published | **500** |
| aivs | `3841651795600351000` | created | **500** |
| aivs | `3841651795594051600` | released | **500** |
| idp | `3841651769639715000` | released | **500** |
| idp | `3841651769501311000` | published | **500** |
| idp | `3841651748919836700` | created | **403** |

The 500s carry `context deadline exceeded (Client.Timeout exceeded while
awaiting headers)` — GitHub timed out waiting for Zenodo.

**Consequence: Zenodo never received the release events.** Minting will *not*
happen by itself when the service recovers, because GitHub is not retrying.

### The remedy — redeliver, do not recreate

Once `https://zenodo.org/api/records/20723560` returns 200, redeliver the
`published` event on each repository:

```bash
gh api -X POST repos/khatvangi/aivs/hooks/642728386/deliveries/3841651795600417000/attempts
gh api -X POST repos/khatvangi/idp-mechanism-classifier/hooks/642727930/deliveries/3841651769501311000/attempts
```

Then confirm each concept DOI resolves to the new version:

```bash
curl -s https://zenodo.org/api/records/20723558 | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['id'],d['doi'],d['metadata']['version'])"
curl -s https://zenodo.org/api/records/20723560 | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['id'],d['doi'],d['metadata']['version'])"
```

**Do not delete and recreate the releases to force a new webhook.** Deleting a
release that Zenodo may have partially processed risks a half-formed deposit,
and recreating tags rewrites the archive's provenance for no benefit. The
redelivery endpoint replays the identical payload.

A read-only recovery poller is running on this host
(`/tmp/claude-1000/zenodo-poll.log`), checking every 45 s. It only observes; it
does not redeliver.

## Steps 5 and 6 — outstanding

- New version DOIs: **not minted.** Job 5 step 3 blocked.
- Post-mint archive verification against the step 3 tables: **not performed.**
  This must still be done — a minted DOI pointing at an incomplete archive is
  the failure this repair exists to correct.
- License metadata `apgl-v3` → `agpl-3.0` on both records: **not performed.**
  Requires the Zenodo API, which is unreachable. Note this also needs an
  authenticated token; none is configured on this host outside the webhook URL.

## Security note

The Zenodo integration webhook embeds a plaintext access token in its URL,
which is how Zenodo's GitHub integration works but means the token is visible
in `repos/{owner}/{repo}/hooks` output and in webhook delivery logs. It was
surfaced into this session's transcript while diagnosing the delivery failures.
It grants deposit access to the Zenodo account. Rotate it in the Zenodo GitHub
settings if this transcript is shared.

## Unchanged and safe

- `var_manuscript_cise.md` — untouched, md5 `34ef424c8f9ecefd95a1ced65fd1f414`
- Existing Zenodo records `20723559` and `20723561` — untouched; `3ca6dead`
  remains reachable, so both still resolve once the service is back


---

# Addendum — minting completed

2026-09-10, host `boron`.

## Both version DOIs minted

| Repo | Tag | Version DOI | Concept DOI | Archive |
|---|---|---|---|---|
| `khatvangi/aivs` | `v0.2.2-paper` | **10.5281/zenodo.22698585** | 10.5281/zenodo.20723558 | 7,466,217 B, md5 `00adfeb03bc81ecb0a403c3f7d826802` |
| `khatvangi/idp-mechanism-classifier` | `v1.0-cise-r1` | **10.5281/zenodo.22698586** | 10.5281/zenodo.20723560 | 21,567,530 B, md5 `69e9c6c117e7fec041108ab3d3fe621c` |

Both concept DOIs now resolve to the new versions. The prior records
(`20723559`, `20723561`) remain reachable.

## Two failures on the way, both worth recording

**1. The recovery poller never fired.** It treated only HTTP 200 as recovery.
The Zenodo record API answers **302** (a redirect), so the poller logged
`HTTP 302` as "still down" and ran to exhaustion. Zenodo had been up for hours.
A liveness check that does not follow redirects is not a liveness check.

**2. The captured delivery IDs were corrupted by JSON number rounding.**
GitHub webhook delivery ids exceed 2^53 — e.g. `3841651795600416768`. Read
through `jq`, they are parsed as IEEE doubles and silently rounded to
`3841651795600417000`. The first redelivery attempts returned 404 on ids that
never existed. Re-reading the raw JSON with a regex, without number parsing,
gave the true ids and both replays succeeded.

This is the same failure shape as the adapter and its test fixture: the
mechanism reported success at every step it could see, and the artifact it
produced was wrong. A 404 from a rounded identifier is indistinguishable from a
404 from an expired one unless you check the identifier itself.

## Redelivery

| Repo | Delivery id | Result |
|---|---|---|
| aivs | `3841651795600416768` (release/published) | **202** |
| idp | `3841651769501310976` (release/published) | **202** |

Zenodo minted both within ten seconds. The releases were not deleted or
recreated; the redelivery replayed the identical payload.

## Step 5 — archive verification

Both archives were downloaded, md5-matched against the record metadata, and
checked for contents. Presence was not assumed from a successful release.

| | idp | aivs |
|---|---:|---:|
| Files in archive | 263 | 80 |
| **Items absent** | **0** | **0** |
| Compiled artefacts | 0 | 0 |

Contents confirmed to be the *corrected* versions, not merely correctly named:

- `table_s1_regions.csv` — 0 HTT rows, 79 data rows
- `16_supplementary_tables.py` — `EXCLUDED_GENES` present (3 occurrences)
- `requirements.txt` — `torch` and `transformers` present, `fair-esm` absent
- `03_disorder_and_features.py` — no hardcoded external path
- `figures/paper/figure_1.png` — md5 `c2b48288c37b`, the regenerated figure
- audit records — md5 `1e6f79d0` / `82585f43`; `capture_tier_achieved: 1`; no
  `AIVS-VAR`; no "prospective"; 5 `superseded`
- `claude_code.py` — carries `_session_dir_name`
- `pyproject.toml` — version 0.2.2; README at v0.2.1 scope
- no Patterns-era manuscript at archive root

## Step 6 — NOT DONE

Both new records still carry `license: apgl-v3`. Editing metadata on a
published record requires an authenticated Zenodo API token; none is configured
on this host (no environment variable, no config file).

The only Zenodo token visible here is the one embedded in the GitHub webhook
URL. It was not used: mutating published records with a credential scraped from
a webhook configuration is not something to do unasked.

Two routes, author's choice:

1. Provide a Zenodo personal access token in the environment; all four records
   can then be corrected (the two new, and the two old if the API permits
   editing published versions).
2. Correct in the Zenodo web UI — Edit → license → `agpl-3.0` → Publish, on
   four records.

Cosmetic, not submission-blocking, but it is a visible metadata error on an
AGPL deposit in a paper about provenance quality.
