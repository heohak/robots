"""EX08 - PID."""
import PiBot


class Robot:
    """The robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.left_wheel_speed_setpoint = 0
        self.right_wheel_speed_setpoint = 0
        self.left_wheel_error_sum = 0
        self.right_wheel_error_sum = 0
        self.left_wheel_last_error = 0
        self.right_wheel_last_error = 0
        self.p = 0
        self.i = 0
        self.d = 0
        self.left_wheel_pid_output = 0
        self.right_wheel_pid_output = 0

    def set_pid_parameters(self, p: float, i: float, d: float):
        self.p = p
        self.i = i
        self.d = d

    def set_left_wheel_speed(self, speed: float):
        self.left_wheel_speed_setpoint = speed

    def set_right_wheel_speed(self, speed: float):
        self.right_wheel_speed_setpoint = speed

    def get_left_wheel_pid_output(self):
        return self.left_wheel_pid_output

    def get_right_wheel_pid_output(self):
        return self.right_wheel_pid_output

    def sense(self):
        left_wheel_actual_speed = self.robot.get_left_wheel_encoder()
        right_wheel_actual_speed = self.robot.get_right_wheel_encoder()

        left_wheel_error = self.left_wheel_speed_setpoint - left_wheel_actual_speed
        right_wheel_error = self.right_wheel_speed_setpoint - right_wheel_actual_speed

        self.left_wheel_error_sum += left_wheel_error
        self.right_wheel_error_sum += right_wheel_error

        # Limit the integral term to prevent windup
        max_integral = 100
        self.left_wheel_error_sum = max(min(self.left_wheel_error_sum, max_integral), -max_integral)
        self.right_wheel_error_sum = max(min(self.right_wheel_error_sum, max_integral), -max_integral)

        left_wheel_error_derivative = left_wheel_error - self.left_wheel_last_error
        right_wheel_error_derivative = right_wheel_error - self.right_wheel_last_error

        self.left_wheel_pid_output = (self.p * left_wheel_error +
                                   self.i * self.left_wheel_error_sum +
                                   self.d * left_wheel_error_derivative)
        self.right_wheel_pid_output = (self.p * right_wheel_error +
                                    self.i * self.right_wheel_error_sum +
                                    self.d * right_wheel_error_derivative)

        self.left_wheel_last_error = left_wheel_error
        self.right_wheel_last_error = right_wheel_error

    def act(self):
        self.robot.set_left_wheel_speed(self.left_wheel_pid_output)
        self.robot.set_right_wheel_speed(self.right_wheel_pid_output)


    def spin(self):
        """Spin loop."""
        for _ in range(200):
            self.sense()
            self.act()
            self.robot.sleep(0.20)


def main():
    """The main entry point."""
    robot = Robot()
    robot.robot.set_coefficients(1.0, 0.7)
    robot.set_pid_parameters(0.1, 0.04, 0.001)
    robot.set_left_wheel_speed(400)  # degs/s
    robot.set_right_wheel_speed(400)  # degs/s
    robot.spin()


if __name__ == "__main__":
    main()