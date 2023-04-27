"""EX06 - Object Detection."""
import statistics

import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()

        self.shutdown = False

        self.left_wheel_speed = 0
        self.right_wheel_speed = 0

        self.left_rear_str = 0
        self.right_rear_str = 0

        self.right_register = 0

        self.left_rear_str_previous = 0
        self.right_rear_str_previous = 0

        self.left_rear_side_begin = 0
        self.right_rear_side_begin = 0

        self.rotation = 0
        self.rotation_previous = 0

        self.last_turn = "left"

        self.is_first = True

        self.turning = None
        self.state = "forward"

        self.left_rear_side = 0
        self.right_rear_side = 0
        self.left_side_previous = 0
        self.right_side_previous = 0

        self.medians_list_l = []
        self.data_l = []

        self.medians_list_r = []
        self.data_r = []

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def get_right_laser(self):
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        if self.right_rear_side:
            if len(self.data_r) < 7:
                self.data_r.append(self.right_rear_side)
            else:
                self.data_r.pop(0)
                self.data_r.append(self.right_rear_side)

    def get_left_laser(self):
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        if self.left_rear_side:
            if len(self.data_l) < 7:
                self.data_l.append(self.left_rear_side)
            else:
                self.data_l.pop(0)
                self.data_l.append(self.left_rear_side)

    def sense(self):
        """Sense method according to the SPA architecture."""
        self.left_rear_side = self.robot.get_rear_left_side_ir()
        self.right_rear_side = self.robot.get_rear_right_side_ir()
        self.left_rear_str = self.robot.get_rear_left_straight_ir()
        self.right_rear_str = self.robot.get_rear_right_straight_ir()
        self.rotation = self.robot.get_rotation()

        self.get_right_laser()
        self.get_left_laser()
        if self.is_first:
            self.right_side_previous = self.right_rear_side
            self.left_side_previous = self.left_rear_side
            self.left_rear_side_begin = self.left_rear_side
            self.right_rear_side_begin = self.right_rear_side
            self.is_first = False

    def plan(self):
        """Plan robot."""
        if self.state == "forward":
            self.left_wheel_speed = -10
            self.right_wheel_speed = -10
            if abs(self.left_rear_side - self.left_rear_side_begin) > 30 and self.left_rear_side > self.right_rear_side:
                print("num1")
                self.left_wheel_speed = -10
                self.right_wheel_speed = -9
            elif abs(self.right_rear_side - self.right_rear_side_begin) > 30 and self.right_rear_side > self.left_rear_side:
                print("num2")
                self.left_wheel_speed = -9
                self.right_wheel_speed = -10
            else:
                if self.last_turn == "left":
                    if self.rotation > 3:
                        self.left_wheel_speed = 8
                        self.right_wheel_speed = -8
                    elif self.rotation < 0:
                        self.left_wheel_speed = -8
                        self.right_wheel_speed = 8
                elif self.last_turn == "right":
                    if self.rotation > -177:
                        self.left_wheel_speed = 8
                        self.right_wheel_speed = -8
                    elif self.rotation < -180:
                        self.left_wheel_speed = -8
                        self.right_wheel_speed = 8
        self.plan2()

    def plan2(self):
        """Create plan 2."""
        if self.state == "forward":
            if statistics.median(self.data_r) < 300 and statistics.median(self.data_l) < 400:
                self.left_wheel_speed = 0
                self.right_wheel_speed = 0
                self.shutdown = True
            elif statistics.median(self.data_r) < 300:
                self.left_wheel_speed = 0
                self.right_wheel_speed = 0
                self.left_rear_str_previous = self.left_rear_str
                self.right_rear_str_previous = self.right_rear_str
                self.state = "turn_left"
            elif statistics.median(self.data_l) < 400:
                self.left_wheel_speed = 0
                self.right_wheel_speed = 0
                self.left_rear_str_previous = self.left_rear_str
                self.right_rear_str_previous = self.right_rear_str
                self.state = "turn_right"
            else:
                self.right_side_previous = self.right_rear_side
                self.left_side_previous = self.left_rear_side
        elif self.state == "turn_left":
            self.left_wheel_speed = -99
            self.right_wheel_speed = -6
            if self.rotation > 5:
                self.left_wheel_speed = 0
                self.right_wheel_speed = 0
                self.data_l = []
                self.last_turn = "left"
                self.state = "forward"
        elif self.state == "turn_right":
            self.left_wheel_speed = -16
            self.right_wheel_speed = -99
            if self.rotation < -185:
                self.left_wheel_speed = 0
                self.right_wheel_speed = 0
                self.data_r = []
                self.last_turn = "right"
                self.state = "forward"

    def act(self):
        """Act robot."""
        self.robot.set_left_wheel_speed(self.left_wheel_speed)
        self.robot.set_right_wheel_speed(self.right_wheel_speed)

    def spin(self):
        """Create the main loop."""
        while not self.shutdown:
            print(abs(self.right_rear_side - self.right_rear_side_begin))
            print(abs(self.left_rear_side - self.left_rear_side_begin))
            print(self.rotation)
            print(self.state)
            self.sense()
            self.plan()
            self.act()
            self.robot.sleep(0.05)


robot = Robot()
robot.spin()