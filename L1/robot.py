"""EX04 - Line tracking."""
import PiBot


class Robot:
    """The robot class."""

    def __init__(self):
        """Class initialization."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.value = 0
        self.sense_list = []
        self.all_sensors_list_tof = []

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set robot reference."""
        self.robot = robot

    def get_all_sensors(self):
        """Get all sensors info."""
        return [self.robot.get_leftmost_line_sensor(), self.robot.get_second_line_sensor_from_left(), self.robot.get_third_line_sensor_from_left(), self.robot.get_third_line_sensor_from_right(), self.robot.get_second_line_sensor_from_right(), self.robot.get_rightmost_line_sensor()]

    def sense(self):
        """Sense method as per SPA architecture."""
        self.sense_list = self.get_all_sensors()

    def get_line_direction(self):
        """
        Return the direction of the line based on sensor readings.

        Returns:
          -1: Line is on the right (i.e., the robot should turn right to reach the line again)
           0: Robot is on the line (i.e., the robot should not turn to stay on the line) or no sensor info
           1: Line is on the left (i.e., the robot should turn left to reach the line again)
        """
        self.all_sensors_list_tof = []
        for i in self.sense_list:
            if i <= 400:
                self.all_sensors_list_tof.append(True)
            else:
                self.all_sensors_list_tof.append(False)
        tof_values = self.all_sensors_list_tof
        """Find all cases."""
        if tof_values == [True, False, False, False, False, False] or tof_values == [True, True, False, False, False, False] or tof_values == [False, True, False, False, False, False]:
            self.value = 1
            return 1
        elif tof_values == [False, False, True, True, False, False] or tof_values == [False, False, True, False, False, False] or tof_values == [False, False, False, True, False, False] or tof_values == [False, True, True, False, False, False] or tof_values == [False, False, False, True, True, False] or tof_values == [True, True, True, False, False, False] or tof_values == [False, False, False, True, True, True]:
            self.value = 0
            return 0
        elif tof_values == [False, False, False, False, False, True] or tof_values == [False, False, False, False, True, True] or tof_values == [False, False, False, False, True, False]:
            self.value = -1
            return -1
        else:
            return self.value

    def act(self):
        if self.get_line_direction() == 0:
            self.robot.set_wheels_speed(10)
        elif self.get_line_direction() == 1:
            self.robot.set_left_wheel_speed(-10)
            self.robot.set_right_wheel_speed(10)
        elif self.get_line_direction() == -1:
            self.robot.set_left_wheel_speed(10)
            self.robot.set_right_wheel_speed(-10)







    def spin(self):
        """Make main spin loop."""
        while not self.shutdown:
            self.sense()
            self.get_line_direction()
            self.act()
            timestamp = self.robot.get_time()
            print(f'timestamp is {timestamp}')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


