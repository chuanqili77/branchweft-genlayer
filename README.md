# BranchWeft

A reusable GenLayer semantic three-way merge primitive for small, fixed-unit text documents. Given base, left and right snapshots, it detects unilateral changes, equivalent edits and unresolved concurrent edits. Accepted output consists exclusively of exact source text selected by deterministic code. Useful for merging short notices or configuration descriptions without introducing generated wording.

## Mechanism

For each unit, the leader classifies base/left, base/right and left/right as EQ, CHANGE or UNKNOWN. EQ means equivalent obligations and factual meaning; changes to quantities, exceptions, deadlines, scope, permissions or requirements count as CHANGE. Validators independently classify all original pairs and require the **entire label vector** to agree. Explanatory wording may vary. This tests semantic agreement, not merely response format.

| Pair labels (base/left, base/right, left/right) | Selection |
| --- | --- |
| EQ, EQ, EQ | base |
| CHANGE, EQ, CHANGE | left |
| EQ, CHANGE, CHANGE | right |
| CHANGE, CHANGE, EQ | left (canonical existing wording) |
| CHANGE, CHANGE, CHANGE | CONFLICT |
| Any UNKNOWN, or exactly two EQ labels | REVIEW |

Exactly two EQ labels violate equivalence transitivity and cannot produce an automatic merge. Identical strings must be classified EQ. CONFLICT dominates REVIEW at document level. Blocked documents expose per-unit findings but no merged text; clean documents concatenate chosen source bytes with blank lines. There is no LLM-authored merge output.

## State and API

`STAGED → MERGED → PUBLISHED`, or `STAGED → REVIEW | CONFLICT`. Caller and document ID define the immutable namespace. Only the owner can merge or publish. Publish requires the exact result digest and recomputes selection before marking the result published. The digest binds protocol, owner, ID, all snapshots, assessment and result. Publication preserves the original MERGED result inside the outer PUBLISHED record.

| Method | Arguments | Result |
| --- | --- | --- |
| `stage` | doc_id, payload | Store immutable snapshots |
| `merge` | owner, doc_id | Consensus assessment and deterministic result JSON |
| `publish` | owner, doc_id, result_digest | Owner confirms clean, digest-bound result |
| `get_document` | owner, doc_id | JSON snapshot |
| `get_protocol` | none | `branchweft-1` |

Payload is a JSON array of 2–5 objects with exactly `id`, `base`, `left`, `right`; consecutive IDs U1, U2, etc. Each text is 16–700 characters; total JSON 80–11000 characters. Document ID is 1–40 alphanumeric/underscore/hyphen. See [examples/document.json](examples/document.json).

With `genlayer-js`, stage via `client.writeContract({address, functionName:'stage', args:[id, JSON.stringify(units)], value:0n, leaderOnly:false})`, then invoke `merge` as the same owner. Read `get_document` with `TransactionHashVariant.LATEST_FINAL`; if MERGED, pass its `result_digest` to `publish`. The verification script is a complete minimal calling example. No frontend is included.

## Scope and limitations

Snapshots are supplied by one owner; this is not independent branch-author authentication or a Git integration. Fixed independent units only: no additions, deletions, reordering or cross-unit consistency proof. Models may mistake meaning or follow malicious text despite the defensive prompt and independent check. Equality is a bounded semantic judgment, not a mathematical or legal guarantee. Conflicts and uncertainty stop automation; resolve off-chain and stage a fresh document. No edit, cancellation, appeal, payments or automatic external publication.

## Originality and reuse

The accessible repository review covered chuanqili77, chongqianli7, zuotu295, gqzy999, zsf11221 and accessible public gqzy1/halihalibt repositories. Existing work included amendment acknowledgement, bilateral clause matrices, compression checks, dependency graphs and evidence aggregation. This primitive instead checks a three-snapshot equivalence triangle and selects immutable source bytes under explicit merge rules. The review is bounded and does not establish worldwide novelty.

## Development and verification

```sh
npm ci
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
genvm-lint check contracts/branch_weft.py
python scripts/prepare-sdk.py
python sdk-tests/check_sdk.py
node scripts/read-live.mjs
```

The unit tests use a small SDK shim and mocked semantic responses. The Direct Mode test uses the official pinned SDK, storage and calldata with a mocked LLM, including independent validator acceptance and rejection. Neither is network consensus. `read-live.mjs` performs only reads: chain ID, deployed source, exact transaction method/arguments/signer/target, full-consensus flags, finalized receipts and final state.

`verify-live.mjs` is an **opt-in write tool**, not a routine test command. `NEW_TEST=1 node scripts/verify-live.mjs` creates disposable development wallets and performs the documented zero-value workflow. It persists private state outside the repository, records intent before sending and resumes existing hashes. Never delete that state to retry a pending or failed transaction. Inspect failures first; it does not Appeal. Do not run it to reproduce evidence already recorded here. Never fund these disposable wallets or use them for valuable assets.

## Network and compatibility

Only Stable Studionet, chain **61999**, RPC **https://studio.genlayer.com/api**. Official [network documentation](https://docs.genlayer.com/developers/intelligent-contracts/networks) and the installed `genlayer-js` Studionet preset were checked before deployment; the RPC returned `0xf22f`. Dependencies are pinned in the lockfiles. The source pins `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`; the official linter suggests a newer runner, so the declared pin is intentionally retained and compatibility is established by the recorded live execution. This is not a claim of compatibility with other networks or future SDK releases.

See [VALIDATION.md](VALIDATION.md), [deployment.json](deployment.json), the generated [schema](schema.json) and [public evidence](evidence/studionet.json). MIT licensed.
