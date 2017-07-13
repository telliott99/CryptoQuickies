#### Probably prime numbers

Wagner (link) says that if a very large random integer *p* (100 decimal digits or more) is

* not divisible by a small prime
* 3^{p-1} mod p = 1

then the number is prime except for a vanishingly small probability, which one can ignore.

Furthermore, should *p* turn out not to be prime, then the RSA public key math would fail, so that will be a clue in case this happens.

This [script](scripts/probably.py) carries out these two checks to generate *p* and *q* and also *m*, sets *e* to a familiar value, calculates the modular multiplicative inverse of *e* mod &phi;, and finally checks the math by doing `c = pow(m,e,n)` followed by `pow(c,d,n)`.

We compare the digits of `m` and `p`:

```
41652195334374510663525916058770381673912991358222
64906224878372249901313308964518533134052338653217

41652195334374510663525916058770381673912991358222
64906224878372249901313308964518533134052338653217

```