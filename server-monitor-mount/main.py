from solid import *
from solid.utils import *
from subprocess import run
from dotenv import dotenv_values

config = dotenv_values("../.env")

HOLE_COLOR = "blue"
MOUNT_COLOR = "green"
MOUNT_EXTENSION_COLOR = "red"

MONITOR_LENGTH = 412
SHELF_LENGTH = 435

MOUNT_EXTENSION_LENGTH = (SHELF_LENGTH - MONITOR_LENGTH) / 2

MOUNT_THICKNESS = 2
MOUNT_LENGTH = 22
MOUNT_HEIGHT = 90

HOLE_SIZE = 7


def frame():
    pass


def mount():
    mount_point = rotate(90, (0, -1, 0))(
        color(MOUNT_COLOR, 1)(
            cube([MOUNT_HEIGHT, MOUNT_LENGTH, MOUNT_THICKNESS])
        )
    )

    mount_extension = translate((0, MOUNT_LENGTH, 0))(
        rotate(90, (0, -1, 0))(
            color(MOUNT_EXTENSION_COLOR, 1)(
                cube([MOUNT_HEIGHT, MOUNT_EXTENSION_LENGTH, MOUNT_THICKNESS])
            )
        )
    )

    mounting_frame = union()(
        mount_point, mount_extension
    )

    # 0.625 = 15.875
    # 1.25 = 31.75
    # 0.5 = 12.7

    hole_1_center = (MOUNT_HEIGHT - (3 + 5))
    hole_2_center = hole_1_center - 31.8
    hole_3_center = hole_2_center - 12.7
    hole_4_center = hole_3_center - 31.8

    holes = []
    hole_centers = [hole_1_center, hole_2_center, hole_3_center, hole_4_center]

    for hole_center in hole_centers:
        hole = translate((-MOUNT_THICKNESS / 2, 7.95, hole_center))(
            color(HOLE_COLOR, 1)(
                sphere(HOLE_SIZE / 2)
            )
        )
        holes.append(hole)

    for hole in holes:
        mounting_frame = difference()(
            mounting_frame, hole
        )

    return mounting_frame


def main():
    model = mount()

    print(scad_render(model))
    scad_render_to_file(model, "server-monitor-mount.scad")
    run([config.get("OPENSCAD"), "-o", "server-monitor-mount.stl", "server-monitor-mount.scad"])


if __name__ == '__main__':
    main()
