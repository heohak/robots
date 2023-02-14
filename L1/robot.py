"""L1 aka Line Tracking."""
import PiBot


class Robot:
    """The robot class."""

    def __init__(self):
        """Class initialization."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.sensors = [0, 0, 0, 0, 0, 0]
        self.sensors_tof = []
        self.line_value = 0
        self.last_value = 0
        self.right_wheel = 0
        self.left_wheel = 0
        self.turn_around_check = [0]

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set robot reference."""
        self.robot = robot

    def get_all_sensors(self):
        """Get all sensors info."""
        return [self.robot.get_leftmost_line_sensor(), self.robot.get_second_line_sensor_from_left(),
                self.robot.get_third_line_sensor_from_left(), self.robot.get_third_line_sensor_from_right(),
                self.robot.get_second_line_sensor_from_right(), self.robot.get_rightmost_line_sensor()]

    def get_line_direction(self):
        """
        Return the direction of the line based on sensor readings.

        Returns:
          -1: Line is on the right (i.e., the robot should turn right to reach the line again)
           0: Robot is on the line (i.e., the robot should not turn to stay on the line) or no sensor info
           1: Line is on the left (i.e., the robot should turn left to reach the line again)
        """
        self.sensors_tof = []
        for i in self.sensors:
            if i <= 400:
                self.sensors_tof.append(True)
            else:
                self.sensors_tof.append(False)
        tof_values = self.sensors_tof
        if len(self.turn_around_check) > 6:
            self.turn_around_check = self.turn_around_check[0:6]
            if self.turn_around_check == [0, 0, 0, 0, 0, 0]:
                return 2
        elif tof_values == [True, False, False, False, False, False] or tof_values == [True, True, False, False, False, False] or tof_values == [False, True, False, False, False, False]:
            self.last_value = 1
            print("Value is " + str(self.last_value))
            self.turn_around_check.insert(0, self.last_value)
            return 1
        elif tof_values == [False, False, True, True, False, False] or tof_values == [False, False, True, False, False, False] or tof_values == [False, False, False, True, False, False] or tof_values == [False, True, True, False, False, False] or tof_values == [False, False, False, True, True, False] or tof_values == [True, True, True, False, False, False] or tof_values == [False, False, False, True, True, True]:
            self.last_value = 0
            print("Value is " + str(self.last_value))
            self.turn_around_check.insert(0, self.last_value)
            return 0
        elif tof_values == [False, False, False, False, False, True] or tof_values == [False, False, False, False, True, True] or tof_values == [False, False, False, False, True, False]:
            self.last_value = -1
            print("Value is " + str(self.last_value))
            self.turn_around_check.insert(0, self.last_value)
            return -1
        else:
            print("Value is " + str(self.last_value))
            self.turn_around_check.insert(0, self.last_value)
            return self.last_value

    def sense(self):
        """Sense method."""
        self.sensors = self.get_all_sensors()
        self.line_value = self.get_line_direction()

    def plan(self):
        """Plan method."""
        if self.line_value == 0:
            self.left_wheel = 10
            self.right_wheel = 10

        elif self.line_value == 1:
            self.left_wheel = 0
            self.right_wheel = 10

        elif self.line_value == -1:
            self.left_wheel = 10
            self.right_wheel = 0

        elif self.line_value == 2:
            self.left_wheel = -10
            self.right_wheel = 10

    def act(self):
        """Act method."""
        self.robot.set_left_wheel_speed(self.left_wheel)
        self.robot.set_right_wheel_speed(self.right_wheel)

    def spin(self):
        """Make main spin loop."""
        while not self.shutdown:
            self.sense()
            self.plan()
            self.act()
            timestamp = self.robot.get_time()
            print(f'timestamp is {timestamp}')
            self.robot.sleep(0.05)


def main():
    """Initialize main."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
