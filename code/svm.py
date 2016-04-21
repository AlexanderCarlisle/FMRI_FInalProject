import Constants
import util
import numpy
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC

class SVM:
  def test(self, categories):
    for i in range(Constants.NUM_SUBJECTS):
      trainSubjects = [1, 2, 3, 4]
      testSubjects = [i + 1]
      trainSubjects.remove(i + 1)

      trainVoxelArrayMap = util.getVoxelArray(subjectNumbers = trainSubjects)
      testVoxelArrayMap = util.getVoxelArray(subjectNumbers = testSubjects)
      util.normalize(trainVoxelArrayMap)
      util.normalize(testVoxelArrayMap)
      util.filterData(trainVoxelArrayMap, categories=categories)
      util.filterData(testVoxelArrayMap, categories=categories)

      Xtrain = numpy.array([trainVoxelArrayMap[key] for key in trainVoxelArrayMap])
      Ytrain = numpy.array([key[1] for key in trainVoxelArrayMap])

      Xtest = numpy.array([testVoxelArrayMap[key] for key in testVoxelArrayMap])
      Yanswer = numpy.array([key[1] for key in testVoxelArrayMap])

      Yprediction = OneVsRestClassifier(LinearSVC()).fit(Xtrain, Ytrain).predict(Xtest)
      # Yprediction = OneVsOneClassifier(LinearSVC()).fit(Xtrain, Ytrain).predict(Xtest)

      correct = 0
      for index in range(len(Yanswer)):
        if Yanswer[index] == Yprediction[index]:
          correct += 1
      # correct = [1 if Yanswer[index] == Yprediction[index] else 0 for index in range(len(Yanswer))]
      print categories, "Correct Predictions: ", correct, "/", len(Yanswer)
      return float(correct) * 100 / len(Yanswer)

if __name__ == '__main__':
  print 'SVM BINARY CLASSIFICATION'
  # for subject in range(Constants.NUM_SUBJECTS):
  classification = 0
  for i in range(Constants.NUM_CATEGORIES):
    for j in range(Constants.NUM_CATEGORIES - i - 1):
      svm = SVM()
      classification += svm.test([i, j + i + 1])
  print 'Average classification rate =', classification / ((Constants.NUM_CATEGORIES * (Constants.NUM_CATEGORIES - 1)) / 2)
