# Public-release readiness audit v1

Audited main: `203d9795e2b442ac8af90652eb95de58d3e6bdb5`. Repository remains **PRIVATE**. This is a non-normative assessment, not publication authorization or a new product contract.

**PUBLIC_RELEASE_AUDIT_READY_FOR_RELEASE_PREP** means the audited surfaces contain no identified security/privacy/provenance or runtime-install blocker. Owner decisions and concrete release preparation remain. Do not make the repository public on the strength of this report alone.

## What would be exposed

The current main has 42 files: 5 root files, 5 source files, 12 test/support/fixture files, 15 docs, 1 contract, 2 examples/data files, 1 workflow and 1 summary tool. All tracked entries are regular non-executable files; no symlinks, submodules or LFS pointers. Source distribution artifacts built during this audit remain outside the repository and are not automatically published by a visibility change.

Public repository exposure includes historical versions, retained remote branches, commit identities, existing discussions and accessible workflow outputs. The scan covered 14 reachable commits and all 54 blobs from all normal refs after fetching every remote head/tag, including 12 blob versions absent from current main. No files have a historical-only path; older versions of current paths are still exposure surfaces.

Configured known key-format, generic credential, path, identity and private-data patterns were scanned, with practical entropy checks and manual context review. No actual credentials, private source payloads, real-market/competition datasets or unsafe historical/remote-branch blobs were found. Twenty content-pattern hits were reviewed: fifteen generic origin-market labels and five high-level historical process/exclusion references. These are not leaked data; process wording needs release-document cleanup. Known digest-shaped synthetic values were treated as context-reviewed expected values, not credentials.

## Publication safety matrix

| Surface | Audited result | Public-safe assessment |
| --- | --- | --- |
| Current main tree | 42 tracked files; all scanned | CONTENT_SAFE_WITH_RELEASE_PREP |
| Git history | 14 reachable commits, 54 blobs, 12 historical-only versions | NO_UNSAFE_CONTENT_FOUND |
| Remote branches | 6 heads; all reachable branch-only versions scanned | NO_UNSAFE_CONTENT_FOUND |
| Tags/releases | 0 local tags, 0 remote tags, 0 GitHub Releases | NO_EXPOSURE_PRESENT |
| Commit identities | 3 author/committer identity groups; real-name/non-noreply exposure retained | OWNER_REVIEW_REQUIRED |
| PR/issues/comments | 5 PRs; no standalone issues, comments or reviews | PUBLIC_SAFE |
| Workflow config | contents:read, hosted runners, credential persistence off | PUBLIC_SAFE |
| Workflow outputs | 13 accessible runs / 20 logs; 0 artifacts | PUBLIC_SAFE_WITH_RECORDED_LIMITS |
| Repository configuration | read defaults verified; protection/rulesets HTTP403 | OWNER_CONFIGURATION_REVIEW_REQUIRED |
| Dependencies | stdlib runtime; local dev/build metadata inspected | NO_KNOWN_METADATA_CONCERN_WITH_LIMITS |
| License status | no LICENSE or license metadata/grant | OWNER_DECISION_REQUIRED |
| Package metadata | internally consistent private dev package, 0.0.0.dev0 | RELEASE_PREPARATION_REQUIRED |
| Wheel/sdist | 9-file wheel / 22-file sdist; normal artifact install passes; sdist test assets incomplete | RELEASE_PREPARATION_REQUIRED |
| Examples/fixtures | 116 synthetic goldens and 3 synthetic observations | PUBLIC_SAFE |
| English README | navigation, instructions, limitations valid; private state accurate now | RELEASE_STATE_UPDATE_REQUIRED |
| Chinese README | faithful navigation/claims, no unsupported promises | RELEASE_STATE_UPDATE_REQUIRED |
| Docs | 17 classified documents; historical scaffold/process contradictions recorded | RELEASE_PREPARATION_REQUIRED |
| Fresh clone | exact main; fresh Python3.12.10 environment | PASS |
| Install | editable dev, noneditable, wheel and sdist outside-source imports | PASS |
| Tests | 392 collected, 385 passed, 7 explicit Windows capability/concept skips | PASS |
| Demo | human output and repeated 374-byte JSON match tracked receipt | PASS |

