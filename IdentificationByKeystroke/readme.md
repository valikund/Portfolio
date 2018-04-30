# User Identification Based on Typing Patterns:

Created a classifier for identification based on typing, used feature based machine learning methods with Scikit Learn. Achieved 97% accuracy. Won the inhouse challange during the Data Mining class. The data was recorded from several users trough a javascript client, the data was provided to me by a professor. The classifier is based on trnsforming the data to features with Dinamic Time Warping. I fitted several types of classifiers, but later decided to use only knn as a base algorithm. I used knn inside a semisupervised algorithm I created, to get from 84% accuracy to 97%.

# The files:

## Raw data:
keystrokes-12users-raw-data.txt	
keystrokes-12users-test-hypothetic-labels.txt
keystrokes-12users-train-labels.txt

## Preprocessed files: 
dtw_matrix1.npy	
dtw_matrix2.npy	
dtw_test1.npy	
dtw_test2.npy
test_index.npy	
test_y.npy

## Different files for preprocessing:
all start with DTW
the best version is "DTW_Legjobb.ipynb"

## Files for model fitting:
all the other .ipynb files
the best version is "LEGJOBB.ipynb"
