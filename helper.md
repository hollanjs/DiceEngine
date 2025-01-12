to activate venv in wsl environment:
```
source .venv/bin/activate
```

to deactivate venv in wsl environment:
```
deactivate
```

to build module:
```
python3 setup.py bdist_wheel sdist
```

to install module in local venv for testing:
```
pip install dist/diceengine-0.0.0.tar.gz
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