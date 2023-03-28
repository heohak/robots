"""EX06 - Object Detection."""
import math
import statistics
import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Class constructor."""
        self.front_laser_start = None
        self.right_laser_start = None
        self.left_laser_start = None
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
        self.right_wheel = 0
        self.left_wheel = 0
        self.is_stopped_right = False
        self.check_left = False
        self.is_stopped = False
        self.stopp = False
        self.front_laser = 0
        self.right_laser = 0
        self.left_laser = 0
        self.state = "search"

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def get_angle(self):
        """Get Robot angle."""
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
                if self.get_front_middle_laser() > 0.5:
                    self.end = self.get_angle()
                    self.objects.append((self.start + self.end) / 2)
                    self.check = False
                    print('new check')
            if self.get_front_middle_laser() < 0.5 and not self.check:
                if (self.front_laser_start - self.front_laser) > 0.2:
                    self.start = self.get_angle()
                    self.check = True
        # return self.objects

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
        print('sense')
        self.front_laser_start = self.front_laser
        self.left_laser_start = self.left_laser
        self.right_laser_start = self.right_laser
        self.left_encoder = self.robot.get_left_wheel_encoder()
        self.right_encoder = self.robot.get_right_wheel_encoder()
        self.front_laser = self.robot.get_front_middle_laser()
        self.right_laser = self.robot.get_front_right_laser()
        self.left_laser = self.robot.get_front_left_laser()
        print(f"Front: {self.front_laser}")
        print(f"Left: {self.left_laser}")
        print(f"Right: {self.right_laser}")
        self.values.append(self.front_laser)
        if len(self.values) == 6:
            self.values.pop(0)

    def plan(self):
        """Plan action."""
        print('plan')
        if self.check is False and self.state == "search":
            self.left_wheel = -6
            self.right_wheel = 6
            self.get_objects()
        if self.check is True:
            print("OBJECT DETECTED")
            self.state = "drive"
            self.right_wheel = 0
            self.left_wheel = 0
        if self.state == "drive":
            self.right_wheel = 10
            self.left_wheel = 10
            if self.front_laser < 0.1:
                self.right_wheel = 0
                self.left_wheel = 0
                self.state = "stop"

    def act(self):
        """Act according to plan."""
        print('act')
        self.robot.set_right_wheel_speed(self.right_wheel)
        self.robot.set_left_wheel_speed(self.left_wheel)

    def spin(self):
        """Initialize the main loop."""
        while not self.shutdown:
            print('running')
            self.sense()
            self.plan()
            self.act()
            self.robot.sleep(0.05)


def main():
    """Initialize main entry."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()