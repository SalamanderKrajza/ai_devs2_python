# What is FAISS libriary
**FAISS (Facebook AI Similarity Search)**
is a library developed by Facebook AI Research for efficient similarity search and clustering of dense vectors. 

It provides fast and scalable methods for searching and indexing high-dimensional vectors, making it useful for various applications such as nearest neighbor search, recommendation systems, and image retrieval.

# How it works
FAISS works by building an index of vectors and performing similarity search queries on that index. 

Lets say we have some data:
```
The quick brown fox jumps over the lazy dog.
A quick brown fox quickly jumps over the lazy dog.
The lazy dog sleeps all day long.
The quick brown fox is very agile.
```

### Step 1: Convert the data to vectors by embeddings (text) or feature extraction techniques (images)
Text is converted multi-dimensional (128+) numbers. Lets simplify it to juest 3 dimensions:
```
Text ID | Embedding
1 | [0.2, 0.5, 0.8]
2 | [0.3, 0.6, 0.7]
3 | [0.1, 0.2, 0.3]
4 | [0.4, 0.7, 0.9]
```
In this example, each text is represented by a 3-dimensional vector. The values in the vector capture some semantic information about the text, such as its meaning or context.

### Step 2: Create an Index
Now that we have the embeddings, we can create an index to enable efficient similarity search. The index organizes the embeddings in a way that allows for fast retrieval of similar vectors.

They are multiple types of indexing:
- Flat indexes: Store the vectors as-is without approximation.
- Inverted file indexes: Cluster the vectors into Voronoi cells and search within relevant cells.
- Product quantization indexes: Compress the vectors using quantization for memory efficiency.

Let's take  Flat indexes as simple example:
- It keeps embeddings in **unchanged form** (as lists of numbers)
- The index stores the vectors in a **contiguous block of memory**. This means that the vectors are stored sequentially, one after another, without any gaps or fragmentation (that may slows down the process)
- **Optimized Search Algorithm** to search for nearest neighboars based on L2 Distance **implemented in C++**. In other words - they have functionalities optimized for performence created outside the limitations of python (so using them provies result faster)
- **Parallelization** - it supports parallel search on multiple CPU cores. When you perform a search using the index, Faiss can automatically distribute the search workload across multiple threads, taking advantage of the available CPU resources to further accelerate the search process.

### 3. Use pre-generated indexes for efficient similarity search later.
When a query vector is provided, FAISS uses the pre-built index to quickly find the most similar vectors to our query.

Methods depends on type of indexes. Linear benefits mostly thanks to C++ implementation and pararell search while another may group them. Examples:

IndexFlatL2 (Exhaustive Search):

    IndexFlatL2 does compare the query vector against every vector in the dataset.
    However, it uses optimized algorithms and parallelization to perform this exhaustive search efficiently.
    While it compares against every vector, the search is still faster than a naive linear scan.

IndexIVFFlat (Inverted File Index):

    IndexIVFFlat divides the vector space into Voronoi cells and assigns each vector to a cell.
    During the search, it first finds the closest cells to the query vector and then compares the query vector only against the vectors within those cells.
    By limiting the search to a subset of vectors, it avoids comparing against every vector in the dataset.

IndexHNSW (Hierarchical Navigable Small World):

    IndexHNSW builds a hierarchical graph structure that connects similar vectors.
    During the search, it traverses the graph, starting from the entry point and navigating to the most promising nodes.
    By following the graph structure, it quickly narrows down the search space and avoids comparing against every vector.

# Summary
In summary, the pre-built index enables fast similarity search by organizing the vectors in a way that allows for efficient retrieval. By using optimized algorithms, data structures, and approximation techniques, FAISS avoids comparing the query vector against every vector in the dataset, leading to faster search times compared to exhaustive linear scans.
Claud