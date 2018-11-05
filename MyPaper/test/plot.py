'''
Created on  2018-11-01 17:35:37

@author: quantaolin
'''
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

a = [1, 2, 5, 3, 4]
b = np.array(a)
plt.plot(b)
plt.grid(True) ##增加格点
plt.axis('tight')
plt.show()