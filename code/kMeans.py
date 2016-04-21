import scipy.io
import random
import math
import util

def run():
	voxelArrayMap = util.getVoxelArray(False, False, False, True, [2])
	util.normalize(voxelArrayMap)

	centroids = [0] * 5
	keys = list(voxelArrayMap.keys())
	selected = []
	for index in range(len(centroids)):
		while True:
			centroidKey = random.choice(keys)
			category = centroidKey[1]
			if category not in selected:
				selected.append(category)
				break
		print centroidKey
		centroids[index] = voxelArrayMap[centroidKey]

	numIters = 120
	assignmentMap = {}
	for iteration in range(numIters):
		newCentroids = [ [0] * 1973 for i in range(len(centroids))]
		clusterCounts = [0] * len(newCentroids)
		for key in voxelArrayMap:
			value = voxelArrayMap[key]
			distances = [ util.getDistance(centroid, value) for centroid in centroids ]
			minDistance = min(distances)
			optCentroid = distances.index(minDistance)
			assignmentMap[key] = optCentroid
			for voxelIndex in range(len(newCentroids[optCentroid])):
				newCentroids[optCentroid][voxelIndex] += value[voxelIndex]
			clusterCounts[optCentroid] += 1

		for index in range(len(newCentroids)):
			numPoints = clusterCounts[index]
			if numPoints != 0:
				centroid = newCentroids[index]
				centroid = [ centroid[voxelIndex] / numPoints for voxelIndex in range(len(centroid)) ]
				newCentroids[index] = centroid
		centroids = newCentroids

	# we want ClusterNum -> What type of image
	catMap = {}
	for key in assignmentMap:
		assignment = assignmentMap[key]
		# key[1] is the category (0-5 for face, body, etc)
		# assignment is the optimal centroid
		if assignment in catMap:
			arr = catMap[assignment]
			arr.append(key[1])
			catMap[assignment] = arr
		else:
			catMap[assignment] = [key[1]]
	print catMap

run()