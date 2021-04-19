# tedutil

Utility functions

[![PyPI version](https://badge.fury.io/py/tedutil.svg)](https://badge.fury.io/py/tedutil)
[![Upload to PyPI](https://github.com/tedlaz/tedutil/actions/workflows/publish2pypi.yml/badge.svg)](https://github.com/tedlaz/tedutil/actions/workflows/publish2pypi.yml)
[![Tests](https://github.com/tedlaz/tedutil/actions/workflows/run-tests.yml/badge.svg)](https://github.com/tedlaz/tedutil/actions/workflows/run-tests.yml)
[![codecov](https://codecov.io/gh/tedlaz/tedutil/branch/master/graph/badge.svg)](https://codecov.io/gh/tedlaz/tedutil)

# Σχετικά

Βιβλιοθήκη γραμμένη σε python που αφορά την επεξεργασία δεδομένων διαφόρων τύπων που αφορούν την Ελλάδα όπως:

- Διαχείρηση Ελληνικών ημερομηνιών
- Έλεγχοι ορθότητας ΑΦΜ, ΑΜΚΑ
- Δημιουργία αρχείων κειμένου για ΑΠΔ, ΦΜΥ κλπ
- Υπολογισμός Φόρων (Εισόδημα, ΕΕΑ)

# Εγκατάσταση

```bash
pip install tedutil
```

# Ταξινόμηση εγγραφών με regular expressions
a  b  c  d    v        z
1  2  6  7  54.00   3,5,4,8

20.00.00.024  100 -> b (Επειδή κανονικά πρέπει να είναι χρεωστικό)
54.00.00.024   24 -> v
50.* ή 38.*  -124 -> Z Αγνούνται άρα είναι στο τέλος
bvΖ 

20.00.00.024  100 -> b
54.00.00.024   24 -> v
64.00.00.024  100 -> c
54.00.29.024   24 -> v
50.* ή 38.*  -248 -> Z
bcvΖ

70.00.00.024 -100 -> 7 D
54.00.70.024  -24 -> 7 V
30.* ή 38.*   124 -> v z
DVz

70.00.00.024 100 -> 7 D
54.00.70.024  24 -> f D
