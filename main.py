import numpy as np
from scipy.misc import imread
import argparse
import mesh
import utils
import matplotlib.pyplot as plt
import resize
from matplotlib.image import AxesImage


def get_meshfile_from_image(filename):
    s = filename.split('.')
    s[-1] = 'mesh'

    return '.'.join(s)

def get_subject_from_file(filename):
    s = filename.split('.')
    return s[-2]

if __name__ == "__main__":
    """
    -i1 <image file 1> : input image file 1
    -i2 <image file 2> : input image file 2
    -n <integer> : number of result, default 5
    -sh : show mesh, not show images
    -sf : save output image files
    -sm : save mesh files
    """
    parser = argparse.ArgumentParser(description='Morph two pictures together')
    parser.add_argument('-i1', dest='file1', required=True, help='filename for first image')
    parser.add_argument('-i2', dest='file2', required=True, help='filename for second image')
    parser.add_argument('-n', dest='num_internal', default=5,
            type=int, help='number of interior points for the morph')
    parser.add_argument('-sh', dest='show', action='store_const',
        const=True, default=False, help='Show the mesh on the plots')
    parser.add_argument('-sf', dest='save_files', action='store_const',
        const=True, default=False, help='Show images of the plots/meshes')
    parser.add_argument('-sm', dest='save_mesh', action='store_const',
        const=True, default=False, help='Show images of the plots/meshes')

    args = parser.parse_args()

    utils.save_files = args.save_files

    width = 500
    height = 500

    resize.resize(args.file1, 'mid_product_1.png', width, height)
    im1 = imread('mid_product_1.png', mode='RGBA')
    mesh1 = mesh.load_mesh('mid_product_1.png', width, height)

    resize.resize(args.file2, 'mid_product_2.png', width, height)
    im2 = imread('mid_product_2.png', mode='RGBA')
    mesh2 = mesh.load_mesh('mid_product_2.png', width, height)

    plt.close('all')

    interpolations = mesh.animate_image_interpolation(im1, im2, mesh1, mesh2, args.num_internal)

    i_file = get_subject_from_file(args.file1) + '_' + get_subject_from_file(args.file2)

    name_index = [str(i+1) for i in range(args.num_internal + 2)]

    for interp in interpolations:
        i, m, a = interp['image'], interp['mesh'], interp['alpha']
        points = m.points if args.show is False else np.empty((0,2))
        a = "{:.2f}".format(a).replace('.','_')
        if args.show:
            mesh.plot_mesh(args.save_mesh, m, filename='{}_{}_mesh.png'.format(i_file, a))
        else:
            fig = plt.figure()
            fig_show = fig.add_subplot(111)
            img = fig_show.imshow(i)
            fig.show()
            input("press any key to continue")
            plt.close()
        if args.save_files:
            plt.imsave('out' + name_index.pop() + '.png', i)
