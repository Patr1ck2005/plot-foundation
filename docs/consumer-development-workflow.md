# Consumer Development Workflow

Plot Foundation is developed from real A or B requirements while remaining
independent of both repositories.

## Ownership test

Move behavior into Plot Foundation only when its public contract can be stated
with arrays, typed plot models, style policy, and backend artists. Keep it in a
consumer when it depends on column names, file formats, physical interpretation,
registries, output hierarchy, or workflow decisions.

## Environments

- Daily A/B environments install a stable wheel.
- Editable installs belong only in an isolated development environment.
- The compatibility harness may use a temporary `PYTHONPATH` to identify an
  exact uncommitted checkout. Production modules may not do so.
- The COMSOL Python never needs Plot Foundation and must not receive an editable
  shared install.

## Change sequence

1. Add a characterization case in the consumer that requested the behavior.
2. Add the smallest domain-neutral model/renderer contract here.
3. Add package tests, including NaN and invalid-input behavior.
4. Update the consumer adapter and its runtime provenance assertion.
5. Run `tools/verify_consumers.py` and direct acceptance examples.
6. Update the current stage document.
7. Commit Plot Foundation before consumer commits.
8. Build a wheel, install it in a disposable environment, and confirm
   `runtime_info().install_mode == "wheel"` before release.

## Release ranges

Consumers use compatible-release intervals such as
`plot-foundation>=0.1,<0.2`. API-breaking changes require a new minor release
while the major version is zero. Acceptance evidence must record version,
module path, interpreter, and install mode.

