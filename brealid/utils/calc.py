# Function to calculate mean
def mean(data):
    return sum(data) / len(data)

# Function to calculate standard deviation
def std(data):
    _mean = mean(data)
    variance = sum((x - _mean) ** 2 for x in data) / (len(data) - 1)
    return variance ** 0.5