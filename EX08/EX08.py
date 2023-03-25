"""EX08 - PID."""
import PiBot


class Robot:
    """The robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.p = 0
        self.i = 0
        self.d = 0
        self.left_wheel_speed_setpoint = 0
        self.right_wheel_speed_setpoint = 0
        self.left_wheel_error_sum = 0
        self.right_wheel_error_sum = 0
        self.left_wheel_last_error = 0
        self.right_wheel_last_error = 0
        self.left_wheel_pid_output = 0
        self.right_wheel_pid_output = 0

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
        # Your code here...

    def set_left_wheel_speed(self, speed: float):
        """
        Set the desired setpoint.

        Arguments:
          speed -- The speed setpoint for the controller.
        """
        self.left_wheel_speed_setpoint = speed
        # Your code here...

    def set_right_wheel_speed(self, speed: float):
        """
        Set the desired setpoint.

        Arguments:
          speed -- The speed setpoint for the controller.
        """
        self.right_wheel_speed_setpoint = speed
        # Your code here...
        pass

    def get_left_wheel_pid_output(self):
        """
        Get the controller output value for the left motor.

        Returns:
          The controller output value.
        """
        # Your code here...
        return self.left_wheel_pid_output

    def get_right_wheel_pid_output(self):
        """
        Get the controller output value for the right motor.

        Returns:
          The controller output value.
        """
        # Your code here...
        return self.right_wheel_pid_output

    def sense(self):
        """SPA architecture sense block."""
        # Your code here...
        left_wheel_actual_speed = self.robot.get_left_wheel_encoder()
        right_wheel_actual_speed = self.robot.get_right_wheel_encoder()

        left_wheel_error = self.left_wheel_speed_setpoint - left_wheel_actual_speed
        right_wheel_error = self.right_wheel_speed_setpoint - right_wheel_actual_speed

        self.left_wheel_error_sum += left_wheel_error
        self.right_wheel_error_sum += right_wheel_error

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
        """SPA architecture act block."""
        # Your code here...
        left_wheel_speed = self.get_left_wheel_pid_output()
        right_wheel_speed = self.get_right_wheel_pid_output()

        self.robot.set_left_wheel_speed(left_wheel_speed)
        self.robot.set_right_wheel_speed(right_wheel_speed)

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