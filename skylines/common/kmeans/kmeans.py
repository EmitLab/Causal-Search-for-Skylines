import numpy as np
from random import Random

class KMeans:

    def __init__(self, bins, max_iterations, tolerance, seed):
        self.bins = bins
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.random = Random(seed)

        self.iterations = 0
        self.labels = None

    def _initialize_centroids(self, data: np.ndarray):
        n_samples, n_features = data.shape
        centroids = np.empty((self.bins, n_features))

        # Choose first centroid randomly
        idx = self.random.randint(0, n_samples)
        centroids[0] = data[idx]

        # Track the closest distance to any selected centroid
        diff = data - centroids[0]
        closest_dist_sq = np.einsum('ij,ij->i', diff, diff)

        for c in range(1, self.bins):
            # Normalize distances to form probability distribution
            closest_dist_sq_sum = np.sum(closest_dist_sq)
            if closest_dist_sq_sum == 0:
                probs = np.full_like(closest_dist_sq, 1.0 / len(closest_dist_sq))
            else:
                probs = closest_dist_sq / closest_dist_sq_sum

            # Efficient weighted random selection using np.searchsorted
            r = self.random.random()
            cumulative_probs = np.cumsum(probs)
            idx = np.searchsorted(cumulative_probs, r)

            # Assign next centroid
            centroids[c] = data[idx]

            # Update closest distances
            new_dist_sq = np.sum((data - centroids[c]) ** 2, axis=1)
            np.minimum(closest_dist_sq, new_dist_sq, out=closest_dist_sq)

        return centroids

    def cluster(self, data: np.ndarray):
        # Initialize centroids using KMeans++
        centroids = self._initialize_centroids(data)

        # Initialize variables
        self.labels = np.full(data.shape[0], -1)
        changed = True

        # Iteratively find the clusters
        for self.iterations in range(1, self.max_iterations + 1):
            if not changed:
                break
            changed = False

            # Assign points to nearest centroid using vectorized distance computation
            diff = data[:, None, :] - centroids[None, :, :]
            sum_squared_diff = np.einsum('ijk,ijk->ij', diff, diff)

            # Assign labels based on the minimum distance
            new_labels = np.argmin(sum_squared_diff, axis=1)

            # Check for changes in labels
            if not np.array_equal(self.labels, new_labels):
                self.labels = new_labels
                changed = True

            # Update the centroids based on the new labels
            for i in range(self.bins):
                cluster_points = data[self.labels == i]
                if cluster_points.shape[0] > 0:
                    new_centroid = cluster_points.mean(axis=0)

                    # Update centroid if there is significant change
                    if np.any(np.abs(centroids[i] - new_centroid) > self.tolerance):
                        centroids[i] = new_centroid
                        changed = True
