import math
import PiBot
class Robot:

    """Robot class."""

    def __init__(self, initial_odometry=[0, 0, 0]):
        """
        Initialize variables.

        Arguments:
          initial_odometry -- Initial odometry(start position and angle),
                              [x, y, yaw] in [meters, meters, radians]
        """
        self.robot = PiBot.PiBot()
        self.odometry = initial_odometry

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set the API reference."""
        self.robot = robot

    def get_encoder_odometry(self):
        """
        Return the encoder odometry.

        Returns:
           A tuple with x, y coordinates and yaw angle (x, y, yaw)
           based on encoder data. The units must be (meters, meters, radians).
        """
        left_distance, right_distance = self.robot.get_encoder_distances()
        delta_distance = (left_distance + right_distance) / 2
        delta_yaw = (right_distance - left_distance) / self.robot.wheel_base

        # Update odometry
        self.odometry[0] += delta_distance * math.cos(self.odometry[2])
        self.odometry[1] += delta_distance * math.sin(self.odometry[2])
        self.odometry[2] += delta_yaw

        return tuple(self.odometry)

    def get_imu_odometry(self):
        """
        Return the IMU odometry.

        Returns:
           A tuple with x, y coordinates and yaw angle (x, y, yaw)
           based on encoder and IMU data. The units must be
           (meters, meters, radians).
        """
        imu_yaw = self.robot.get_imu_yaw()
        self.odometry[2] = imu_yaw

        return tuple(self.odometry)

    def sense(self):
        """SPA architecture sense block."""
        self.get_encoder_odometry()
        self.get_imu_odometry()

    def spin(self):
        """Spin loop."""
        for _ in range(100):
            self.sense()
            self.robot.sleep(0.05)

    # ...

def main():
    """The main entry point."""
    robot = Robot()
    robot.spin()

if __name__ == "__main__":
    main()
