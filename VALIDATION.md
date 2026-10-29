# Validation

Recorded on 2026-10-29.

## Local verification (simulated semantics)

- 13 unit tests passed. These use mocked model results, not live consensus.
- Official linter: validation passed; 3 checks, 5 public methods (3 write, 2 view).
- Official pinned SDK Direct Mode: storage, calldata, terminal state and independent validator acceptance/rejection passed with a mocked LLM.
- Property checks: all 27 three-label equivalence combinations and source-preservation decisions.

## Real Stable Studionet evidence

Contract: `0x512F45FD4FE44D2A4a1D9DacEC96B18c5E2EcF10`. Chain 61999; RPC https://studio.genlayer.com/api.
Exact deployed source SHA-256: `8d58de464930ce1f3fcdb06812b80ed6018fbe61478f63e95eac05118cd7ab0e`.

4 distinct transactions completed with `FINALIZED`, `MAJORITY_AGREE`, `SUCCESS` and `leader_only=false`. No transaction was resent and no Appeal was requested. Zero-value development transactions; no cash purchase or funding.

| Step | Transaction hash |
| --- | --- |
| deploy | `0x9f1dff62789e9f757e77951cfbd4ef924594fa7ee7b8f6f490f567f57d4b6f43` |
| stage | `0x5b32b392aaa50e567a15c78ef1e76f9bd93b2244aff752f273a1e87112aec79e` |
| merge | `0xf9ccecbd0cf0da94612f3bbc1ac08b599023fd2fa234b254a86ce36ee1b6bf72` |
| publish | `0x0bf20a5d2c062fd2f6de6d117feba37c6ed69950dbafbe8bb30cdf96896fdefc` |

Final state: **PUBLISHED**.

The three-unit fixture selected left for retention, right for reply time, and exact base bytes for equivalent CSV/UTF-8 wording. The digest-bound result was published. These are synthetic supplied snapshots, not authenticated real-world branch authors.

[evidence/studionet.json](evidence/studionet.json) retains final records, transaction arguments, public receipt projections, consensus votes and leader receipt payloads. Node configuration, timing logs and redundant byte arrays are omitted. Public receipts establish actual network execution; they do not prove model correctness on all inputs.

## Boundaries of evidence

Only the clean recorded fixture was exercised on-chain. Ambiguous, conflict (where applicable), authorization and equivalence disagreement cases are covered locally, not claimed as live consensus tests. The read-only verifier checks code equality, exact receipt/call binding and finalized state; it sends no transactions. SDK compatibility may change after this date.
