# DustBadge

**Area:** Mining · **Status:** Concept · **Prototype budget:** about $90 USD · **Difficulty:** 3 of 5

A low-cost wearable dust monitor for workers in quarries, mines, stone fabrication and construction that estimates respirable dust exposure through the shift and warns before limits are reached.

## Concept rationale

Real-time feedback lets workers and supervisors change practice during the shift, which a lab result days later cannot do.

## Burning platform

Silicosis is resurging among engineered stone workers in several countries, and millions of miners and quarry workers are exposed without monitoring.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Health and safety in mining was the second gap identified in the mining research area.

## Problem

Respirable crystalline silica causes silicosis, which is incurable. Personal exposure sampling is expensive and results arrive days later, so most workers never know their exposure.

## Concept

A low-cost wearable dust monitor for workers in quarries, mines, stone fabrication and construction that estimates respirable dust exposure through the shift and warns before limits are reached.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Optical particle sensor
- Low-power microcontroller with Bluetooth
- Vibration motor and LED alert
- Rechargeable cell, full-shift capacity
- Clip-on enclosure near the breathing zone
- Phone app for shift log

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> A research and educational prototype, not certified personal protective or monitoring equipment. It does not replace approved sampling or respirators. Lithium cells can overheat, vent and burn. Use protected cells or LiFePO4, fuse every pack, charge only within the cell maker's limits and never leave a first build charging unattended.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
