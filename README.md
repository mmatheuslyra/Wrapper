# Wrapper Library
This project contains a Wrapper Library for the original Word2vec and a set of optimizations, namely, the pWord2vec, pWord2vec_MPI, and Wang2vec algorithms. 
This tool allows the NLP community to run the mentioned algorithms in different computational environments. 

## Getting Started

This tool is ment to be used from a Python terminal, that so, here is an example of how it can be used.

```python
import wrapper

emb = wrapper.Embeddings()
emb.setEnv('remote')
emb.Word2vec()
emb.Wang2vec()
```
* The default algorithm execution utilizes the parameter set as predefined in the environment files, although, it is possible to inform different parameters directly in the command line.

```python
emb.Word2vec(train = 'test.txt', window = 8)
```

### Environment Definitions

To execute the algorithms remotely, it is necessary to specify the new environments in the "environment" directory. 
