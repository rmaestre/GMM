library(MASS)

# Generate data
bivn1 <- mvrnorm(1000, mu = c(0, 0), Sigma = matrix(c(1, .2, .2, 1), 2))
bivn2 <- mvrnorm(5000, mu = c(10, 0), Sigma = matrix(c(0.1, .1, .5, 3), 2))
df <- data.frame(rbind(bivn1, bivn2))
# Write sampling
write.table(df, file="/tmp/bivariate.csv", row.names=FALSE, col.names=FALSE, sep=",")

# Load cluster (in this simple test only one part is generated)
df.clusters <- read.csv("/tmp/bivariate/tmp/clusters/part-00000", sep="\t", header=F)
df$cluster <- df.clusters$V1

# Plot cluster membership
ggplot(aes(x=X1, y=X2), data=df) +
  geom_point(aes(color=cluster))