## Remote refs and history

| Branch | Head | Ahead / behind main | Unique reachable blobs | Result |
| --- | --- | --- | --- | --- |
| demo/minimal-asof-v1 | 1c4196ca5629de5c254ee11c2023b4e112182313 | 0 / 2 | 0 | NO_UNSAFE_CONTENT_FOUND |
| docs/chinese-readme | 869ebd3d6dcbf7a72d9d050a46f6ec72dc0f11f5 | 3 / 1 | 3 | NO_UNSAFE_CONTENT_FOUND |
| impl/minimal-primitives-v1 | 2bd167b1cd510acdf9dd8fbdb0f9e4a200770987 | 0 / 6 | 0 | NO_UNSAFE_CONTENT_FOUND |
| main | 203d9795e2b442ac8af90652eb95de58d3e6bdb5 | 0 / 0 | 0 | NO_UNSAFE_CONTENT_FOUND |
| spec/minimal-primitive-semantics-v1 | fca3e26207cb7ab3920e685ab565a64363c24163 | 2 / 8 | 11 | NO_UNSAFE_CONTENT_FOUND |
| test/cross-platform-conformance-v1 | 7b55b91af0f779d40bfc0610b6f0300d165a4903 | 0 / 4 | 0 | NO_UNSAFE_CONTENT_FOUND |

Some retained feature branches have unique commits because integration did not preserve identical commit ancestry. The unique blobs were scanned, including obsolete README/specification versions; a merged PR was never used as a substitute for content review. No remote branch is classified unsafe. There are no local tags, remote tags or GitHub Releases. No refs were deleted or rewritten.

Commit author/committer metadata contains three distinct identity groups: two use GitHub noreply addresses; one uses a non-noreply address. Two groups also require display-name/identity review. Names and email values are intentionally omitted here. Classification is **OWNER_REVIEW_REQUIRED**, not a credential leak. Owner acceptance or a separately authorized remediation plan is required before public exposure. Public GitHub handles and known public tool attribution are not automatically privacy blockers.

## GitHub collaboration and Actions

PRs #1 through #5 were reviewed in full current title/body form and classified PUBLIC_SAFE. There are no standalone issues, issue comments, review submissions or review comments, and no private attachments were found. Existing same-repository CI links are expected publication surfaces.

All 13 accessible workflow runs and 20 job logs were inspected: 430,784 UTF-8 bytes / 4,792 lines, with no artifacts. The 166 path-pattern matches belong to ephemeral hosted runners, and twenty repeated URL matches are a public platform changelog. Raw logs, owner paths and sensitive matched text are not included in this report.

The workflow uses `contents: read`, hosted Windows/Ubuntu Python3.12, and checkout credential persistence disabled. No provider/DB calls, self-hosted assumptions, embedded secrets, artifact upload or publishing step was found. Repository workflow defaults are read-only and cannot approve PR reviews. Auto-merge is disabled; merge, squash and rebase methods are enabled. Actions allow all actions and do not require SHA pinning; review maintained versions/pinning as governance work. Logs carry action-runtime deprecation notices but all inspected jobs succeeded.

Branch-protection and ruleset API reads returned HTTP403. Their status is **UNVERIFIED**, not absent. Deleted/inaccessible server-side history, edited discussion versions and removed logs cannot be certified by this accessible-surface audit.

## Provenance and synthetic data

**NO EVIDENCE OF PRIVATE SOURCE COPY IN AUDITED REPOSITORY.** There is one independently rooted repository history. All five runtime modules, source comments, test/example Python content, synthetic fixtures and generated package files were reviewed. No copied-license headers or private implementation details were identified. This is evidence bounded to this repository, not legal proof or a comparison against the private origin implementation.

