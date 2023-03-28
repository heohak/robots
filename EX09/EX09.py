import PiBot
from math import sin, cos


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
        self.WHEEL_CIRCUMFERENCE = self.robot.WHEEL_DIAMETER * 3.141592653589793
        self.ENCODER_TICKS = 360

        self.encoder_odometry = list(initial_odometry)
        self.imu_odometry = list(initial_odometry)
        self.imu_yaw = 0

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set the API reference."""
        self.robot = robot

    def update_encoder_odometry(self):
        d_left = self.left_wheel_distance
        d_right = self.right_wheel_distance
        d_center = (d_left + d_right) / 2

        delta_yaw = (d_right - d_left) / self.robot.AXIS_LENGTH

        dx = d_center * cos(self.encoder_odometry[2] + delta_yaw / 2)
        dy = d_center * sin(self.encoder_odometry[2] + delta_yaw / 2)

        self.encoder_odometry[0] += dx
        self.encoder_odometry[1] += dy
        self.encoder_odometry[2] += delta_yaw

    def update_imu_odometry(self):
        d_left = self.left_wheel_distance
        d_right = self.right_wheel_distance
        d_center = (d_left + d_right) / 2

        imu_yaw = self.robot.get_rotation()
        delta_yaw = imu_yaw - self.imu_yaw
        self.imu_yaw = imu_yaw

        dx = d_center * cos(self.imu_odometry[2] + delta_yaw / 2)
        dy = d_center * sin(self.imu_odometry[2] + delta_yaw / 2)

        self.imu_odometry[0] += dx
        self.imu_odometry[1] += dy
        self.imu_odometry[2] += delta_yaw

    @property
    def left_wheel_distance(self):
        ticks = self.robot.get_left_wheel_encoder()
        return (ticks / self.ENCODER_TICKS) * self.WHEEL_CIRCUMFERENCE

    @property
    def right_wheel_distance(self):
        ticks = self.robot.get_right_wheel_encoder()
        return (ticks / self.ENCODER_TICKS) * self.WHEEL_CIRCUMFERENCE

    def get_encoder_odometry(self):
        """
        Return the encoder odometry.

        Returns:
           A tuple with x, y coordinates and yaw angle (x, y, yaw)
           based on encoder data. The units must be (meters, meters, radians).
        """
        print(tuple(self.encoder_odometry))
        return tuple(self.encoder_odometry)

    def get_imu_odometry(self):
        """
        Return the IMU odometry.

        Returns:
           A tuple with x, y coordinates and yaw angle (x, y, yaw)
           based on encoder and IMU data. The units must be
           (meters, meters, radians).
        """
        print(tuple(self.imu_odometry))
        return tuple(self.imu_odometry)

    def sense(self):
        """SPA architecture sense block."""
        self.update_encoder_odometry()
        self.update_imu_odometry()

    def spin(self):
        """Spin loop."""
        for _ in range(100):
            self.sense()
            self.robot.sleep(0.05)

def test():
    robot = Robot()
    import spin_left # or any other data file
    data = spin_left.get_data()
    robot.robot.load_data_profile(data)
    for i in range(len(data)):
        robot.sense()
        print(tuple(robot.encoder_odometry))
        print(tuple(robot.imu_odometry))

        #print(f"encoder {robot.robot.get_left_wheel_encoder()}")
        robot.robot.sleep(0.05)

if __name__ == "__main__":
    test()