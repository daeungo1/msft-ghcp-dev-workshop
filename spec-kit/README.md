---
title: TeamFeed Spec Kit Components
description: Local extension, workflow, and bundle sources for the TeamFeed v0.2 workshop
ms.date: 2026-11-02
ms.topic: reference
---

# TeamFeed Spec Kit Components

These component sources target Spec Kit 1.2.5 or later.

## Components

* `extensions/teamfeed-quality` provides `/speckit-teamfeed-quality-verify`
* `workflows/teamfeed-delivery` runs the SDD cycle with human approval gates
* `bundles/teamfeed-multi-harness` pins the approved extension and workflow
  versions

## Local installation

Review every manifest and shell instruction before installation. From the
repository root, install the payloads first:

```bash
specify extension add ./spec-kit/extensions/teamfeed-quality --dev
specify workflow add ./spec-kit/workflows/teamfeed-delivery --dev
```

The bundle is a composition record. Install the local payloads first so the
bundle can confirm and pin the already present component versions without
network access.

```bash
specify bundle install ./spec-kit/bundles/teamfeed-multi-harness --offline
```

Run the workflow with:

```bash
specify workflow run ./spec-kit/workflows/teamfeed-delivery \
  --input spec="Describe the TeamFeed capability"
```

The workflow uses the project's initialized integration. It does not require a
specific model.
