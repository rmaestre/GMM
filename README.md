GMM
===

Gaussian Mixture Model Implementation in Pyspark

GMM algorithm models the entire data set as a finite mixture of Gaussian distributions,each parameterized by a mean vector, a covariance matrix  and a mixture weights. Here the probability of each point to belong to each cluster is computed along with the cluster statistics.

This distributed implementation of GMM in pyspark estimates the parameters using the  Expectation-Maximization algorithm and considers only diagonal covariance matrix for each component.

Ressults
==========
A GMM Clustering is run with next parameters (c\_components = 2, n\_iter=100 and convengernce=10) obtained the next means
```
```


![Cluster results](https://raw.githubusercontent.com/rmaestre/GMM/master/images/gmm_clustering.png)
