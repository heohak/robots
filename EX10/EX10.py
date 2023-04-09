"""EX10 - Robot vision processing."""
import math

import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Initialize variables."""
        self.robot = PiBot.PiBot()
        self.visible_objects = []
        self.cam_resolution = self.robot.CAMERA_RESOLUTION
        self.field_of_view = self.robot.CAMERA_FIELD_OF_VIEW

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set the API reference."""
        self.robot = robot

    def get_closest_visible_object_angle(self):
        """
        Find the closest visible object from the objects list.

        Returns:
          The angle (in radians) to the closest object w.r.t. the robot
          orientation (i.e., 0 is directly ahead) following the right
          hand rule (i.e., objects to the left have a plus sign and
          objects to the right have a minus sign).
          Must return None if no objects are visible.
        """
        if not self.visible_objects:
            return None

        max_radius_obj = max(self.visible_objects, key=lambda obj: obj[2])
        x_coord = max_radius_obj[1][0]

        cam_x_coord = self.cam_resolution[0]
        fov_x_coord = self.field_of_view[0]
        angle = ((cam_x_coord / 2) - x_coord) / cam_x_coord * fov_x_coord

        return math.radians(angle)

    def sense(self):
        """SPA architecture sense block."""
        self.visible_objects = self.robot.get_camera_objects()

    def spin(self):
        """Initialize the spin loop."""
        for _ in range(100):
            self.sense()
            self.robot.sleep(0.05)


def main():
    """Initialize Main entry point."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
