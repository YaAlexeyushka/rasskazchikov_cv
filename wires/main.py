from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np


struct = np.ones((3, 3))

image = np.load("wires6npy.txt")

labeled_image = label(image)

for i in range(1, labeled_image.max()+1):
    wire = labeled_image == i 
    result = label(binary_erosion(wire)).max()

    if result == 1:
        print("Провод", i, "целый")
    
    elif result == 0:
        print("У провода", i, "нет частей")

    else:   
        print("Провод", i, "имеет", result, "частей")

plt.imshow(labeled_image)
plt.show()



