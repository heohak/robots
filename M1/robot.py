"""EX06 - Object Detection."""
import PiBot


class Robot:
    """Robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.right_encoder = 0
        self.left_encoder = 0
        self.right_wheel = 0
        self.left_wheel = 0
        self.state = "search"
        self.ir_values = []
        self.left_straight = 0
        self.left_diagonal = 0
        self.left_side = 0
        self.right_side = 0
        self.right_diagonal = 0
        self.right_straight = 0
        self.last_turn = ''

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def sense(self):
        """Sense method according to the SPA architecture."""
        print('sense')
        self.left_encoder = self.robot.get_left_wheel_encoder()
        self.right_encoder = self.robot.get_right_wheel_encoder()
        self.ir_values = self.robot.get_rear_irs()
        self.left_straight = self.robot.get_rear_left_straight_ir()
        self.left_diagonal = self.robot.get_rear_left_diagonal_ir()
        self.left_side = self.robot.get_rear_left_side_ir()
        self.right_straight = self.robot.get_rear_right_straight_ir()
        self.right_diagonal = self.robot.get_rear_right_diagonal_ir()
        self.right_side = self.robot.get_rear_right_side_ir()

    def plan(self):
        """Plan action."""
        print('plan')
        print('-------------------')
        print(f'left side: {self.left_side}')
        print(f'left diagonal: {self.left_diagonal}')
        print(f'left straight: {self.left_straight}')
        print(f'right straight: {self.right_straight}')
        print(f'right diagonal: {self.right_diagonal}')
        print(f'right side: {self.right_side}')
        print('-------------------')
        if self.right_side > 550 and self.left_side > 550:
            self.right_wheel = -10
            self.left_wheel = -10
        elif self.left_side > 600 and self.left_diagonal > 500:
            self.right_wheel = 10
            self.left_wheel = -20
            self.last_turn = 'right'
        elif 600 < self.right_side and 500 < self.right_diagonal:
            self.right_wheel = -20
            self.left_wheel = 10
            self.last_turn = "left"
        elif self.left_side < 500 and self.last_turn == 'right':
            self.right_wheel = -50
            self.left_wheel = 10
        elif self.right_side < 500 and self.last_turn == 'left':
            self.right_wheel = 10
            self.left_wheel = -50
        else:
            self.right_wheel = -10
            self.left_wheel = -10

        # elif self.left_side < 600 and self.right_side < 600:
        #     if self.last_turn == 'right':
        #         self.right_wheel = 10
        #         self.left_wheel = -50
        #         print('turning right')
        #     elif self.last_turn == 'left':
        #         self.right_wheel = -50
        #         self.left_wheel = 10
        #         print('turning left')

        # shutdown
        # if all(i < 500 for i in self.ir_values):
        #     self.right_wheel = 0
        #     self.left_wheel = 0

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