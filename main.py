import numpy as np
import argparse
import mesh
import image
import utils
import matplotlib.pyplot as plt


def get_meshfile_from_image(filename):
    s = filename.split('.')
    s[-1] = 'mesh'

    return '.'.join(s)

def get_subject_from_file(filename):
    s = filename.split('.')
    return s[-2]

def main():
    parser = argparse.ArgumentParser(description='Morph two pictures together')
    parser.add_argument('-i1', dest='file1', required=True, help='filename for first image')
    parser.add_argument('-i2', dest='file2', required=True, help='filename for second image')
    parser.add_argument('--internal-points', dest='num_internal', default=5,
            type=int, help='number of interior points for the morph')

    parser.add_argument('--show-mesh', dest='show_mesh', action='store_const',
        const=True, default=False, help='Show the mesh on the plots')

    parser.add_argument('-s', dest='save_files', action='store_const',
        const=True, default=False, help='Save images of the plots/meshes')

    parser.add_argument('--update-mesh', dest='update_mesh', action='store_const',
        const=True, default=False, help='Update existing meshes if they exist')

    args = parser.parse_args()

    utils.save_files = args.save_files

    im1 = image.load_image(args.file1)
    mesh1 = mesh.load_mesh(args.file1)

    im2 = image.load_image(args.file2)
    mesh2 = mesh.load_mesh(args.file2)

    plt.close('all')

    interpolations = mesh.animate_image_interpolation(im1, im2, mesh1, mesh2, args.num_internal)

    i_file = get_subject_from_file(args.file1) + '_' + get_subject_from_file(args.file2)
    for interp in interpolations:
        i, m, a = interp['image'], interp['mesh'], interp['alpha']
        points = m.points if args.show_mesh else np.empty((0,2))
        a = "{:.2f}".format(a).replace('.','_')
        if args.show_mesh:
            mesh.plot_mesh(m, filename='{}_{}_mesh.png'.format(i_file, a))

        image.pick_points(i, points, close_fig=True, filename='{}_{}.png'.format(i_file, a))

    return

if __name__ == "__main__":
    main()
