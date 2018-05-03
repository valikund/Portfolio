import numpy as np

asd = [[1,2,3,4],[1,2,3,4],[5,6,7,8]]
asdd = np.asarray(asd)
k = asdd.shape[0]
threshold = 1/k
avg = asdd.mean(axis=0)
avg = np.row_stack((avg,avg,avg))
stdev =  asdd.std(axis=0)
stdev =  np.row_stack((stdev,stdev,stdev))

proximity = np.square(asdd) + np.square(avg) - 2*np.multiply(asdd,avg)
print proximity
proximity = np.divide(proximity, 2*k*np.square(stdev))
proximity = np.sum(proximity, axis=1)
print np.partition(proximity, -2)[-2]
if (asdd.shape[0]-1 == np.argmax(proximity)  and (np.max(proximity)-np.partition(proximity, -2)[-2])>threshold):
    print 'anomaly'