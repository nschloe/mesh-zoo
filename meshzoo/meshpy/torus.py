#!/usr/bin/env python

import argparse
from meshpy.tet import MeshInfo, build
from meshpy.geometry import \
        generate_surface_of_revolution, \
        EXT_OPEN, \
        EXT_CLOSED_IN_RZ, \
        GeometryBuilder
import numpy as np
import time


def _main():

    args = _parse_options()

    big_r = args.bigr
    small_r = args.smallr
    num_points = args.numpoints

    dphi = 2*np.pi / num_points

    # Compute the volume of a canonical tetrahedron
    # with edgelength radius2*dphi.
    a = small_r * dphi
    canonical_tet_volume = np.sqrt(2.0) / 12 * a**3

    radial_subdiv = int(2*np.pi*big_r / a)

    rz = [(big_r + small_r*np.cos(i*dphi), 0.5 * small_r*np.sin(i*dphi))
          for i in xrange(num_points)]

    print 'Build mesh...',
    start = time.time()
    geob = GeometryBuilder()
    geob.add_geometry(
            *generate_surface_of_revolution(
                rz,
                closure=EXT_CLOSED_IN_RZ,
                radial_subdiv=radial_subdiv
                ))
    mesh_info = MeshInfo()
    geob.set(mesh_info)
    meshpy_mesh = build(mesh_info, max_volume=canonical_tet_volume)
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    print('\n%d nodes, %d elements.\n' %
          (len(meshpy_mesh.points), len(meshpy_mesh.elements))
          )

    return


def _parse_options():
    '''Parse input options.'''
    parser = argparse.ArgumentParser(
            description='Construct tetrahedrization of a torus.'
            )

    parser.add_argument(
            'filename',
            metavar='FILE',
            type=str,
            help='file to be written to'
            )

    parser.add_argument(
            '--numpoints', '-n',
            type=int,
            default=10,
            help='number of discretization points along a logitudinal line'
            )

    parser.add_argument(
            '--bigr', '-R',
            type=float,
            default=1.0,
            help='inner radius of the torus (default: 1.0)'
            )

    parser.add_argument(
            '--smallr', '-r',
            type=float,
            default=0.5,
            help='radius of the torus (default: 0.5)'
            )

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    import meshio
    _main()
    # write the mesh
    print 'Write mesh...',
    start = time.time()
    meshio.write(
            args.filename,
            meshpy_mesh.points,
            {'tetra': np.array(meshpy_mesh.elements)}
            )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed