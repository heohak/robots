"""OT05 - Noise."""
import PiBot
import statistics


class Robot:
    """Robot class."""

    def __init__(self):
        """Initialize object."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.values = []

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set the PiBot reference."""
        self.robot = robot

    def sense(self):
        """Read values."""
        front_laser = self.robot.get_front_middle_laser()
        self.values.append(front_laser)
        if len(self.values) == 6:
            self.values.remove(self.values[0])

    def get_front_middle_laser(self) -> float:
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        if not self.values:
            return None
        return statistics.median(self.values)
        # Your code here...

    def spin(self):
        """Initialize spin loop."""
        while not self.shutdown:
            print(f'Value is {self.get_front_middle_laser()}')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


def main():
    """Main entry point."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
