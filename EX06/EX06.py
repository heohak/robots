import PiBot

class Robot:
    """Robot class."""

    def __init__(self):
        """Class constructor."""
        self.robot = PiBot.PiBot()
        self.shutdown = False
        self.objects = []
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
        return self.objects

    def get_front_middle_laser(self):
        """
        Return the filtered value.

        Returns:
          None if filter is empty, filtered value otherwise.
        """
        return self.robot.get_front_middle_laser()

    def sense(self):
        """Sense method according to the SPA architecture."""
        distance = self.get_front_middle_laser()
        if distance is not None and distance < 0.5:
            left_encoder = self.robot.get_left_wheel_encoder()
            right_encoder = self.robot.get_right_wheel_encoder()
            delta = (right_encoder - left_encoder) * 0.025
            angle = delta / distance
            self.objects.append((angle, distance))

    def spin(self):
        """The main loop."""
        while not self.shutdown:
            print(f'Value is {self.get_front_middle_laser()}')
            self.robot.sleep(0.05)
            if self.robot.get_time() > 20:
                self.shutdown = True



def main():
    """The  main entry point."""
    robot = Robot()
    robot.spin()


if __name__ == "__main__":
    main()

def test():
    robot = Robot()
    import close # or any other data file
    data = close.get_data()
    robot.robot.load_data_profile(data)
    for i in range(len(data)):
        print(f"laser = {robot.robot.get_front_middle_laser()}")
        robot.robot.sleep(0.05)

if __name__ == "__main__":
    test()
