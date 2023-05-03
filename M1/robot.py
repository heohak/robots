"""Maze - Bronze."""
import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.shutdown = False

        self.right_enc = 0
        self.left_enc = 0
        self.right_motor = 0
        self.left_motor = 0

        self.ir_values = []
        self.left_forward = 0
        self.left_diag = 0
        self.left_lateral = 0
        self.right_lateral = 0
        self.right_diag = 0
        self.right_forward = 0

        self.state = "search"
        self.last_turn = ''

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def sense(self):
        """Sense block."""
        print('sense')
        self.left_enc = self.robot.get_left_wheel_encoder()
        self.right_enc = self.robot.get_right_wheel_encoder()

        self.ir_values = self.robot.get_rear_irs()
        self.left_forward = self.robot.get_rear_left_straight_ir()
        self.left_diag = self.robot.get_rear_left_diagonal_ir()
        self.left_lateral = self.robot.get_rear_left_side_ir()
        self.right_forward = self.robot.get_rear_right_straight_ir()
        self.right_diag = self.robot.get_rear_right_diagonal_ir()
        self.right_lateral = self.robot.get_rear_right_side_ir()

    def plan(self):
        """Plan block."""
        print('plan')
        if self.right_lateral > 550 and self.left_lateral > 550:
            self.right_motor = -10
            self.left_motor = -10
        elif self.left_lateral > 600 and self.left_diag > 500:
            self.right_motor = 10
            self.left_motor = -20
            self.last_turn = 'right'
        elif 600 < self.right_lateral and 500 < self.right_diag:
            self.right_motor = -20
            self.left_motor = 10
            self.last_turn = "left"
        elif self.left_lateral < 500 and self.last_turn == 'right':
            self.right_motor = -50
            self.left_motor = 10
        elif self.right_lateral < 500 and self.last_turn == 'left':
            self.right_motor = 10
            self.left_motor = -50
        else:
            self.right_motor = -10
            self.left_motor = -10

    def act(self):
        """Act block."""
        print('act')
        self.robot.set_right_wheel_speed(self.right_motor)
        self.robot.set_left_wheel_speed(self.left_motor)

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
