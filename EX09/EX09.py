import math
import PiBot

class Robot:
    def __init__(self, initial_odometry=[0, 0, 0]):
        self.robot = PiBot.PiBot()
        self.prev_left_encoder = 0
        self.prev_right_encoder = 0
        self.encoder_odometry = initial_odometry[:]
        self.imu_odometry = initial_odometry[:]

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        self.robot = robot

    def get_encoder_odometry(self):
        return tuple(self.encoder_odometry)

    def get_imu_odometry(self):
        return tuple(self.imu_odometry)

    def sense(self):
        left_encoder = self.robot.get_left_wheel_encoder()
        right_encoder = self.robot.get_right_wheel_encoder()
        imu_yaw = self.robot.get_rotation()

        # Compute the change in encoder values
        left_delta = (left_encoder - self.prev_left_encoder) * self.robot.WHEEL_DIAMETER * math.pi
        right_delta = (right_encoder - self.prev_right_encoder) * self.robot.WHEEL_DIAMETER * math.pi
        # Update the previous encoder values
        self.prev_left_encoder = left_encoder
        self.prev_right_encoder = right_encoder

        # Calculate the average distance traveled and the change in yaw
        avg_delta = (left_delta + right_delta) / 2
        yaw_delta = (right_delta - left_delta) / self.robot.AXIS_LENGTH

        # Update the encoder odometry
        self.encoder_odometry[0] += avg_delta * math.cos(self.encoder_odometry[2] + yaw_delta / 2)
        self.encoder_odometry[1] += avg_delta * math.sin(self.encoder_odometry[2] + yaw_delta / 2)
        self.encoder_odometry[2] += yaw_delta

        # Update the IMU odometry
        self.imu_odometry[0] += avg_delta * math.cos(imu_yaw)
        self.imu_odometry[1] += avg_delta * math.sin(imu_yaw)
        self.imu_odometry[2] = imu_yaw

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
        print(f"encoder {robot.robot.get_left_wheel_encoder()}")
        robot.robot.sleep(0.05)

if __name__ == "__main__":
    test()
