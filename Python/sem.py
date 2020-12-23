import scipy

def plot_mean_and_sem(array, axis=1):
    mean = array.mean(axis=axis)
    sem_plus = mean + scipy.stats.sem(array, axis=axis)
    sem_minus = mean - scipy.stats.sem(array, axis=axis)
    
    fill_between(np.arange(mean.shape[0]), sem_plus, sem_minus, alpha=0.5)
    plot(mean)
