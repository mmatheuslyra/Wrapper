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
### Environment Definitions

To execute the algorithms remotely, it is necessary to specify the new environments in the "environment" directory. 

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```
