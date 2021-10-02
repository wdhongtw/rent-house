# Simple 591 Crawler

## Local Installation

- Setup a (virtual) Python environment (optional)
- Ensure build dependency: `pip install -U setuptools wheel`
- `pip install .`
  - Require `pip` version larger then `10.0`

## Usage

```shell
# See rent-591.md for well-known parameter
cp settings-sample.toml settings.toml

# Start scanning loop
web591.py -c settings.toml scan

# Export records from database to CSV
export.py houses.sqlite3 houses.csv
```

## Related Work

- [M157q/sgl](https://github.com/M157q/sgl)
- [g0v/tw-rental-house-data](https://github.com/g0v/tw-rental-house-data/)
