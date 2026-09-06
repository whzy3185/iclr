# GitHub Transport and Source-Commit Receipt

No change was made to `main` or the four canonical scientific documents.
Work is published on `codex/p0-task0-task1`. Direct Git push lacked credentials,
so the already-connected GitHub Git Data tools were used, without extracting
tokens or changing authentication settings.

The tools preserve file trees but create new commit metadata, hence new SHAs.
Each tree below was compared exactly before the corresponding commit was made.
The work was transported as separate commits, not a squashed evidence rewrite.

| Checkpoint | Original local commit | GitHub commit | Identical tree |
| --- | --- | --- | --- |
| TASK 0 | a66ab9d053d3b33e80f712f4955d4f3ab99839e0 | dd6fa472bbcdbec1223d65b31dceb169d1e41b8f | d4a9d4ae0699a8c4fdabf6e9f7aec78fa4e780ff |
| TASK 1 implementation | cff4e17ad815cb94a44d03d423cc6be535476fc6 | 36787de3233521c3825ec2641a0dcc54061dfbc6 | f2037fa9581b2bb8137ef0659857530adf432fa4 |
| TASK 1 result/status | b82f1e298a9d1303f34d50009129595572a302e8 | 026d4ec999a2ccf679558a8674b398355a02148f | ca202cd2bb448d4200f038c55e03ffc37cf55167 |
| TASK 2 partial | 2aae88fcf04fcf0436103c1c748a91d5b1e85bcc | d88227ece16206e9a309d9a98d64053ba6691fbc | 481086a0b912c26e8280afbd5e57bdf1af775b83 |

The retained mock trace truthfully refers to the original implementation commit
`cff4e17...`. It has not been relabeled to claim execution on a later remote
commit. To restore that exact source history, use the included bundle:

```sh
git bundle verify experiments/idea_collapse/tests/artifacts/source-history.bundle
git fetch experiments/idea_collapse/tests/artifacts/source-history.bundle refs/heads/codex/p0-task0-task1:refs/remotes/local-evidence/p0-checkpoint
git show cff4e17ad815cb94a44d03d423cc6be535476fc6:experiments/idea_collapse/generation/run.py
```

Bundle SHA256:
`a0a5fe72c14fb4502679be1ed7f4f82a47ca8137060b3905ba7e87ba162ffa8a`.
`git bundle verify` passed and reports a complete history with no prerequisites.
The bundle ends at the original TASK 2 partial checkpoint; this transport receipt
is a later administrative change, not a scientific run.

Raw annual-index HTML snapshots were preserved locally during acquisition;
their SHA256 hashes and source URLs are committed in `corpus/acquisition/`.
The normalized annual title indexes are committed in full. Neither these indexes
nor the mock corpus are a frozen pilot abstract corpus.

The publication uses GitHub tool operations `create_tree`, `create_blob`,
`create_commit`, and `create_branch`; it does not submit a paper, create a
research-lead decision, authorize model spending, or advance TASK 3/4.
