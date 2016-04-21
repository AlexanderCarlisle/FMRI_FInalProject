import scipy.io
import random
import math
import Constants
import numpy
import util

import scipy
from scipy.stats import pearsonr
from matplotlib import pyplot as plt

##add correlation to map at whatever categories they were at
def addToMap (pairCounts, correlationMap,key1, key2, correlation):
	imageCat1 = key1[1]
	imageCat2 = key2[1]
	orderedList = sorted([imageCat1, imageCat2])
	mapKey = (orderedList[0],orderedList[1])
	if mapKey in correlationMap:
		pairCounts[mapKey] = pairCounts[mapKey] +1
		correlationMap[mapKey] = correlationMap[mapKey] + correlation
	else:
		pairCounts[mapKey] = 1
		correlationMap[mapKey] = correlation

def averageCorrelations(correlationMap, pairCounts):
	for k in correlationMap:
		correlationMap[k] = correlationMap[k]/ float(pairCounts[k])


## Between all pairs, calculate correlations
## Store mean correlation between same categories
## Have a map of category -> sumCorrelationsWithinCategory
## there are 5 categories, want average mean between each pair of categories.
## 

def calculateAverageCorrelations(voxelArrayMap):
	util.normalize(voxelArrayMap)
	correlationMap = { }
	counts = { }
	alreadySeen = set()
	#Between all pairs of vectors, want to add their correlation to the correspond [cat1][cat2] spot in matrix
	for k1 in voxelArrayMap:
		for k2 in voxelArrayMap:
			if k1 is not k2 and (k1,k2) not in alreadySeen and (k2,k1) not in alreadySeen:
				alreadySeen.add((k1,k2))
				alreadySeen.add((k2,k1))
				correlation = scipy.stats.pearsonr(voxelArrayMap[k1],voxelArrayMap[k2])[0]
				combKey = (min(k1[1], k2[1]),max(k1[1], k2[1]))
				if combKey in correlationMap:
					correlationMap[combKey] += correlation
					counts[combKey] += 1
				else:
					correlationMap[combKey] = correlation
					counts[combKey] = 1
	averageCorrelations(correlationMap, counts)
	return correlationMap

	#Given the voxelArray for an example, calculate its average correlation against the different categories
def calculateSingleExampleCorrelations(example, voxelArrayMap):
	categoryCorrelationMap = [0]*5
	countsMap = [0]*5
	for key in voxelArrayMap:
		vec1 = voxelArrayMap[key]
		correlation = scipy.stats.pearsonr(vec1, example)[0]
		imageCat = key[1]
		if imageCat in categoryCorrelationMap:
			categoryCorrelationMap[imageCat] += correlation
			countsMap[imageCat] += 1
		else:
			categoryCorrelationMap[imageCat] = correlation
			countsMap[imageCat] = 1
	for i in range(len(categoryCorrelationMap)):
		categoryCorrelationMap[i]/= countsMap[i]

	return categoryCorrelationMap


def matrixify(map):
	matrix = [[0 for x in range(5)] for x in range(5)] 
	for key in map:
		row = key[0]
		col = key[1]
		matrix[row][col] = map[key]
		matrix[col][row] = map[key]
	return matrix
## will just make a 5 by 5 matrix, of average correlations
## Then we get our one row and compare it to which row is closest
'''
exampleCorrelations is a map of mean correlations between examples and all examples of a data type
#For instance, exampleCorrelations[0] is mean correlation between our example and all ampl data for faces
averageCategoryCorrelations is map of all pairs of images and their mean correlations.
That is averageCategoryCorrelations(0,1) would give average mean of correlations between faces, bodies in train data. 
'''
def classifyByClosestCorrelation(exampleCorrelations, averageCategoryCorrelations):
	#Lets say (ex,0) = 5, (ex,1) = 15,(ex,2) = -30,(ex,3) = 40,(ex,4) = 100,
	#Can 		 (1,0) =3, (2,0) = 5...
	#should really see our 0 - their 0, our 1 vs real 1
	#For each possible category the image could be, 
	#We will go through and see how far its correlation to each category compares to average
	distances = [0]*5
	correlations = [0] *5
	indClosest = [0]*5
	for y in range(5):
		distances[y] = util.getDistance(exampleCorrelations,averageCategoryCorrelations[y])
		correlations[y] = scipy.stats.pearsonr(exampleCorrelations, averageCategoryCorrelations[y])[0]
		differences = [abs(a - b) for a,b in zip(exampleCorrelations, averageCategoryCorrelations[y])]
		indClosest[y] = min(differences)
	return (distances.index(min(distances)), indClosest.index(min(indClosest)), correlations.index(max(correlations)) )


''' Our voxelArray came from some imageType.
	We know what each x,other type ought to be
	And we can calculate correlation between our x and all other image types
	then choose image type with closest correlation
	'''
def correlationNearestNeighbor():
	voxelArrayMap = util.getVoxelArray(False, False,True,False, [4])
	
	util.normalize(voxelArrayMap)
	correct = [{ }]*3
	totalCountCorrect = [0] *3
	totalCountInCorrect = [0] *3
	incorrect = [{ }]*3
	voxelCopy = voxelArrayMap.keys()
	totalCorrect =0
	totalIncorrect =0
	count = 0
	for key in voxelCopy:
		count +=1
		testExample = voxelArrayMap[key]
		voxelArrayMap.pop(key, None)

		averageCategoryCorrelations = matrixify(calculateAverageCorrelations(voxelArrayMap))
		exampleCorrelations = calculateSingleExampleCorrelations(testExample, voxelArrayMap)
		classifiedCategory = classifyByClosestCorrelation(exampleCorrelations,averageCategoryCorrelations)

		if classifiedCategory[0] == key[1]:
			totalCorrect +=1
		else:
			totalIncorrect +=1
		voxelArrayMap[key] = testExample
	print "Correct", totalCorrect, "Incorrect", totalIncorrect, "Percentage Correct ", totalCorrect/float((totalCorrect +totalIncorrect))







	## Now go for each example calcuate mean covariance against each image type
	## and choose closes	
correlationNearestNeighbor()











