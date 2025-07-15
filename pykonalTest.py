
# uninstalled numpy with:
# pip uninstall numpy
# tried to install something else with:
# pip install "numpy<2.0"
# but this left something that was too low, it wanted something higher
# installed:
# pip install numpy==1.26.4
# ==> this seems to work
# all this was done in the Thonny system shell

## docs: https://malcolmw.github.io/pykonal-docs/index.html
## git: https://github.com/malcolmw/pykonal/tree/master

# Import modules.
import numpy as np
import pykonal
import matplotlib.pyplot as plt
from skimage import io

# settings for the output image
imgCtrX = 50
imgCtrY = 50
imgContours = 200
imgLineWid = 0.3

# file settings
inFile = '4.2.07.png'
outFile = '4.2.07.svg'

# loading the image
image = io.imread(inFile, as_gray=True)  # Load image as grayscale

#starting the calculation
imgHigh = len(image)
imgWide = len(image[0])
print('image height: ' + str(imgHigh))
print('image width:  ' + str(imgWide))

# let's try to make an array the same size as the image, it has to be 3d because this library
v = np.ones((imgHigh,imgWide,1))

# read the values in, there's probably a quick way to do this but eh
for i in range(imgHigh):
    for j in range(imgWide):
        v[i][j] = image[i][j]

# Instantiate EikonalSolver object using Cartesian coordinates.
solver = pykonal.EikonalSolver(coord_sys="cartesian")
# Set the coordinates of the lower bounds of the computational grid.
# For Cartesian coordinates this is x_min, y_min, z_min.
# In this example, the origin is the lower bound of the computation grid.
solver.velocity.min_coords = 0, 0, 0
# Set the interval between nodes of the computational grid.
# For Cartesian coordinates this is dx, dy, dz.
# In this example the nodes are separated by 1 km in in each direction.
solver.velocity.node_intervals = 1, 1, 1
# Set the number of nodes in the computational grid.
# For Cartesian coordinates this is nx, ny, nz.
# This is a 2D example, so we only want one node in the z direction.
solver.velocity.npts = imgHigh, imgWide, 1

# Set the velocity model.
# In this case the velocity is based on image brightness
solver.velocity.values = v 

# Initialize the source. This is the trickiest part of the example.
# The source coincides with the node at index (0, 0, 0)
src_idx = imgCtrY, imgCtrX, 0

# Set the traveltime at the source node to 0.
solver.traveltime.values[src_idx] = 0

# Set the unknown flag for the source node to False.
# This is an FMM state variable indicating which values are completely
# unknown. Setting it to False indicates that the node has a tentative value
# assigned to it. In this case, the tentative value happens to be the true,
# final value.
solver.unknown[src_idx] = False

# Push the index of the source node onto the narrow-band heap.
solver.trial.push(*src_idx)

# Solve the system.
solver.solve()

# And finally, get the traveltime values.
tt = solver.traveltime.values

# make a 2D array the right size
d = np.zeros((imgHigh, imgWide))

# here we do another conversion, this one back to 2D becaue matplotlib
for i in range(imgHigh):
    for j in range(imgWide):
        d[i][j] = tt[i][j][0]


contour_levels = np.linspace(d.min(), d.max(), imgContours)  # asking for 50 contour levels along the travel time

# setting some options for the plot, like black, thin lines, no axes and invert the y
contour_set = plt.contour(d, levels=contour_levels, colors='k', linewidths=imgLineWid)
plt.axis('off')
plt.gca().invert_yaxis()

# save the output
plt.savefig(outFile)

# plot it, because why not?
plt.show()
