import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny


# Loading Data: this data is obtained by, exposure time=0.3sec, 20 accumulated
spdcring_mtx = tiff.imread('ring.tif')


#This function draws circle on the image
def draw_circle(x,y,r,color):
    for i in range(512):
        for j in range(512):
            if pow((i-x),2) + pow((j-y),2) > pow(r-1,2) and pow((i-x),2) + pow((j-y),2) < pow(r+1,2):
                plt.scatter(i,j,c=color,marker='.',s=0.5,alpha=1)

#-------------- Hough transform : Fitting SPDC cone image to a circle--------------#
# Load picture and detect edges
image = spdcring_mtx
edges = canny(image, sigma=3, low_threshold=10, high_threshold=50)


# Detect two radius : outer edge and inner edge.
# We should estimate the outer radius and inner radius, and manually select the range of np.arange
#----------Finding Inner circle-----------#
hough_radii_inner = np.arange(140, 170, 1) #inner circle
hough_res_inner = hough_circle(edges, hough_radii_inner)

# Select the most prominent circles
accums_inner, cx_inner, cy_inner, radii_inner = hough_circle_peaks(hough_res_inner, hough_radii_inner,
                                           total_num_peaks=1) #total_num_peaks represents the number of circle fitting candidates

for center_y, center_x, radius in zip(cy_inner, cx_inner, radii_inner):
    print(f'inner circle radius: {radius}, inner circle center: {center_x}, {center_y}')
    draw_circle(center_x,center_y,radius,'black')



#----------Finding Outer circle-----------#
hough_radii_outer = np.arange(170,220,1) #outer circle
hough_res_outer = hough_circle(edges, hough_radii_outer)

# Select the most prominent circles
accums_outer, cx_outer, cy_outer, radii_outer = hough_circle_peaks(hough_res_outer, hough_radii_outer,
                                           total_num_peaks=1) #total_num_peaks represents the number of circle fitting candidates

for center_y, center_x, radius in zip(cy_outer, cx_outer, radii_outer):
    print(f'outer circle radius: {radius}, outer circle center: {center_x}, {center_y}')
    draw_circle(center_x,center_y,radius,'black')


#plot
plt.imshow(spdcring_mtx,'jet')
plt.colorbar()
#plt.clim()
plt.savefig('spdc_ring.png',dpi=300)
plt.clf()
