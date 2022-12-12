# Clustering Algorithm Implementation
### By James Camacho and Joseph Camacho

We are implementing ["Sublinear Time and Space Algorithms for Correlation Clustering via Sparse-Dense Decompositions"](https://doi.org/10.48550/arxiv.2109.14528).

## Setup
To install data, run
```
bash setup.sh
```

Ideas on what to check:
- What is the probability it actually ends up being a laminar group of sets?
- How close to optimal is it when we vary `eps` and `c`?
- How does this compare with different data sets? Dictionary vs. random clusters?
