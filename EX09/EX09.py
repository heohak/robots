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
        self.x, self.y, self.yaw = initial_odometry
        self.prev_left_encoder = self.robot.get_left_wheel_encoder()
        self.prev_right_encoder = self.robot.get_right_wheel_encoder()

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
        left_wheel_encoder = self.robot.get_left_wheel_encoder()
        right_wheel_encoder = self.robot.get_right_wheel_encoder()

        delta_left = (left_wheel_encoder - self.prev_left_encoder) * self.robot.WHEEL_DIAMETER * math.pi / 360
        delta_right = (right_wheel_encoder - self.prev_right_encoder) * self.robot.WHEEL_DIAMETER * math.pi / 360

        self.prev_left_encoder = left_wheel_encoder
        self.prev_right_encoder = right_wheel_encoder

        delta_s = (delta_right + delta_left) / 2
        delta_yaw = (delta_right - delta_left) / self.robot.AXIS_LENGTH

        self.x += delta_s * math.cos(self.yaw + delta_yaw / 2)
        self.y += delta_s * math.sin(self.yaw + delta_yaw / 2)
        self.yaw += delta_yaw

        return self.x, self.y, self.yaw

    def get_imu_odometry(self):
        """
        Return the IMU odometry.

        Returns:
           A tuple with x, y coordinates and yaw angle (x, y, yaw)
           based on encoder and IMU data. The units must be
           (meters, meters, radians).
        """
        # Your code here...
        pass

    def sense(self):
        """SPA architecture sense block."""
        odometry = self.get_encoder_odometry()
        print(f"Odometry: x={odometry[0]:.3f}, y={odometry[1]:.3f}, yaw={odometry[2]:.3f}")

    def spin(self):
        """Spin loop."""
        for _ in range(100):
            self.sense()
            self.robot.sleep(0.05)


def main():
    """The main entry point."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()