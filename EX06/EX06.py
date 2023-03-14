"""EX06 - Object Detection."""
import math
import statistics
import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.values = []
        self.end = 0
        self.start = 0
        self.objects = []
        self.check = False
        self.angle = 0
        self.right_encoder = 0
        self.left_encoder = 0

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def get_angle(self):
        """Get Robot angles."""
        if self.right_encoder > 0:
            self.angle = math.degrees(self.robot.WHEEL_DIAMETER * self.right_encoder * math.pi / 360 / (self.robot.AXIS_LENGTH / 2))
        elif self.left_encoder > 0:
            self.angle = 360 - math.degrees(self.robot.WHEEL_DIAMETER * self.left_encoder * math.pi / 360 / (self.robot.AXIS_LENGTH / 2))
        return self.angle

    def get_objects(self) -> list:
        """
        Return the list with the detected objects so far.

        (i.e., add new objects to the list as you detect them).

        Returns:
          The list with detected object angles, the angles are in
          degrees [0..360), 0 degrees being the start angle and following
          the right-hand rule (e.g., turning left 90 degrees is 90, turning
          right 90 degrees is 270 degrees).
        """
        if len(self.values) == 5:
            if self.check:
                if self.get_front_middle_laser() > 0.45:
                    self.end = self.get_angle()
                    self.objects.append((self.start + self.end) / 2)
                    self.check = False
            if self.get_front_middle_laser() < 0.45 and not self.check:
                self.start = self.get_angle()
                self.check = True
        return self.objects

    def get_front_middle_laser(self):
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        if not self.values:
            return None
        return statistics.median(self.values)

    def sense(self):
        """Sense method according to the SPA architecture."""
        self.left_encoder = self.robot.get_left_wheel_encoder()
        self.right_encoder = self.robot.get_right_wheel_encoder()
        front_laser = self.robot.get_front_middle_laser()
        self.values.append(front_laser)
        if len(self.values) == 6:
            self.values.pop(0)

    def spin(self):
        """Initialize the main loop."""
        while not self.shutdown:
            self.sense()
            print(f'Value is {self.get_front_middle_laser()}')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


def main():
    """Initialize main entry."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
