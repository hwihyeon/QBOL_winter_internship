import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np


#This function draws circle on the image
def draw_circle(x,y,r,color):
    for i in range(512):
        for j in range(512):
            if pow((i-x),2) + pow((j-y),2) > pow(r-1,2) and pow((i-x),2) + pow((j-y),2) < pow(r+1,2):
                plt.scatter(i,j,c=color,marker='.',s=0.5,alpha=0.1)

#draw circle as a reference of SPDC pair position: we obtain these values from SPDC_Fitting_Ring.py,
#radius is the mean value of outer circle's and inner circle's radius
center_x = 250
center_y = 239
radius = 167



#Data: we have 100 data each, for noise and spdc signal. Both exposure time: 1ms
#Check noise level
'''
sample_noise_mtx = tiff.imread(f'noise_X75.tif')
noise_Arr = sample_noise_mtx.flatten()
print(np.mean(noise_Arr))
print(np.var(noise_Arr))
print(np.std(noise_Arr))
plt.hist(noise_Arr,bins=50)
plt.xlim(180,220)
plt.show()
plt.clf()'''

'''
Arr_noisemax = np.zeros(100)
Arr_spdcmax = np.zeros(100)
Arr_spdcmin = np.zeros(100)
for i in range(100):
    noise_mtx = tiff.imread(f'noise_X{int(i+1)}.tif')
    Arr_noisemax[i] = np.max(noise_mtx)
    spdc_mtx = tiff.imread(f'spdc_X{int(i+1)}.tif')
    Arr_spdcmax[i] = np.max(spdc_mtx)
    Arr_spdcmin[i] = np.min(spdc_mtx)


plt.plot(Arr_noisemax,label='noise maximum')
plt.plot(Arr_spdcmax,label='spdc maximum')
plt.legend()
plt.show()
plt.clf()
'''


def second_largest_number(arr):
    second = largest = 0
    for n in arr:
        if n > largest:
            second = largest
            largest = n
        elif second < n < largest:
            second = n
    return second



def plot_spdcmtx(filename):
    sample_spdc_mtx = tiff.imread(filename)

    # I am using this color limit : max count - gap ~ max count, where gap is max count - second largest count
    #c_below = second_largest_number(sample_spdc_mtx.flatten()) - ( np.max(sample_spdc_mtx) - second_largest_number(sample_spdc_mtx.flatten()))
    #c_above = np.max(sample_spdc_mtx)
    c_below = 260
    c_above = 280

    out_radius = 178
    in_radius = 156
    radius_gap = out_radius - in_radius

    # One dot is too small. We exagerrate the dot.
    exaggerate_level = 7 # expand a pixel to 7*7 pixel in visualization
    exagger_shift = int(exaggerate_level/2)
    x_Arr = np.where(sample_spdc_mtx > c_below)[0]
    y_Arr = np.where(sample_spdc_mtx > c_below)[1]

    # we only visualize the photons near spdc cone
    for point_idx in range(len(x_Arr)):
        if pow( in_radius - radius_gap , 2) < pow( x_Arr[point_idx] - center_x , 2) + pow( y_Arr[point_idx] - center_x , 2) < pow( out_radius + radius_gap , 2) :
            for i in range(exaggerate_level):
                for j in range(exaggerate_level):
                    sample_spdc_mtx[x_Arr[point_idx] - exagger_shift + i ][y_Arr[point_idx] - exagger_shift + j] = sample_spdc_mtx[x_Arr[point_idx]][y_Arr[point_idx]]
        else:
            sample_spdc_mtx[x_Arr[point_idx]][y_Arr[point_idx]] = 0


    plt.imshow(sample_spdc_mtx,'hot')
    plt.clim(c_below,c_above)
    plt.colorbar()
    draw_circle(center_x,center_y,radius,'white')

#plot_spdcmtx(f'spdc_X52.tif')
#plt.show()



#----------------------Making a gif file-------------------#
import imageio
import os

Num_image = 100
def img_file_to_gif(img_files, output_file_name):
    ## making gif file from imge file list
    imgs_array = [np.array(imageio.imread(img_file)) for img_file in img_file_lst]
    imageio.mimsave(output_file_name, imgs_array, duration= 300 / Num_image) #duration indicates the gif frame change speed


#### temporary image generation ####
img_file_lst = []
for img_num in range(Num_image):
    plot_spdcmtx(f'spdc_X{int(img_num+1)}.tif')
    output_img_file_name = 'temp_img_{}.png'.format(img_num)
    img_file_lst.append(output_img_file_name)
    plt.savefig(output_img_file_name,bbox_inches='tight',dpi=100)
    print(f'{100*img_num/Num_image}%') # show progress
    plt.close()
img_file_to_gif(img_file_lst, "animation_spdc_nearcone.gif")
print('complete')


#### temporary image delete ####
for img_file in img_file_lst:
    if os.path.exists(img_file):
        os.remove(img_file)
print('image file delete complete')
