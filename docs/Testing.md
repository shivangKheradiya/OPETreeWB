# OPETreeWB – Test Specification

This document lists all test files and describes
what each test validates.

All tests are executed **inside FreeCAD**.

---

## How to Run Tests

Open FreeCAD → Python Console and execute:

```python
from opetreewb.tests.run_tests import run_all
run_all()
````

***

## Test List

### T0001.py

**Purpose:**  
Validate static domain configuration rules.

**What is validated:**

*   Domain keys `DESI` and `DICT` exist
*   `RootType` values are correct
*   No unexpected mutation of domain rules

**Layer:**  
Domain (pure logic, no FreeCAD UI)

***

### T0002.py

**Purpose:**  
Validate unified node label formatting.

**What is validated:**
- Type + Name formatting
- Fallback to Node ID
- Fallback to default type when missing

**Layer:**
Domain

### T0003.py
**Purpose:**  
Ensure domain rules are treated as invariant configuration.

**What is validated:**
- Domain rules are not meant to be mutated at runtime
- Violations are detectable during development

**Layer:**  
Domain