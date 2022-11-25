import matplotlib.pyplot as plt
import numpy as np


def plot_rubik(state):
    tensor = np.zeros(shape=(9,9,9))
    colors = np.zeros(shape=(*tensor.shape, 3))
    min = [-state.coordinates[:,0].min(),-state.coordinates[:,1].min(),-state.coordinates[:,2].min()]
    #  the objects into a single boolean array
    for i, cube in enumerate(state.coordinates):
        tensor[cube[0] + min[0] ,cube[1] + min[1],cube[2] + min[2]] = 1
        colors[cube[0] + min[0] ,cube[1] + min[1],cube[2] + min[2]] = np.array([i/27, i/27, i/27])
        # combine

    # and plot everything
    ax = plt.figure().add_subplot(projection='3d')
        
    ax.voxels(tensor, edgecolor='k', facecolors=colors)

    plt.show()
