# Running the RAO* Experiments

This checkout is already a Git repository.  The original code expects to be
imported as a package named `rao`, so this repository includes a small
compatibility package at `rao/` that points Python imports at the repository
root.

## Environment

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The repository also includes local compatibility shims for the historical
`rmpyl`, `pytemporal`, and `pysulu` packages.  They implement the subset needed
by the included examples and use straight-line path generation for pSulu-style
paths.

## Autonomous Science Agents

From the repository root:

```bash
PYTHONPATH=. .venv/bin/python tests/psulu/test_fake_planner.py
PYTHONPATH=. .venv/bin/python tests/psulu/test_tfake_planner.py
PYTHONPATH=. .venv/bin/python tests/psulu/test_psulu.py
```

These commands generate policy artifacts such as `rover_policy_fake.svg`,
`rover_policy_tfake.svg`, `rover_psulu_policy.svg`, `*.tpn`, and `*.pickle`.

## AFOSR FlightGear Temporal Example

This is the only AFOSR script in this checkout that runs RAO* directly:

```bash
cd tests/afosr/flightgear
PYTHONPATH=../../.. ../../../.venv/bin/python test_flightgear_tfake_planner.py
```

It generates `flightgear_policy.svg`, `flightgear_rmpyl.tpn`, and
`flightgear_rmpyl.pickle`.

## Power Supply Restoration

No power-supply-restoration model or experiment entry point is present in this
checkout or its two local Git commits.  Keyword searches for `power`,
`restoration`, `supply`, `breaker`, `circuit`, `bus`, and `load` only find
copied header comments or unrelated examples.  The AFOSR FlightGear example is
a firefighting/route-planning demo, not a power restoration experiment.
