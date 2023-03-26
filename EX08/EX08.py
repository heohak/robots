"""EX08 - PID."""
import PiBot


class Robot:
    """The robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()

        self.left_encoder_now = 0
        self.right_encoder_now = 0
        self.left_encoder_prev = 0
        self.right_encoder_prev = 0
        self.prev_time = 0
        self.delta_time = 0
        self.time = 0
        self.left_actual_speed = 0
        self.right_actual_speed = 0
        self.left_wheel_speed_setpoint = 0
        self.right_wheel_speed_setpoint = 0
        self.left_pid_output = 0
        self.right_pid_output = 0
        self.error_left_prev = 0
        self.error_right_prev = 0
        self.error_left_now = 0
        self.error_right_now = 0
        self.error_left_sum = 0
        self.error_right_sum = 0
        self.p = 0
        self.i = 0
        self.d = 0

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set the API reference."""
        self.robot = robot

    def set_pid_parameters(self, p: float, i: float, d: float):
        """
        Set the PID parameters.

        Arguments:
          p -- The proportional component.
          i -- The integral component.
          d -- The derivative component.
        """
        self.p = p
        self.i = i
        self.d = d

    def set_left_wheel_speed(self, speed: float):
        """
        Set the desired setpoint.

        Arguments:
          speed -- The speed setpoint for the controller.
        """
        self.left_wheel_speed_setpoint = speed

    def set_right_wheel_speed(self, speed: float):
        """
        Set the desired setpoint.

        Arguments:
          speed -- The speed setpoint for the controller.
        """
        self.right_wheel_speed_setpoint = speed

    def get_left_wheel_pid_output(self):
        """
        Get the controller output value for the left motor.

        Returns:
          The controller output value.
        """
        return self.left_pid_output

    def get_right_wheel_pid_output(self):
        """
        Get the controller output value for the right motor.

        Returns:
          The controller output value.
        """
        return self.right_pid_output

    def update_time(self):
        """Update time."""
        self.prev_time = self.time
        self.time = self.robot.get_time()
        self.delta_time = self.time - self.prev_time

    def update_encoders(self):
        """Update encoders."""
        self.left_encoder_prev = self.left_encoder_now
        self.right_encoder_prev = self.right_encoder_now
        self.left_encoder_now = self.robot.get_left_wheel_encoder()
        self.right_encoder_now = self.robot.get_right_wheel_encoder()

    def calculate_actual_speed(self):
        """Calculate actual speed."""
        if self.delta_time > 0:
            self.left_actual_speed = (self.left_encoder_now - self.left_encoder_prev) / self.delta_time
            self.right_actual_speed = (self.right_encoder_now - self.right_encoder_prev) / self.delta_time

    def calculate_errors(self):
        """Calculate errors."""
        self.error_left_now = self.left_wheel_speed_setpoint - self.left_actual_speed
        self.error_right_now = self.right_wheel_speed_setpoint - self.right_actual_speed

    def update_error_sums(self):
        """Update error sums."""
        self.error_left_sum += self.error_left_now * self.delta_time
        self.error_right_sum += self.error_right_now * self.delta_time

    def calculate_error_differences(self):
        """Calculate error differences."""
        if self.delta_time > 0:
            left_error_diff = (self.error_left_now - self.error_left_prev) / self.delta_time
            right_error_diff = (self.error_right_now - self.error_right_prev) / self.delta_time
        else:
            left_error_diff = 0
            right_error_diff = 0
        return left_error_diff, right_error_diff

    def update_previous_errors(self):
        """Update previous errors."""
        self.error_left_prev = self.error_left_now
        self.error_right_prev = self.error_right_now

    def update_controller_outputs(self, left_error_diff, right_error_diff):
        """Update previous outputs."""
        self.left_pid_output = self.p * self.error_left_now + self.i * self.error_left_sum + self.d * left_error_diff
        self.right_pid_output = self.p * self.error_right_now + self.i * self.error_right_sum + self.d * right_error_diff

    def sense(self):
        """SPA architecture sense block."""
        self.update_time()
        self.update_encoders()
        self.calculate_actual_speed()
        self.calculate_errors()
        self.update_error_sums()

        left_error_diff, right_error_diff = self.calculate_error_differences()
        self.update_previous_errors()
        self.update_controller_outputs(left_error_diff, right_error_diff)

    def act(self):
        """SPA architecture act block."""
        self.robot.set_left_wheel_speed(self.get_left_wheel_pid_output())
        self.robot.set_right_wheel_speed(self.get_right_wheel_pid_output())

    def spin(self):
        """Spin loop."""
        for _ in range(200):
            self.sense()
            self.act()
            print(self.get_left_wheel_pid_output())
            print(self.get_right_wheel_pid_output())
            self.robot.sleep(0.20)


def main():
    """Create main method for robot."""
    robot = Robot()
    robot.robot.set_coefficients(1.0, 0.7)
    robot.set_pid_parameters(0.1, 0.04, 0.001)
    robot.set_left_wheel_speed(400)  # degs/s
    robot.set_right_wheel_speed(400)  # degs/s
    robot.spin()


if __name__ == "__main__":
    main()
