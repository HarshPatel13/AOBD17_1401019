#Total Convergence after 49 iterations.


from data_utils import *
from PCA import *
from PPCA import *
import math
# Python imports
import time
import numpy as np
import scipy
import random
import matplotlib
import skimage
#matplotlib.use('TkAgg')
import scipy.misc
import pylab
from skimage.color import rgb2gray
from skimage import data
from sklearn.metrics import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from scipy.misc import imread
from PIL import Image
# Seed the random number generator
#np.random.seed(148007482)

start_time = time.time()

# Parameters
N = 50	#this is our number of dimensions
num_points = 1000
s = 1/8 # parameter for the stationary random covatiance matrix

org=mpimg.imread('einst.jpg')
orgb=rgb2gray(org)

#img=mpimg.imread('img_miss_5.jpg')
#img_bw=rgb2gray(img)
#imgplot = plt.imshow(img_gray,cmap=plt.cm.Greys_r)
#plt.show()

RGB_noise = skimage.util.random_noise(org, mode='s&p', seed=None, clip=True, amount=0.2)
RGB_Gray = rgb2gray(RGB_noise)
scipy.misc.imsave('20paper.jpg', RGB_Gray)
plt.imshow(RGB_Gray,cmap=plt.cm.Greys_r)
plt.show()

#pca1 = PCA()
#mult_pca_components = pca1.num_components
mult_pca_components=100
ppca = PPCA(latent_dim = mult_pca_components, max_iter = 200)

data_std = ppca.fit(RGB_Gray)
print("Sucess..")
data_reduced = ppca.transform_data(data_std)
data_reconstructed = ppca.inverse_transform(data_reduced)

#scipy.misc.imsave('outfile.jpg',data_reconstructed )

imgplot = plt.imshow(data_reconstructed,cmap=plt.cm.Greys_r)
plt.show()
rms_error = math.sqrt(mean_squared_error(data_reconstructed,orgb))
print(rms_error)

#main()
print("--- %s seconds ---" % (time.time() - start_time))