import sys


class Cluster(object):

    def __init__(self, centroid):
        self.centroid = centroid
        self.points = []

    def update_centroid(self):
        if not self.points:
            return
        total = Vector([0] * len(self.points[0]))
        for point in self.points:
            total += point
        self.centroid = total / len(self.points)

class Vector(object):

    def __init__(self, values):
        self.values = values

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.values, other.values)])

    def __truediv__(self, scalar):
        return Vector([a / scalar for a in self.values])

    def __len__(self):
        return len(self.values)
    
def main():
    epsilon = 0.001
    deltaCentroid = 0.0
    d, N, k, maxIter, counter = 0, 0, 0, 400, 0
    isConverged = False
    fileName = ""
    clusters, vectors = [], []

    # taking args
    if len(sys.argv) < 3:
        print("not enough arguments")
        sys.exit(1)  

    if len(sys.argv) > 4:
        print("too many arguments")
        sys.exit(1)

    if len(sys.argv) == 3:
        fileName = sys.argv[2]
    
    if len(sys.argv) == 4:
        maxIter = int(sys.argv[2])
        fileName = sys.argv[3]

    k = int(sys.argv[1])
    
    # read data from file
    try:
        with open(fileName, 'r') as f:
            for line in f:
                vector = Vector([float(val) for val in line.strip().split(',')])
                vectors.append(vector)
                N += 1
                if d == 0:
                    d = len(vector.values)
    except FileNotFoundError:
        print(f"File {fileName} not found.")
        sys.exit(1)

    if k <= 1 or k >= N:
        print("Invalid number of clusters!")
        sys.exit(1)
    
    # Initialize centroids 
    for i in range(k):
        centroid = Vector(vectors[i].values.copy())
        clusters.append(Cluster(centroid))
    
    while not isConverged and maxIter > counter:
        # Assign points to clusters

        for cluster in clusters:
            cluster.points = []

        for vector in vectors:
            closest_cluster = min(clusters, key=lambda c: euclidean_distance(vector, c.centroid))
            closest_cluster.points.append(vector)

        isConverged = True

        for cluster in clusters:
            old_centroid = cluster.centroid
            cluster.update_centroid()
            deltaCentroid = euclidean_distance(old_centroid, cluster.centroid)
            if (deltaCentroid >= epsilon):
                isConverged = False
        counter += 1
    
    printCentroids(clusters)

    
def printCentroids(clusters):
    for cluster in clusters:
        print(",".join(f"{value:.4f}" for value in cluster.centroid.values))
    

def euclidean_distance(vec1, vec2):
    return sum((a - b) ** 2 for a, b in zip(vec1.values, vec2.values)) ** 0.5


if __name__ == "__main__":
    main()
    