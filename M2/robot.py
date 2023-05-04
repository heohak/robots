"""M2 - Maze."""
import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.right_wheel_speed = 0
        self.left_wheel_speed = 0
        self.left_straight_ir = 0
        self.left_diagonal_ir = 0
        self.left_side_ir = 0
        self.right_side_ir = 0
        self.right_diagonal_ir = 0
        self.right_straight_ir = 0
        self.last_turn = ""

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def sense(self):
        """Sense method according to the SPA architecture."""
        self.left_straight_ir = self.robot.get_rear_left_straight_ir()
        self.left_diagonal_ir = self.robot.get_rear_left_diagonal_ir()
        self.left_side_ir = self.robot.get_rear_left_side_ir()
        self.right_straight_ir = self.robot.get_rear_right_straight_ir()
        self.right_diagonal_ir = self.robot.get_rear_right_diagonal_ir()
        self.right_side_ir = self.robot.get_rear_right_side_ir()

    def plan(self):
        """Plan action."""
        if self.right_side_ir > 550 and self.left_side_ir > 550:
            self.right_wheel_speed = -10
            self.left_wheel_speed = -10
        elif self.left_side_ir > 600 and self.left_diagonal_ir > 500:
            self.right_wheel_speed = 10
            self.left_wheel_speed = -20
            self.last_turn = "right"
        elif 600 < self.right_side_ir and 500 < self.right_diagonal_ir:
            self.right_wheel_speed = -20
            self.left_wheel_speed = 10
            self.last_turn = "left"
        elif self.left_side_ir < 500 and self.last_turn == "right":
            self.right_wheel_speed = -50
            self.left_wheel_speed = 10
        elif self.right_side_ir < 500 and self.last_turn == "left":
            self.right_wheel_speed = 10
            self.left_wheel_speed = -50
        elif self.left_straight_ir > 600 and self.right_straight_ir > 600:
            self.right_wheel_speed = -50
            self.left_wheel_speed = 50
        else:
            self.right_wheel_speed = -10
            self.left_wheel_speed = -10

        if self.left_side_ir < 400 and self.left_diagonal_ir < 400 and self.left_straight_ir < 400 and\
                self.right_straight_ir < 400 and self.right_diagonal_ir < 400 and self. right_side_ir < 400:
            self.right_wheel_speed = 0
            self.left_wheel_speed = 0

    def act(self):
        """Act according to plan."""
        print('act')
        self.robot.set_right_wheel_speed(self.right_wheel_speed)
        self.robot.set_left_wheel_speed(self.left_wheel_speed)

    def spin(self):
        """Initialize the main loop."""
        while not self.shutdown:
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
