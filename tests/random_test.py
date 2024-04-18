import numpy as np

def generate_return_period():
        
    rp0001 = 1-1/2-1/5-1/10-1/50-1/100-1/250-1/500-1/1000

    return_periods = ['rp0001', 'rp0002', 'rp0005', 'rp0010', 'rp0050', 'rp0100', 'rp0250', 'rp0500', 'rp1000']

    probabilities = [rp0001,1/2,1/5,1/10,1/50,1/100,1/250,1/500,1/1000]
    sampled_return_period = np.random.choice(a = return_periods,p = probabilities)

    return sampled_return_period

for r in range(100):

    print(generate_return_period())