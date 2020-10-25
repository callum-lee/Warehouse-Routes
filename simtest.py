import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns 
import scipy.stats as stats


x = stats.norm.rvs(loc= 8300, scale = 1000, size = 1000)


sns.distplot(x)

plt.show()
