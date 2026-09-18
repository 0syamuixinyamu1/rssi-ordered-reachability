# Publication Audit

Audit date: 2026-09-18. This is a release audit of the frozen RSSI A–F
synthetic series. It does not add an experiment, parameter, metric, or claim.

## Result

The public snapshot passed the portable artifact, claim-value, documentation,
scope, hygiene, and full-file hash checks. The existing A–F generators were
also rerun in temporary directories and all 45 designated reproducibility
outputs matched the frozen uncompressed bytes.

| Check | Result |
| --- | --- |
| Frozen artifact manifest | 74 entries; hashes, byte sizes, and row counts matched |
| CSV inventory | 43 tables; 745,735 data rows |
| Large-file publication transform | 9 deterministic gzip files; uncompressed SHA-256 retained |
| Existing A–F reproduction | 45/45 designated files matched |
| Representative claim values | A–F checks passed |
| Markdown links and claim categories | 351 links and 7 categories passed |
| License and citation metadata | Passed |
| Absolute private paths / common secret patterns | No matches in 81 published text files |
| Complete snapshot hash inventory | 151 files matched (plus the inventory itself) |

The reproduction comparison covered 3 A files, 4 B files, 5 C files, 10 D
files, 11 E files, and 12 F files. Temporary outputs were discarded and the
frozen results were not overwritten.

## Scientific identity and publication transforms

The [artifact manifest](../results/frozen/MANIFEST.json) records both stored
and uncompressed hashes. Seventy-three of 74 manifest entries preserve the
original uncompressed bytes exactly. The sole metadata normalization is the
removal of machine-specific command paths from F `analysis.json`; its
scientific fields are unchanged.

Large CSV files are stored as deterministic gzip archives so the repository
remains suitable for ordinary Git hosting. Their uncompressed hashes—not the
compression container bytes—are the scientific artifact identities.

## Public/private boundary

Included material is sufficient to rerun the frozen Python A–F generators and
audit their published outputs. The following were intentionally excluded:

- the separate/private Ideal E1–E8 implementation, fixtures, and tests;
- machine-specific workspace snapshots and absolute checkout paths;
- failed native-runtime search paths;
- environment-specific historical command arrays.

Those exclusions are not converted into positive native-validation claims.
See [Boundary and provenance](BOUNDARY_AND_PROVENANCE.md) and the
[machine-readable publication boundary](../results/frozen/PUBLICATION_BOUNDARY.json).

## Commands

Read-only snapshot audit:

```bash
python scripts/validate_snapshot.py
```

Existing A–F reproduction in temporary output directories:

```bash
python scripts/reproduce.py --series all
```

The machine-readable result is
[PUBLICATION_VALIDATION.json](../results/frozen/PUBLICATION_VALIDATION.json).

## Claim discipline

The audit confirms consistency with the frozen scope; it does not establish
external validity. In particular, it does not validate a deployed recursive
self-improving AI, a native HohoEngine RSSI loop, real LLM behavior, human
belief dynamics, arbitrary high-dimensional systems, or an alignment solution.
