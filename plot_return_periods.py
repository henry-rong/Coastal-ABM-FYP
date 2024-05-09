import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],  # Specify your preferred font here
})

# Define return periods with corresponding years
return_periods = {
    'rp0001': 1, 'rp0002': 2, 'rp0005': 5, 'rp0010': 10,
    'rp0050': 50, 'rp0100': 100, 'rp0250': 250, 'rp0500': 500, 'rp1000': 1000
}

# Generate return periods in numerical order
sorted_return_periods = sorted(return_periods.items(), key=lambda x: int(x[0][2:]))

def generate_return_period() -> str:
    rp0001 = 1-1/2-1/5-1/10-1/50-1/100-1/250-1/500-1/1000
    probabilities = [rp0001, 1/2, 1/5, 1/10, 1/50, 1/100, 1/250, 1/500, 1/1000]
    sampled_return_period = np.random.choice(a=[rp for rp, _ in sorted_return_periods], p=probabilities)
    return sampled_return_period

X = []

for i in range(10000):
    X.append(generate_return_period())

# Convert return periods to corresponding years
X_years = [return_periods[rp] for rp in X]

sns.histplot(data=X_years)

# Set x-axis labels to years
# plt.xticks(np.arange(1, 1001, 100))

plt.title('KDE of Return Periods')
plt.xlabel('Return Period (Years)')
plt.ylabel('Density')

plt.show()
