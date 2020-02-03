from numpy import array, where, in1d, log, unique

def MI_numpy(x, y):
    num_rows, num_cols = x.shape
    mi_arr = []
    for i in range(0, num_cols):
        x_feature = x[:,i]
        y_target = y
        x_feature_uniq = unique(x_feature)
        y_target_uniq = unique(y_target)
        likely_outcome = x_feature.size
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

x = array([[0, 0, 0],
           [1, 1, 0],
           [2, 0, 1],
           [2, 0, 1],
           [2, 0, 1]])
y = array([0, 1, 2, 2, 1])

print(MI_numpy(x,y))
