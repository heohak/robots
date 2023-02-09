"""EX03 - Instantaneous velocity."""
import PiBot
import math


class Robot:
    """The robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.left_wheel_encoder = 0
        self.right_wheel_encoder = 0
        self.left_wheel_before_encoder = 0
        self.right_wheel_before_encoder = 0
        self.left_wheel_spin_velocity = 0
        self.right_wheel_spin_velocity = 0
        self.wheel_size = 0
        self.before_time = 0
        self.current_time = 0

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set robot reference."""
        self.robot = robot

    def get_robot_wheel_size(self):
        """Find the robot's wheel size by taking the wheel diameter and multiplying it with Pi."""
        wheel_size = self.robot.WHEEL_DIAMETER * math.pi
        return wheel_size

    def get_left_velocity(self) -> float:
        """
        Return the current left wheel velocity.

        Returns:
          The current wheel translational velocity in meters per second.
        """
        left_wheel_velocity = self.left_wheel_spin_velocity * self.get_robot_wheel_size() / 360
        return left_wheel_velocity

    def get_right_velocity(self) -> float:
        """
        Return the current right wheel velocity.

        Returns:
          The current wheel translational velocity in meters per second.
        """
        right_wheel_velocity = self.right_wheel_spin_velocity * self.get_robot_wheel_size() / 360
        return right_wheel_velocity

    def find_time_between_scans(self):
        """Find the time inbetween two encoder scans."""
        time_between_scans = self.current_time - self.before_time
        return time_between_scans

    def sense(self):
        """Read the sensor values from the PiBot API."""
        "Get current scan time"
        self.current_time = self.robot.get_time()

        "Get both wheel encoders."
        self.left_wheel_encoder = self.robot.get_left_wheel_encoder()
        self.right_wheel_encoder = self.robot.get_right_wheel_encoder()

        "Get both wheel spin velocity."
        if self.find_time_between_scans() > 0:
            self.right_wheel_spin_velocity = \
                (self.right_wheel_encoder - self.right_wheel_before_encoder) / self.find_time_between_scans()
            self.left_wheel_spin_velocity = \
                (self.left_wheel_encoder - self.left_wheel_before_encoder) / self.find_time_between_scans()
        else:
            pass

        "Get before scan time current time so you can measure the wheel spin velocity again."
        self.before_time = self.current_time

        "Get previous encoders."
        self.left_wheel_before_encoder = self.left_wheel_encoder
        self.right_wheel_before_encoder = self.right_wheel_encoder

        "Now the loop continues..."

    def spin(self):
        """Spin main function."""
        while not self.shutdown:
            self.sense()
            timestamp = self.robot.get_time()
            left_velocity = self.get_left_velocity()
            right_velocity = self.get_right_velocity()
            print(f'{timestamp}: {left_velocity} {right_velocity}')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


def main():
    """Get main entry."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()
