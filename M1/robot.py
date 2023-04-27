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

        self.can_turn_left = True
        self.can_turn_right = False

        self.state = "forward"

        self.left_rear_side = 0
        self.right_rear_side = 0
        self.left_side_previous = 0
        self.right_side_previous = 0

        self.medians_list_l = []
        self.data_l = []

        self.medians_list_r = []
        self.data_r = []

        self.medians_list_front_r = []
        self.medians_list_front_l = []

        self.data_front_r = []
        self.data_front_l = []

        self.count = 0

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def get_right_front(self):
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        if self.right_rear_str:
            if len(self.data_front_r) < 7:
                self.data_front_r.append(self.right_rear_str)
            else:
                self.data_front_r.pop(0)
                self.data_front_r.append(self.right_rear_str)

    def get_left_front(self):
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        if self.left_rear_str:
            if len(self.data_front_l) < 7:
                self.data_front_l.append(self.left_rear_str)
            else:
                self.data_front_l.pop(0)
                self.data_front_l.append(self.left_rear_str)

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

        self.get_right_front()
        self.get_left_front()

        if self.is_first:
            self.right_side_previous = self.right_rear_side
            self.left_side_previous = self.left_rear_side
            self.left_rear_side_begin = self.left_rear_side
            self.right_rear_side_begin = self.right_rear_side
            self.is_first = False

    def plan(self):
        """Plan robot."""
        if self.state == "forward":
            self.forward()
        elif self.state == "drive_towards_wall_left":
            self.drive_towards_wall_left()
        elif self.state == "drive_towards_wall_right":
            self.drive_towards_wall_right()
        elif self.state == "turn_left":
            self.turn_left()
        elif self.state == "turn_right":
            self.turn_right()
        elif self.state == "forward_until_between_walls":
            self.forward_until_between_walls()

    def adjust_left(self):
        """Adjust after left turn."""
        if self.rotation > 3:
            self.left_wheel_speed = 8
            self.right_wheel_speed = -8
        elif self.rotation < 0:
            self.left_wheel_speed = -8
            self.right_wheel_speed = 8

    def adjust_right(self):
        """Adjust after right turn."""

    def forward(self):
        """State forward."""
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
                self.adjust_left()
            elif self.last_turn == "right":
                self.adjust_right()
        if statistics.median(self.data_r) < 400 and statistics.median(self.data_l) < 400:
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.shutdown = True
        elif statistics.median(self.data_r) < 300 and self.can_turn_left:  # ORIGINAALIS 300
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.state = "drive_towards_wall_left"
        elif statistics.median(self.data_l) < 400 and self.can_turn_right:
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.state = "drive_towards_wall_right"
        else:
            self.right_side_previous = self.right_rear_side
            self.left_side_previous = self.left_rear_side

    def drive_towards_wall_left(self):
        """Drive towards back wall."""
        if statistics.median(self.data_front_r) > 500 and statistics.median(
                self.data_front_l) > 500:  # OTSI NEED NUMBRID ÜLES ÕIGEL ROBOTIL
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.rotation_previous = self.rotation
            self.state = "turn_left"
        else:
            self.left_wheel_speed = -10
            self.right_wheel_speed = -10

    def turn_left(self):
        """Turn left."""
        if abs(self.rotation - self.rotation_previous) >= 88 and self.count == 0:
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.data_front_l = []
            self.data_front_r = []
            self.data_l = []
            self.state = "drive_towards_wall_left"
            self.count = 1
        elif abs(self.rotation - self.rotation_previous) >= 88 and self.count == 1:
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.data_l = []
            self.data_front_l = []
            self.data_front_r = []
            self.count = 0
            self.state = "forward_until_between_walls"
            self.last_turn = "left"
            self.can_turn_left = False
            self.can_turn_right = True
        else:
            self.left_wheel_speed = -8
            self.right_wheel_speed = 8

    def drive_towards_wall_right(self):
        """Drive towards back wall."""
        if statistics.median(self.data_front_r) > 500 and statistics.median(
                self.data_front_l) > 500:  # OTSI NEED NUMBRID ÜLES ÕIGEL ROBOTIL
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.rotation_previous = self.rotation
            self.state = "turn_right"
        else:
            self.left_wheel_speed = -10
            self.right_wheel_speed = -10

    def turn_right(self):
        """Turn right."""
        if abs(self.rotation - self.rotation_previous) >= 88 and self.count == 0:
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.data_front_l = []
            self.data_front_r = []
            self.data_l = []
            self.state = "drive_towards_wall_right"
            self.count = 1
        elif abs(self.rotation - self.rotation_previous) >= 88 and self.count == 1:
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
            self.data_l = []
            self.data_front_l = []
            self.data_front_r = []
            self.count = 0
            self.state = "forward_until_between_walls"
            self.last_turn = "right"
            self.can_turn_right = False
            self.can_turn_left = True
        else:
            self.left_wheel_speed = 8
            self.right_wheel_speed = -8

    def forward_until_between_walls(self):
        """Drive forward until robot between walls."""
        if statistics.median(self.data_r) > 500 and statistics.median(self.data_l) > 500:  # NEED NUMBRID KA
            self.state = "forward"
        self.left_wheel_speed = -10
        self.right_wheel_speed = -10

    def act(self):
        """Act robot."""
        self.robot.set_left_wheel_speed(self.left_wheel_speed)
        self.robot.set_right_wheel_speed(self.right_wheel_speed)

    def spin(self):
        """Create the main loop."""
        while not self.shutdown:
            print(f"right_rear: {abs(self.right_rear_side)}")
            print(f"left rear: {abs(self.left_rear_side)}")
            print(f"tagumine otse: {self.right_rear_str}")  # TAGUMINE OTSE
            print(f"tagumine otse: {self.left_rear_str}")  # TAGUMINE OTSE
           # print(self.rotation)
           # print(abs(self.rotation % 180))
           # print(self.state)
            self.sense()
            self.plan()
            self.act()
            self.robot.sleep(0.05)


robot = Robot()
robot.spin()