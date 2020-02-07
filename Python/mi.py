from numpy import array, where, in1d, log, unique

def MI_numpy(x, y):
    
    if x.size == 0 or y.size == 0:
        raise ValueError('Passed array is empty')
    x_num_rows, x_num_cols = x.shape
    y_num_rows = y.size
    mi_arr = []
    if x_num_rows != y_num_rows:
        raise ValueError('Passed array is not of the same shape')
    for i in range(0, x_num_cols):
        x_feature = x[:,i]
        y_target = y
        x_feature_uniq = unique(x_feature)
        y_target_uniq = unique(y_target)
        likely_outcome = y_num_rows
        mi_total = 0
        for xval in x_feature_uniq:
            for yval in y_target_uniq:        
                xloc = where(x_feature == xval)[0]
                yloc = where(y_target == yval)[0]  
                probx = xloc.size / likely_outcome
                proby = yloc.size / likely_outcome        
                matchXandY = where(in1d(xloc, yloc)==1)[0]
                probxy = matchXandY.size / likely_outcome        
                if probxy > 0.0:
                    mi_total += probxy * log((probxy / (probx * proby)))                
        mi_arr.append(mi_total)
    return mi_arr

# x = array([[0, 0, 0],
#            [1, 1, 0],
#            [2, 0, 1],
#            [2, 0, 1],
#            [2, 0, 1]])
# y = array([0, 1, 2, 2, 1])

x = array([[1],
            [1],
            [2],
            [1]])
y = array([1, 1, 1, 2])

print(MI_numpy(x,y))
