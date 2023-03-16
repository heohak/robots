"""EX07 - Driving in a Straight Line."""
import PiBot


class Robot:
    """The robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.state = ""
        self.left_encoder = 0
        self.right_encoder = 0
        self.left_speed = 0
        self.right_speed = 0
        self.real_left_encoder = 0
        self.real_right_encoder = 0
        self.left_coefficient = 0
        self.right_coefficient = 0



    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set the robot reference."""
        self.robot = robot

    def set_state(self, state: str):
        """
        Set the current state.

        Arguments:
          state - the state as a string.
        """
        # Add code here..
        self.state = state


    def get_state(self) -> str:
        """
        Get the state.

        Returns:
          The state as a string.
        """
        # Add code here...
        return self.state

    def sense(self):
        """The sense method in the SPA architecture."""
        # Add code here...
        self.left_encoder = self.robot.get_left_wheel_encoder()
        self.right_encoder = self.robot.get_right_wheel_encoder()

    def plan(self):
        """The plan method in the SPA architecture."""
        # Add code here...
        if self.state == "calibrate":
            start_time = self.robot.get_time()
            while start_time + 4.0 > self.robot.get_time():
                self.robot.set_left_wheel_speed(8)
                self.robot.set_right_wheel_speed(8)
            real_left_encoder = self.robot.get_left_wheel_encoder
            real_right_encoder = self.robot.get_right_wheel_encoder
            if real_left_encoder > real_right_encoder:
                self.left_coefficient = 1.0
                self.right_coefficient = real_right_encoder / real_left_encoder
            else:
                self.right_coefficient = 1.0
                self.left_coefficient = real_left_encoder / real_right_encoder
            self.state = "ready"

        if self.state == "ready":
            self.state = "drive"

        if self.state == "drive":
            if self.real_left_encoder > self.real_right_encoder:
                self.left_speed = 10
                self.right_speed = 10 * self.right_coefficient
            else :
                self.right_speed = 10
                self.left_speed = 10 * self.left_coefficient


    def act(self):
        """The act method in the SPA architecture."""
        # Add code here...
        self.robot.set_left_wheel_speed(self.left_speed)
        self.robot.set_right_wheel_speed(self.right_speed)

    # ...


def main():
    """The main entry point."""
    robot = Robot()
    robot.robot.set_coefficients(0.7, 1.0)
    robot.set_state("calibrate")
    for i in range(int(120/0.05)):
        if robot.get_state() == "ready":
            start_left = robot.robot.get_left_wheel_encoder()
            start_right = robot.robot.get_right_wheel_encoder()
            robot.set_state("drive")
        robot.sense()
        robot.plan()
        robot.act()
        robot.robot.sleep(0.05)
    left_delta = robot.robot.get_left_wheel_encoder() - start_left
    right_delta = robot.robot.get_right_wheel_encoder() - start_right
    print(f"left {left_delta} right {right_delta}")


if __name__ == "__main__":
    main()