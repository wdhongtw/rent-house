# Sample Project for Pure PEP517 Setup Demonstration

PEP517 has define a standard way to do Python packaging.
Thus, we no longer require a `setup.py` file (a turing complete program,
which is usually a bad idea when we only require some static information)
in project root to specify how to package the project.

## How to Use

### Packaging

- Setup a (virtual) Python environment
- Make sure the package `pep517` is available
  - `pep517` is a reference implementation of build frontend
- `python -m pep517.build .`

Then there will be `.tar.gz` and `.whl` file in `dist` folder

### Local Installation

- Setup a (virtual) Python environment
- `pip install .`
  - Require `pip` version larger then `10.0`

## References

- <https://www.python.org/dev/peps/pep-0517/>
- <https://setuptools.readthedocs.io/en/latest/build_meta.html>
- <https://setuptools.readthedocs.io/en/latest/setuptools.html>
- <https://pip.pypa.io/en/stable/reference/pip/#pep-517-and-518-support>
