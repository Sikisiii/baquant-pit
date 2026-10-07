# Public release audit checklist

Future gate only. This checklist is unexecuted for public release and grants no
rights. The bootstrap privacy scan has a smaller scope and does not constitute
public package acceptance. Record review scope, exact commit, evidence, reviewer,
exceptions and disposition outside distributable material where appropriate.

## Content and history

- [ ] Review the entire current working tree, including ignored/untracked files
      that could enter a distribution or generated artifact.
- [ ] Review the entire Git history: every commit, branch, tag, blob and commit
      metadata; confirm no private source history or prohibited copies.
- [ ] Check tokens, passwords, webhooks, cookies, DSNs and provider credentials.
- [ ] Check private URLs, private hostnames, local absolute paths, user names,
      author metadata and user/personal data.
- [ ] Check database dumps, backup files, archive images and production snapshots.
- [ ] Check licensed data and provider response payloads, even when stripped of
      credentials; establish independently redistributable rights.
- [ ] Check copyrighted research, paid reports and third-party text/code rights.
- [ ] Check competition content and Golden Case.
- [ ] Check alpha/factor/strategy details, strategy members and portfolio details.
- [ ] Check private snapshot IDs, run/evidence identifiers and private run artifacts.
- [ ] Check proprietary prompts and BAquant operational configuration.

## Package and generated surface

- [ ] Review package metadata, built wheel/sdist contents and exported public API.
- [ ] Review dependency licenses, provenance and all redistribution obligations;
      separately approve a package license. None is granted during staging.
- [ ] Review README examples and minimal demos.
- [ ] Review test fixtures; prefer newly authored synthetic evidence.
- [ ] Review notebook outputs, generated artifacts and screenshots.
- [ ] Review GitHub Actions logs/artifacts, caches and other hosted outputs if relevant.
- [ ] Confirm no private DB, Provider, BAquant runtime or secret dependency.
- [ ] Validate temporal semantics, fail-closed behavior and deterministic tests;
      keep identity/applicability/consumer qualification uncertainty explicit.

## Authorization gates

- [ ] Record independent audit findings and close blocking findings.
- [ ] Obtain explicit Owner authorization for any private-to-public visibility change.
- [ ] Obtain explicit Owner authorization for any release/version and publication.

**PUBLIC RELEASE AUDIT PASS does not itself authorize public release.** Owner
authorization remains required. No public visibility, release, PyPI publication
or open-source license is authorized by bootstrap tests or this checklist.
