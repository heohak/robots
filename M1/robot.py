"""Maze - Bronze."""
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

        self.last_turn = "forward"

        self.is_first = True

        self.turning = None
        self.state = "forward"

        self.left_rear_side = 0
        self.right_rear_side = 0
        self.left_side_previous = 0
        self.right_side_previous = 0

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def sense(self):
        """Sense method according to the SPA architecture."""
        self.left_rear_side = self.robot.get_rear_left_side_ir()
        self.right_rear_side = self.robot.get_rear_right_side_ir()
        self.left_rear_str = self.robot.get_rear_left_straight_ir()
        self.right_rear_str = self.robot.get_rear_right_straight_ir()
        self.rotation = self.robot.get_rotation()
        if self.is_first:
            self.right_side_previous = self.right_rear_side
            self.left_side_previous = self.left_rear_side
            self.left_rear_side_begin = self.left_rear_side
            self.right_rear_side_begin = self.right_rear_side
            self.is_first = False

    def plan(self):
        """Plan the robot's actions based on its current state."""
        if self.state == "forward":
            self.handle_forward_state()
        elif self.state == "turn_left":
            self.handle_turn_left_state()
        elif self.state == "turn_right":
            self.handle_turn_right_state()

    def handle_forward_state(self):
        """Handle the robot's actions when it is in the "forward" state."""
        if abs(self.left_rear_side - self.left_rear_side_begin) > 30 and self.left_rear_side > self.right_rear_side:
            print("num1")
            self.left_wheel_speed = -10
            self.right_wheel_speed = -9
        elif abs(self.right_rear_side - self.right_rear_side_begin) > 30 and self.right_rear_side > self.left_rear_side:
            print("num2")
            self.left_wheel_speed = -9
            self.right_wheel_speed = -10
        else:
            self.adjust_rotation_based_on_last_turn()

        self.check_and_prepare_for_turns()

    def adjust_rotation_based_on_last_turn(self):
        """Adjust the robot's rotation based on its last turn direction."""
        if self.last_turn == "left":
            if self.rotation > 177:
                self.left_wheel_speed = 8
                self.right_wheel_speed = -8
            elif self.rotation < 174:
                self.left_wheel_speed = -8
                self.right_wheel_speed = 8
        elif self.last_turn == "right":
            if self.rotation > 3:
                self.left_wheel_speed = 8
                self.right_wheel_speed = -8
            elif self.rotation < 0:
                self.left_wheel_speed = -8
                self.right_wheel_speed = 8
        else:
            self.left_wheel_speed = -10
            self.right_wheel_speed = -10

    def check_and_prepare_for_turns(self):
        """Check if the robot needs to turn, and prepare for turning if needed."""
        if abs(self.right_rear_side - self.right_side_previous) >= 200:
            self.prepare_for_turn("turn_left")
        elif abs(self.left_rear_side - self.left_side_previous) >= 200:
            self.prepare_for_turn("turn_right")
        else:
            self.right_side_previous = self.right_rear_side
            self.left_side_previous = self.left_rear_side

    def prepare_for_turn(self, turn_state):
        """
        Prepare the robot for turning by updating its state and wheel speeds.

        Args:
            turn_state (str): The state to change to for turning ("turn_left" or "turn_right").
        """
        self.left_wheel_speed = 0
        self.right_wheel_speed = 0
        self.left_rear_str_previous = self.left_rear_str
        self.right_rear_str_previous = self.right_rear_str
        self.state = turn_state

    def handle_turn_left_state(self):
        """Handle the robot's actions when it is in the "turn_left" state."""
        self.left_wheel_speed = -9
        self.right_wheel_speed = -8
        if self.rotation > 175:
            self.last_turn = "left"
            self.state = "forward"

    def handle_turn_right_state(self):
        """Handle the robot's actions when it is in the "turn_right" state."""
        self.left_wheel_speed = -8
        self.right_wheel_speed = -9
        if self.rotation < 5:
            self.last_turn = "right"
            self.state = "forward"

    def act(self):
        """Act robot."""
        self.robot.set_left_wheel_speed(self.left_wheel_speed)
        self.robot.set_right_wheel_speed(self.right_wheel_speed)

    def spin(self):
        """Create the main loop."""
        while not self.shutdown:
            self.sense()
            self.plan()
            self.act()
            self.robot.sleep(0.05)


robot = Robot()
robot.spin()
