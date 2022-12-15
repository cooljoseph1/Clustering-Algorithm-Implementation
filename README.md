# Clustering Algorithm Implementation
### By James Camacho and Joseph Camacho

We are implementing ["Sublinear Time and Space Algorithms for Correlation Clustering via Sparse-Dense Decompositions"](https://doi.org/10.48550/arxiv.2109.14528).

## Setup
To install data, run
```
git clone https://github.com/cooljoseph1/Clustering-Algorithm-Implementation.git
bash setup.sh
```

## Files
`Final Paper.pdf` - Our final paper.
`cluster/cluster.py` - Our implementation of Assadi & Wang's paper.
`cluster/graph.py` - Builds random graphs, and contains a generic graph class.
`cluster/load.py` - Loads the thesaurus graph.
`cluster/load_vector.py` - Loads a word vector graph.
`cluster/laminar_tests.py` - Some tests to check how close to laminar the candidate clusters are.