# Bala's all-column diagonal identity

This note derives the coefficient identity as a polynomial in the column parameter from the binomial identity proved by Wildon in 2013 and identified by Gessel as terminating Kummer summation. The exact specialization is given explicitly. It includes complete written proofs of further consequences and precise attribution of the previously proved column identities and supercongruences.

## Files and rebuilding

The source archive contains `note.tex` with its bibliography, this README, `metadata.json`, `verify.py`, the two expected checker outputs, and `MANIFEST.json`. The readable `note.pdf` accompanies the archive separately.

Build with Tectonic 0.17.0:

```sh
tectonic note.tex
python3 verify.py > checker-output.json
python3 verify.py --siblings > sibling-checker-output.json
```

Alternatively, run `pdflatex note.tex` twice. The bibliography is embedded, so no BibTeX step is necessary. The checker needs Python 3.10 or later and the standard library alone.

## Mathematical coverage

For every nonnegative integer `n`, Theorem 1 identifies the nested-radical coefficient, the rational-function diagonal coefficient and Manyama's binomial sum as the same polynomial in `k`. This includes the known boundary columns, the signed array and the main diagonal.

Additional written proofs establish:

- The diagonal and equivalent multiple-sum formulas for columns 1, 2 and 3, with their earlier proofs credited.
- The Gauss congruences `T(mp^r,k) = T(mp^(r-1),k) mod p^r` for all integer parameters `k`, all primes `p`, and positive integers `m,r`.
- A polynomial identity for `T(n,k)^2`, including Bala's squared-coefficient conjecture for column 2.
- The odd companion's radical generating function, integral description and recurrence.
- The even and odd fixed-positive-parameter asymptotics and the varying-parameter formula for `k=b_n^2`, `b_n>=2`, `b_n=o(n)`, including the main diagonal.

The main binomial evaluation has an elementary proof in [Wildon's 2013 answer](https://mathoverflow.net/a/150152). Its application here is obtained by comparing each coefficient of the column parameter, not by a priority claim about a new evaluation. The stronger column supercongruences modulo `p^(2r)` are consequences of the prior theorems of Pan and Sun (2020) and Blanco Gómez (2026). The note also credits Bala's 2025 column-1 proof and Blanco Gómez's 2026 column-2 and column-3 proofs as well as Epstein's 2026 explicit application of Pan–Sun.

The declaration `D5.S3.Combinatorics.PowerSeries.BalaA337389Diagonal.result` in the [pinned Lean file](https://github.com/the-omega-institute/trureturing/blob/3378450a2176909e857354ab064dde6ec7679b71/D5/S3/Combinatorics/PowerSeries/BalaA337389Diagonal.lean) proves the coefficient identity for all natural parameters and degrees over rational formal power series, including existence of the normalized radical pair and the identity for every pair satisfying its equations. The polynomial extension, congruences, square identity, recurrence consequences and asymptotics have the written proofs and cited supporting theorems in the note; their scope is distinct from that declaration.

The two checker outputs describe exact finite comparisons, not substitutes for the unbounded arguments. The default comparison ranges are unchanged from the earlier coefficient package. The `--siblings` comparisons cover the additional square identity, odd recurrence, column sums and congruences over the ranges recorded in `sibling-checker-output.json`. Asymptotic conclusions follow from the written dominated-convergence argument, not from numerical fitting.

## Sources and license

The primary posing locator is the final FORMULA of [A337389, revision 40](https://oeis.org/history/view?seq=A337389&v=40), signed Peter Bala on May 3, 2022. The coverage table gives the exact status of each related source item. Only the existing problem ID `bala337389` is used in metadata.

Creators, in order: Haobo Ma (ChronoAI Pte Ltd, Singapore); Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore). The note and original accompanying source are licensed under CC BY 4.0 (`cc-by-4.0`). Cited works retain their own terms.
