# -*- coding: utf-8 -*-
#
import os
import sys

import meshzoo


def test_ball():
    points, cells = meshzoo.meshpy.ball.create_ball_mesh(10)
    assert len(points) == 1360
    assert len(cells) == 5005
    return


def test_cube():
    points, cells = meshzoo.meshpy.cube.create_cube_mesh(10)
    assert len(points) == 50
    assert len(cells) == 68
    return


def test_ellipse():
    points, cells = meshzoo.meshpy.ellipse.create_ellipse_mesh([0.5, 1], 100)
    assert len(points) == 1444
    assert len(cells) == 2774
    return


if __name__ == '__main__':
    test_ball()