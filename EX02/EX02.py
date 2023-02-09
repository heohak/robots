"""EX02."""


import PiBot


class Robot:
    """Initialize robot class."""

    def __init__(self):
        """Initialize the robot1."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.state = "unknown"
        self.distance = 0.0

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """
        Set the reference to PiBot object.

        Returns:
          None
        """
        self.robot = robot

    def get_state(self) -> str:
        """
        Return the current state.

        Returns:
          The current state as a string.
        """
        # Your code here...
        return self.state

    def sense(self):
        """
        Read values from sensors via PiBot  API into class variables (self).

        Returns:
          None
        """
        self.distance = self.robot.get_front_middle_laser()
        # Write some code here...
        pass

    def plan(self):
        """
        Perform the planning steps as required by the problem statement.

        Returns:
          None
        """
        if self.distance >= 2.0:
            self.state = "very far"
        elif self.distance > 1.5:
            self.state = "far"
        elif 0.5 < self.distance <= 1.5:
            self.state = "ok"
        elif 0.0 < self.distance <= 0.5:
            self.state = "close"
        else:
            self.state = "unknown"

        # Write some code here...
        pass

    def spin(self):
        """Initialize the main loop of the robot."""
        while not self.shutdown:
            print(f'The time is {self.robot.get_time()}!')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.sense()
                self.plan()
                self.shutdown = True

    # Add more code...


def main():
    """Create a Robot object and spin it."""
    robot = Robot()
    robot.spin()
