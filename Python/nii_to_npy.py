import numpy as np
import nibabel as nib
import sys

img = nib.load('/homes/1/sq566/Downloads/dwib0-pad.nii.gz')
imgU16 = img.get_data().astype(np.int16)

non_brain_value = imgU16[0][0][0]
non_brain_region = imgU16 == non_brain_value
imgU16[non_brain_region] = 0.0

np.save('/homes/1/sq566/Downloads/before_norm.npy', imgU16)
