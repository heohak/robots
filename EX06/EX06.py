import PiBot

WHEEL_DIAMETER = 0.03
AXIS_LENGTH = 0.132


class Robot:
    """Robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.object_list = []
        self.prev_encoder_values = [0, 0]
        self.prev_time = self.robot.get_time()
        self.prev_direction = None

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set Robot reference."""
        self.robot = robot

    def get_objects(self) -> list:
        """
        Return the list with the detected objects so far.

        (i.e., add new objects to the list as you detect them).

        Returns:
          The list with detected object angles, the angles are in
          degrees [0..360), 0 degrees being the start angle and following
          the right-hand rule (e.g., turning left 90 degrees is 90, turning
          right 90 degrees is 270 degrees).
        """
        return self.object_list

    def get_front_middle_laser(self):
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        laser_values = self.robot.get_front_lasers()
        return laser_values[1]

    def sense(self):
        """Sense method according to the SPA architecture."""
        curr_encoder_values = [self.robot.get_left_wheel_encoder(), self.robot.get_right_wheel_encoder()]
        curr_time = self.robot.get_time()
        time_diff = curr_time - self.prev_time

        if self.prev_direction is None:
            # no previous direction, wait for the robot to move
            if curr_encoder_values != self.prev_encoder_values:
                self.prev_direction = 'forward' if curr_encoder_values[0] > 0 else 'backward'
        else:
            # calculate rotation and distance
            rotation = (curr_encoder_values[1] - curr_encoder_values[0]) / AXIS_LENGTH
            distance = (curr_encoder_values[0] + curr_encoder_values[1]) / 2 * WHEEL_DIAMETER

            if self.prev_direction == 'backward':
                # reverse the sign of the rotation
                rotation = -rotation

            # calculate the heading change
            heading_change = rotation * 180 / 3.1415
            self.robot.set_heading(self.robot.get_heading() + heading_change)

            # check for objects
            laser_value = self.get_front_middle_laser()
            if laser_value < 0.2 and distance > 0:
                # object detected, add to the list
                angle = self.robot.get_heading() % 360
                self.object_list.append(angle)

        # update the previous values
        self.prev_encoder_values = curr_encoder_values
        self.prev_time = curr_time

    def act(self):
        """Act method according to the SPA architecture."""
        self.robot.forward(0.2)

    def spin(self):
        """The main loop."""
        while not self.shutdown:
            self.sense()
            self.act()
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True


def main():
    """The main entry point."""
    robot = Robot()
    robot.spin()
    print(robot.get_objects())


if __name__ == "__main__":
    main()