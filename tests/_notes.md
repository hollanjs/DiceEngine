## testing dice - Chi-Square

```Python
from DiceEngine import SixSidedDie
from math import sqrt
die = SixSidedDie()

roll_count = 600_000
rolls = [die.roll() for _ in range(roll_count)]

expected_freq = roll_count / die.face_count
significance = 0.05
degrees_of_freedom = die.face_count - 1
chi_sqr = sum([((rolls.count(value) - expected_freq) ** 2) / expected_freq for value in range(1, die.face_count + 1)])

# USE SCIPY OR ANOTHER MODULE TO CALCULATE AND GET P-VALUE FOR TESTING

print(x)
```