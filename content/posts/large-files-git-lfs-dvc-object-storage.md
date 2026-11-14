---
title: "Git LFS, DVC or Object Storage: Where to Keep Large Vision Files"
description: "Images, videos and model weights do not belong in plain Git. How Git LFS, DVC and object storage with a manifest compare, and how to choose for your team."
category: "Tools and Workflow"
date: 2026-12-09
tags: [git-lfs, dvc, storage, datasets, workflow]
---

Every computer vision repository eventually meets the same problem. Someone commits a folder of training images or a 200 MB weights file, the repository becomes slow to clone, and history grows forever because Git keeps every version of every file. Removing them later means rewriting history.

Large files need somewhere else to live, with a link from the code to the exact version used. This article compares the three common approaches, Git LFS, DVC and plain object storage with a manifest, and suggests how to choose.

![A decision tree. The first question is what the file is. A few files that belong with the code, such as weights and golden outputs, lead to Git LFS, which versions files with the commit but is limited by the provider's quota. A dataset of thousands of versioned images with splits leads to a second question: do you need pipelines and reproducible stages? Yes leads to DVC, which handles dataset versions, splits and a stage graph. No leads to object storage with a manifest, which is cheapest at scale but means writing the glue yourself. A note says most teams end up using Git LFS for weights and one of the other two for footage.](img:large-files-git-lfs-dvc-object-storage-decision-tree.png "The three options answer different questions, which is why most repositories end up using two of them.")

The mistake worth avoiding is treating this as one choice. A repository holding both a 200 MB weights file and 80,000 training images has two different problems, and the answer for one is the wrong answer for the other.

## What you need from any approach

- **Exact versions.** A commit of the code should identify the exact data and model files it used.
- **Reasonable clone and checkout.** Developers should not download every dataset to change one line of code.
- **Shared access** for the team and for training machines.
- **Cost control.** Storage and download costs grow with every dataset version.
- **Access control,** because footage of people is sensitive data. See [Privacy and Ethics in Camera Analytics](post:privacy-and-ethics-camera-analytics).

## Git LFS

Git Large File Storage replaces large files in the repository with small pointer files, and stores the real content on an LFS server. When you check out a commit, the matching file versions are downloaded.

**Good for:** model weights, a modest number of test images or golden outputs, sample clips used by tests. Files that change occasionally and belong with the code.

**Watch out for:**

- Hosting providers impose storage and bandwidth quotas on LFS, and charge beyond them. A dataset of tens of thousands of images, versioned several times, uses those quickly. Check your provider's current terms.
- Every clone with LFS enabled downloads the LFS files for the checked-out commit, unless configured otherwise.
- It versions files, not datasets. There is no built-in notion of splits, pipelines or which files belong together beyond the commit.
- Rewriting history to move existing large files into LFS is possible but disruptive for everyone with a clone.

## DVC

DVC (Data Version Control) also stores small pointer files in Git, but keeps the data in a storage "remote" you choose: S3-compatible object storage, Google Cloud Storage, Azure, a network drive, an SSH server and others. It tracks whole directories with content hashes and can describe pipelines (data preparation, training, evaluation) whose outputs are cached.

**Good for:** datasets of any size, versioned alongside code, where you want to reproduce "dataset version X with code commit Y" exactly, and you already have or can create a storage bucket.

**Watch out for:**

- Another tool to learn, install on every machine and keep consistent.
- Large directories of small files, such as image datasets, take time to hash and transfer; plan for it.
- The storage remote is yours to secure, back up and pay for.
- Its pipeline features are optional; many teams use only the data versioning part.

## Object storage with a manifest

The lightest approach: store images and videos in a bucket or on a shared drive, in a layout where files are only ever added, never changed in place, and keep a manifest file in Git listing every file in each dataset version with its hash, split and metadata.

```
path,sha256,split,camera,recorded
cam03/2026-10-01/000123.jpg,9f2c...,train,cam03,2026-10-01
```

Training scripts read the manifest, download or mount the listed files, and check hashes. A dataset version is simply a manifest version.

**Good for:** teams that want full control and minimal tooling, very large datasets, and setups where data already lives in object storage. It is also easy for a client to take over at handover, since it needs nothing beyond storage and Git. See [Versioning Datasets and Models Together](post:versioning-datasets-and-models).

**Watch out for:**

- You write the small amount of tooling yourself: manifest creation, hash checks, download.
- Discipline is required: never overwrite a file in place.

## Comparison

| | Git LFS | DVC | Object storage + manifest |
|---|---|---|---|
| Setup | Minimal | A tool and a remote | Storage plus small scripts |
| Best for | Weights, test assets | Datasets with pipelines | Large datasets, simple control |
| Where data lives | Git host's LFS storage | Your chosen remote | Your bucket or drive |
| Cost model | Host's LFS quotas | Your storage costs | Your storage costs |
| Dataset concept | Per file, per commit | Directories and pipelines | Manifest you define |
| Handover | Needs LFS access | Needs DVC and the remote | Needs the bucket and Git |

## A combination that works

Many teams end up using two of them:

- **Git LFS** for things that belong with the code and are small enough: golden test images, short test clips, perhaps the current production weights.
- **DVC or a manifest** for datasets and training outputs, stored in object storage the team controls.

Model weights for released versions often go to a model registry or a dedicated folder in object storage, referenced by version and hash from the deployment configuration. See [Updating Models on Edge Devices Without Bricking Them](post:updating-models-on-edge-devices).

## Practical tips

- **Add a `.gitignore` early** for common data folders and file types (`*.mp4`, `*.pt`, `runs/`, `datasets/`), so accidents do not happen.
- **Add a size check** in a pre-commit hook or CI that rejects files above a limit.
- **Keep raw footage separate** from curated datasets. Raw recordings are large and sensitive; datasets are subsets with labels.
- **Apply retention.** Old dataset versions and raw footage should be deleted when no longer needed, according to your data policy. Content-addressed storage makes it easy to keep things forever by accident.
- **Restrict access** to buckets and remotes with footage, and log who accesses them.
- **Document it** in the repository: where data lives, how to get access, how to fetch a dataset version. See [Handover Documentation for a Computer Vision System](post:handover-documentation-for-cv-systems).

## Checklist

- No large binaries in plain Git; ignore rules and size checks in place.
- Every training run traceable to an exact data version.
- Git LFS for small, code-adjacent assets; DVC or a manifest for datasets.
- Storage you control for footage, with access control and retention.
- Files added, never overwritten, in data storage.
- The setup documented for new team members and handover.

Next steps: [Reproducible Training Runs](post:reproducible-training-runs) and [Experiment Tracking: TensorBoard, Weights & Biases and MLflow](post:experiment-tracking-tensorboard-wandb-mlflow).
