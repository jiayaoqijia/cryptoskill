---
name: ac-geospatial-data
description: "Storing and querying data that lives on a map: coordinate reference systems and the disaster of mixing them, spatial indexes from R-tree to geohash and what each is for, nearest-neighbour and radius queries, bounding boxes as the cheap filter and where they mislead, distance computation over a sphere, polygons and containment, and the written geospatial record. It explains how spatial storage and queries behave; it never recommends a spatial database and never promises a query time. Use when asking \"spatial index\", \"geohash\", \"R-tree\", \"nearest neighbour query\", \"radius search\", \"bounding box\", \"coordinate system\", \"WGS 84\", \"latitude longitude storage\", \"point in polygon\", \"haversine\", \"postgis\", \"why is my distance query slow\", \"GeoJSON\". Not for general database indexing and partitioning (ac-query-and-index-design, ac-database-engine-internals), not for general analytical data modelling and dimensions (ac-analytical-data-modeling), not for map rendering and visual design (ac-dataviz)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Geospatial data

## Overview

Location breaks the assumptions ordinary indexes rely on. A b-tree orders one dimension; the world has two (or three), and the orderings interfere — points that are neighbours in space can be far apart in any single ordering, so a spatial index is a structure that keeps spatially-close things findable: trees of overlapping rectangles, or encodings that interleave latitude and longitude bits so nearby places share a prefix.

The second axis of difficulty is that coordinates are measurements against a reference system, and the reference systems do not agree with each other. Most of the world's data states WGS 84, but local systems, projected grids, and different ellipsoids exist; storing a number without its reference is storing a mystery. This skill covers the storage layer: reference systems, the index structures and their trade-offs, the query families from nearest-neighbour to containment, and the arithmetic of distance on a sphere.

Primary sources: <https://postgis.net/documentation/> and <https://www.rfc-editor.org/rfc/rfc7946>.

## When to use

- Designing storage and indexes for location data.
- Building proximity, radius, nearest-neighbour, or containment queries.
- Handling coordinate reference systems across data sources.
- Diagnosing slow spatial queries or wrong-looking distances.

## When NOT to use

- For non-spatial database indexing and partitioning (use ac-query-and-index-design).
- For analytical star schemas and dimension design (use ac-analytical-data-modeling).
- For the visual design of maps and charts (use ac-dataviz).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/coordinate-reference-systems.md` | `software-engineering/coordinate-reference-systems` | Datums, projections, and the cost of mixing them. |
| `subskills/spatial-index-structures.md` | `software-engineering/spatial-index-structures` | R-trees, quadtrees, and space-filling encodings, and what each is for. |
| `subskills/bounding-boxes-and-filters.md` | `software-engineering/bounding-boxes-and-filters` | The cheap approximate filter and where it misleads. |
| `subskills/distance-and-proximity.md` | `software-engineering/distance-and-proximity` | Great-circle distance, projections, and radius queries. |
| `subskills/nearest-neighbour.md` | `software-engineering/nearest-neighbour` | The k-NN query and the index that makes it fast. |
| `subskills/polygons-and-containment.md` | `software-engineering/polygons-and-containment` | Point-in-polygon, polygons that self-intersect, and validity. |
| `subskills/geospatial-record.md` | `software-engineering/geospatial-record` | The written record: reference systems, indexes, and their measured behaviour. |

## Status and honest limits

Spatial behaviour is measurable but the measurements are data-shaped: an R-tree's performance depends on the distribution of the geometry, and a uniform test set flatters indexes that real coastlines punish. Nothing here recommends a spatial extension or promises a latency; every performance statement belongs in the record with the dataset, the index, and the date, because spatial query times move an order of magnitude with data shape, not with tuning.
