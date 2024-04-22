import numpy as np
import matplotlib.pyplot as plt

return_periods = ['rp0001', 'rp0002', 'rp0005', 'rp0010', 'rp0050', 'rp0100', 'rp0250', 'rp0500', 'rp1000']
rp0001 = 1-1/2-1/5-1/10-1/50-1/100-1/250-1/500-1/1000 # make the rp0001 the default if none of the other return periods occur
probabilities = [rp0001,1/2,1/5,1/10,1/50,1/100,1/250,1/500,1/1000]



D = dict((rp,0) for rp in return_periods)


for x in range(1000):

    sampled_return_period = np.random.choice(a = return_periods,p = probabilities)

    D[sampled_return_period] += 1




plt.bar(range(len(D)), list(D.values()), align='center')
plt.xticks(range(len(D)), list(D.keys()))

plt.show()