The 116 golden vectors and three demo observations are synthetic. No real security identifiers, provider payloads, financial statements, proprietary market data, competition submissions or private qualification evidence were found. BAquant implementation source reads, Git operations and mutations are each zero.

## License and Owner decisions

No LICENSE/LICENSE.txt/COPYING or pyproject license field exists. No redistribution/open-source grant has been made. This is a required licensing decision, not a secret/security finding.

| Candidate | Reuse and attribution | Patent language | Owner-review suitability |
| --- | --- | --- | --- |
| MIT | Permissive; retain copyright and permission notices in copies or substantial portions. | No express patent grant in the text. | Short terms for a reusable library if that tradeoff is acceptable. |
| Apache-2.0 | Permissive; include license, mark modifications, preserve applicable notices and NOTICE attribution. | Explicit contributor grant for covered patent claims, with a litigation termination condition. | Useful to consider for reusable infrastructure when explicit patent terms matter. |

References: [MIT text](https://opensource.org/license/mit) and [Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0). **RECOMMENDED_FOR_OWNER_REVIEW: Apache-2.0**; final license choice and ownership confirmation remain **OWNER_DECISION_REQUIRED**. This comparison does not select or apply a license and is not legal advice.

Additional Owner decisions: accept reachable identity exposure; select a first version strategy such as 0.1.0rc1 or 0.1.0 and compatibility commitments; choose repository/wheel/sdist publication scope; verify protection/rulesets with appropriate access. No decision is presumed made.

## Package, dependencies and installation

Package `baquant-pit`, version `0.0.0.dev0`, Python `>=3.12`, setuptools.build_meta with `setuptools>=77`, src package discovery, README.md metadata. Runtime dependencies are empty; dev dependencies are `pytest>=8,<10` and `ruff>=0.15,<1`. No author/maintainer/license/project-URL metadata is declared and no local/private/file/git dependency was found. Classifiers still include planning and `Private :: Do Not Upload`. Public API compatibility remains NOT_ESTABLISHED and BAquant compatibility NOT_CLAIMED. Python3.12 is verified; 3.13/3.14 are not inferred as tested.

Available installed license metadata:

| Tool/dependency | Observed version | Available license metadata |
| --- | --- | --- |
| pytest | 9.1.1 | MIT |
| ruff | 0.16.10 | MIT |
| iniconfig | 2.3.1 | MIT |
| packaging | 26.3 | Apache-2.0 OR BSD-2-Clause |
| pluggy | 1.6.0 | MIT |
| Pygments | 2.21.0 | BSD-2-Clause |
| colorama | 0.4.6 | License :: OSI Approved :: BSD License |
| pip | 25.0.1 | MIT |
| setuptools | 84.0.0 | MIT |

Dev/build tools are not vendored into the product wheel. These observations do not establish comprehensive transitive/vendored licensing compatibility. Missing metadata would be LICENSE_METADATA_UNVERIFIED rather than presumed incompatible; local declared-tool metadata was available.

A fresh non-local clone at the exact audited SHA used newly created Python3.12.10 environments without system-site packages. Documented editable dev installation, Ruff check, format, full pytest and diff check passed: **392 collected / 385 passed / 7 explicit existing skips / 0 failures**. The skips are two conceptual conformance vectors, unavailable native FIFO and four unavailable local native symlink cases. All application validation is independent of private origin repositories, services and secrets.

Human demo and repeated JSON passed; the JSON is exactly the tracked receipt's 374 UTF-8 bytes, including outside-clone working-directory execution. Normal noneditable installation, wheel installation and direct sdist installation import from environment site-packages outside the repository with exactly twelve public names and version 0.0.0.dev0.

## Build and distribution contents

Local/offline wheel and sdist builds succeeded using the declared backend already acquired by the documented installation, with no extra build-tool dependency installed merely for this audit. Archives were fully inventoried and scanned. There were no embedded absolute paths, secrets, private task logs, private source or competition payloads. Archive-byte reproducibility was not claimed.

- Wheel: `baquant_pit-0.0.0.dev0-py3-none-any.whl`, 9 files: five runtime modules plus METADATA, WHEEL, top_level.txt and RECORD. No tests, examples or private planning documents are bundled; README content is embedded in metadata.
- Sdist: `baquant_pit-0.0.0.dev0.tar.gz`, 22 files including eight test modules, package sources, English README and generated build metadata. It omits test support/golden fixtures/contracts/docs/examples/Chinese README, so it does not reproduce the repository test/demo workflow. Runtime installation from it succeeds. A clone-free collection of all eight bundled test modules confirms six collection errors: four missing test-helper imports, one missing demo script and one missing contract; the complete Git-clone suite passes.

Before artifact release, intentionally define the source manifest and distribution documentation: include coherent tests/assets or omit tests deliberately, and make repository-only demo/test requirements clear. Resolve relative language/doc links for package metadata. This is a **release-preparation gap**, not a failed normal install or leaked content. Full member lists and content digests are in the companion JSON.

## Documentation disposition

Both READMEs have accurate current private status, faithful bilingual navigation, valid commands, market-neutral scope and explicit limitations. All 26 README relative-link occurrences (13 targets), and all 30 repository-relative Markdown link occurrences in the audited pre-existing docs, resolve. No production/API/scientific acceptance claim is established by passing tests.

| Document | Classification | Before release | Priority |
| --- | --- | --- | --- |
| README.md | PUBLIC_PRODUCT_DOC | rewrite: Purpose, market neutrality, exclusions and commands agree with the implementation; synchronize PRIVATE/no-license/version text with separately authorized release decisions and replace links to obsolete planning material. | REQUIRED |
| README.zh-CN.md | PUBLIC_PRODUCT_DOC | rewrite: Faithful bilingual counterpart; apply the same later release-status and navigation changes as English. | REQUIRED |
| docs/ARCHITECTURE.md | PUBLICATION_REVIEW_REQUIRED | rewrite: Still states an empty package and design-only runtime. Describe implemented primitives separately from prospective architecture and remove origin-project process vocabulary from product guidance. | REQUIRED |
| docs/BAQUANT-PIT-PUBLIC-EXTRACTION-PLAN-V1.md | INTERNAL_PROCESS_DOC | move: Historical bootstrap/extraction task sequence is not current product documentation. Move to clearly labelled historical planning or external planning evidence and unlink from the product landing page. Moving cannot remove the existing Git-history exposure; no sensitive payload was found here. | REQUIRED |
| docs/ORIGIN_AND_AUTHORITY.md | PUBLIC_PROVENANCE_DOC | rewrite: Retain bounded independent-origin and compatibility statements; update private-release authorization wording when decisions are made. Origin market suffixes are contextual scope documentation, not market data or a support claim. | REQUIRED |
| docs/PUBLIC_PRIVATE_BOUNDARY.md | PUBLICATION_REVIEW_REQUIRED | rewrite: Preserve generic inclusion/exclusion and content-identity limits; replace obsolete empty-scaffold and private extraction-process statements with actual library scope. | REQUIRED |
| docs/PUBLIC_RELEASE_AUDIT_CHECKLIST.md | INTERNAL_PROCESS_DOC | rewrite: Convert bootstrap-only, unexecuted future-gate wording into an explicitly historical or reusable engineering checklist with a link to the current scoped audit. A completed audit does not authorize publication. | REQUIRED |
| docs/demos/minimal-asof-demo-v1.md | PUBLIC_PRODUCT_DOC | rewrite: Synthetic timeline, inclusive cutoff, tie failure, limitations and fixed output are accurate. Only release-state wording needs later synchronization. | REQUIRED |
| docs/implementation/cross-platform-conformance-v1.json | PUBLIC_ENGINEERING_DOC | remain: Non-normative, versioned conformance design records scope rather than ephemeral success. Preserve as historical technical evidence. | NO_ACTION |
| docs/implementation/cross-platform-conformance-v1.md | PUBLIC_ENGINEERING_DOC | rewrite: Accurately bounds Python 3.12 Windows/Linux validation and conditional filesystem cases; synchronize present-tense private/no-license status in a later release task. | REQUIRED |
| docs/implementation/golden-runtime-coverage-v1.json | PUBLIC_ENGINEERING_DOC | remain: All 116 coverage records are generic synthetic-vector accounting. Its candidate status belongs to a historical receipt, not an independent publication grant. | NO_ACTION |
| docs/implementation/minimal-asof-demo-v1.json | PUBLIC_ENGINEERING_DOC | remain: Synthetic, non-normative reproducibility receipt with fixed five-cutoff expectations and digests; no host paths or live identifiers. | NO_ACTION |
| docs/implementation/minimal-primitives-v1.md | PUBLIC_ENGINEERING_DOC | rewrite: Keep API/error/resource and historical conformance information; label original 336-test/329-pass counts as historical and synchronize current release-state wording. | REQUIRED |
| docs/specs/canonicalization-v1.md | PUBLIC_ENGINEERING_DOC | remain: Preserve frozen normative v1 text/semantics. Add a separate current-status guide explaining design-time private/pre-implementation statements before public presentation. | REQUIRED |
| docs/specs/compatibility-and-versioning-v1.md | PUBLIC_ENGINEERING_DOC | remain: Preserve frozen format/version and compatibility rules. Explain design-time deferred-runtime statements through separate current-status context rather than silently editing v1. | REQUIRED |
| docs/specs/raw-integrity-v1.md | PUBLIC_ENGINEERING_DOC | remain: Preserve frozen raw/file semantics. Separate current-status context must explain its historical no-runtime-API wording. | REQUIRED |
| docs/specs/temporal-semantics-v1.md | PUBLIC_ENGINEERING_DOC | remain: Preserve frozen temporal semantics. Separate current-status context must explain its historical no-runtime-primitive wording. | REQUIRED |

Frozen specs/contracts/goldens must not be silently rewritten to make their old design-time wording current. Add separate reviewed release-state/authority context. Historical process material can be moved or labelled later, but relocation does not erase its Git history.

## Required release preparation and optional improvements

Required work, in a separately authorized task: resolve license/identity/version/distribution decisions; synchronize current private/no-license/development wording and package classifiers; replace obsolete empty-scaffold descriptions; label or move historical planning and update navigation; explain frozen design-time authority; resolve the sdist manifest and package-relative link gaps. None was fixed during this audit.

Recommended community files are SECURITY, CONTRIBUTING and CHANGELOG; CODE_OF_CONDUCT and CITATION are optional. The package metadata and bilingual READMEs already exist. The lack of these optional/community files is not a security blocker. Also consider action maintenance/pinning, governance access, broader tested Python versions and a deliberate tool-version/reproducibility policy. PyPI publication is optional and separately authorized.

## Outcome and retained boundaries

Security/privacy blockers: **none found within the audited scope**. Provenance blockers: **none evidenced**. Packaging/runtime installation blockers: **none**. Owner licensing/identity decisions and release-preparation gaps remain explicitly open.

**PUBLIC_RELEASE_AUDIT_READY_FOR_RELEASE_PREP**. This is readiness to plan the required preparation, not approval to publish. Final Windows/Ubuntu CI on the audit PR head is required after this snapshot is committed; its observed result belongs in the PR/task evidence. The existing workflow is unchanged.

Only this sanitized report and its JSON companion are added. Repository visibility, product source, tests, examples, contracts, frozen specifications, receipts, version, license and workflows are unchanged. No merge, tag, release, PyPI publication, history rewrite, force push, branch deletion, secret revocation or private-origin access occurred.
