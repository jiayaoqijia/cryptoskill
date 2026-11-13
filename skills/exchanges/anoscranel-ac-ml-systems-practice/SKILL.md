---
name: ac-ml-systems-practice
description: "The systems half of machine learning: pipeline hygiene and data validation before training, feature engineering without leakage, train-validation-test discipline and honest evaluation, model persistence and versioning, the train-serve skew class of bugs, champion-challenger deployment with canary and shadow, drift detection on inputs and predictions, and the written model record. It explains how ML pipelines and serving behave as engineering systems; it never tunes a model and never promises an accuracy. Use when asking \"ML pipeline\", \"feature leakage\", \"train serve skew\", \"model versioning\", \"canary a model\", \"shadow deployment\", \"champion challenger\", \"data drift\", \"concept drift\", \"prediction monitoring\", \"retraining trigger\", \"silent failure in prod\". Not for model architecture and mathematics (ac-prompt-engineer owns generation-model selection), not for vector retrieval and embeddings (ac-retrieval-and-vector-systems), not for backtesting trading strategies (ac-backtest-integrity)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# ML systems practice

## Overview

A machine-learning system is mostly pipeline, not model: data in, features computed, a model trained, artefacts versioned, predictions served, and reality drifting the whole time. Most production ML failures are not bad mathematics — they are leakage the evaluation never caught, skew between how features were computed at training time and at serving time, a silent dependency change, or a model that degraded slowly enough that nobody looked.

This skill covers that systems half: validation and hygiene at the pipeline boundary, leakage-proof feature and split discipline, honest evaluation before and after deployment, versioned artefacts, deployment patterns that compare a new model against a champion rather than replacing it blind, and the drift detection that tells you when the world has moved. The modelling itself — architecture, mathematics, tuning — is deliberately outside; the craft here is the engineering that makes any model trustworthy in production.

Primary sources: <https://developers.google.com/machine-learning/guides/rules-of-ml> and <https://ml-ops.org/>.

## When to use

- When building or operating the pipeline that feeds, trains, and serves a model.
- When evaluating a model honestly before deployment, or keeping it honest after.
- When deploying a new model against a champion without a blind cutover.
- When inputs, predictions, or performance drift and retraining must be triggered on evidence.

## When NOT to use

- For choosing and configuring generation models for agent use (use ac-prompt-engineer).
- For vector retrieval, embeddings, and reranking infrastructure (use ac-retrieval-and-vector-systems).
- For backtesting trading strategies and multiple-testing discipline there (use ac-backtest-integrity).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/pipeline-and-data-validation.md` | `software-engineering/pipeline-and-data-validation` | Hygiene at the pipeline boundary: what enters training must be checked, not assumed. |
| `subskills/features-and-leakage.md` | `software-engineering/features-and-leakage` | Building features that do not smuggle the answer or the future into training. |
| `subskills/splits-and-evaluation.md` | `software-engineering/splits-and-evaluation` | Splitting data so the evaluation predicts production, not the past. |
| `subskills/artefacts-and-versioning.md` | `software-engineering/artefacts-and-versioning` | Versioning models, features, and data so any prediction is reproducible. |
| `subskills/train-serve-skew.md` | `software-engineering/train-serve-skew` | The bug class where serving computes features differently than training did. |
| `subskills/champion-challenger-and-canary.md` | `software-engineering/champion-challenger-and-canary` | Deploying models into comparison, not into the void. |
| `subskills/drift-and-retraining.md` | `software-engineering/drift-and-retraining` | Detecting that the world moved, and retraining on evidence rather than calendar. |
| `subskills/ml-systems-record.md` | `software-engineering/ml-systems-record` | The written model record: versions, decisions, incidents, and triggers. |

## Status and honest limits

Every evaluation is a claim about a distribution, and production is under no obligation to stay in that distribution; a model can be honestly evaluated and silently wrong a month later. The monitoring here detects movement, not correctness — a prediction can be confidently drifting. Nothing here tunes a model or promises an accuracy figure, and the biggest failure class of all, a model deployed against a problem nobody framed, is upstream of every leaf in this skill.
