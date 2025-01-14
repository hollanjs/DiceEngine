> Example module:
> [tomchen/example_pypi_package]('https://github.com/tomchen/example_pypi_package/tree/main')

to activate venv in wsl environment:
```
source .venv/bin/activate
```

to deactivate venv in wsl environment:
```
deactivate
```

try using python build (need to add project toml to include additional package dependencies for build)
```
pip install --upgrade build
```

to build module:
```
python -m build
```

to install module in local venv for live testing while developing:
```
pip install --editable .
```

to import module classes into unittests for testing:
```Python
# example
import unittest

from src.DiceEngine import (
    Dice, 
    Die, 
    SixSidedDie,
)
```