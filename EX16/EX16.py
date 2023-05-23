"""EX16."""

import PiBot
import math


class Robot:
    """The robot class."""

    def __init__(self, initial_odom: list = [0, 0, 0],
                 cell_size: float = 0.3, heading_tolerance: float = 5):
        """
        Initialize variables.

        Arguments:
          initial_odom -- Initial odometry, [x, y, yaw] in
            [meters, meters, radians]
          cell_size -- cell edge length in meters
          heading_tolerance -- the number of degrees
            deviation (+/-) allowed for direction classification
        """
        self.robot = PiBot.PiBot()

        self.robot_is_straight = False

        self.old_list = []
        self.new_list = []

        self.x_pos = 0
        self.y_pos = 0

        self.direction = "down"
        self.previous_x = 0
        self.previous_y = 0
        self.previous_dir = "down"

        self.map = [["?", "?", "?"], ["?", "?", "?"], ["?", "?", "?"]]
        self.rows = 3
        self.columns = 3

        self.pose_robot = None

        self.cell_size = cell_size
        self.heading_tolerance = heading_tolerance

        self.left_wheel_encoder = 0
        self.right_wheel_encoder = 0
        self.front_middle_laser = 0
        self.front_middle_list = []

        self.previous_left_wheel_encoder = 0

        self.initial_odom = initial_odom

        self.last_encoders_list = [0, 0]
        self.current_encoders_list = [0, 0]
        self.next_encoders_list = [0, 0]

        self.last_rotation = 0

        self.current_rotation = initial_odom[2]
        self.radius = self.robot.WHEEL_DIAMETER / 2
        self.distance = self.robot.AXIS_LENGTH
        self.time_delta = 0.05

        self.last_imu_odometry = None
        self.current_imu_odometry = None

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Set PiBot reference."""
        self.robot = robot

    def sense(self):
        """SPA architecture sense method."""

        self.old_list.append(self.robot.get_front_middle_laser())

        self.front_middle_laser = self.get_front_middle_laser()
        self.previous_x = self.x_pos
        self.previous_y = self.y_pos

        if self.last_imu_odometry is None and self.current_imu_odometry is None:
            self.last_imu_odometry = self.initial_odom
            self.current_imu_odometry = self.initial_odom

        self.last_encoders_list = self.current_encoders_list
        self.current_encoders_list = [self.robot.get_left_wheel_encoder(), self.robot.get_right_wheel_encoder()]
        self.last_rotation = self.current_rotation
        self.current_rotation = self.robot.get_rotation()
        self.calculate_imu_odometry()

    def get_front_middle_laser(self) -> float:
        """Return the filtered laser value."""
        if not self.old_list:
            return 0
        else:
            if len(self.old_list) > 5:
                self.new_list = self.old_list[-5:]
            else:
                self.new_list = self.old_list
            self.new_list.sort()
            if len(self.new_list) % 2 == 0 and len(self.new_list) != 0:
                return (self.new_list[len(self.new_list) // 2] + self.new_list[len(self.new_list) // 2 - 1]) / 2
            else:
                return self.new_list[len(self.new_list) // 2]

    def update_pose(self) -> None:
        """Update the robot pose."""
        if self.current_imu_odometry is None:
            return
        odometry_x = self.current_imu_odometry[0]
        odometry_y = self.current_imu_odometry[1]
        odometry_yaw = self.current_imu_odometry[2]

        robot_x = odometry_x // self.cell_size
        robot_y = odometry_y // self.cell_size
        robot_yaw = math.degrees(odometry_yaw) % 360
        if robot_yaw < 0:
            robot_yaw += 360

        heading = None

        if 90 - self.heading_tolerance <= robot_yaw <= 90 + self.heading_tolerance:
            heading = 90
            self.direction = "up"
        elif 180 - self.heading_tolerance <= robot_yaw <= 180 + self.heading_tolerance:
            heading = 180
            self.direction = "left"
        elif 270 - self.heading_tolerance <= robot_yaw <= 270 + self.heading_tolerance:
            heading = 270
            self.direction = "down"
        elif 360 - self.heading_tolerance <= robot_yaw or robot_yaw <= 0 + self.heading_tolerance:
            heading = 0
            self.direction = "right"

        self.x_pos = int(robot_x) * 2 + 1
        self.y_pos = int(robot_y) * 2 + 1

        if heading is not None:
            self.robot_is_straight = True
        else:
            self.robot_is_straight = False

        self.pose_robot = [int(robot_x), int(robot_y), heading]

    def get_pose(self) -> tuple:
        """Return pose."""
        if self.pose_robot is None:
            return None
        return tuple(self.pose_robot)

    def update_map(self) -> None:
        """Update map based on the current pose and the laser reading."""
        new_map_info = self.update_rows_and_columns()
        new_rows = new_map_info[0]
        new_columns = new_map_info[1]

        self.add_rows_or_columns_to_map(new_rows, new_columns)
        self.rows += new_rows
        self.columns += new_columns

        self.add_empty_space()
        if len(set(self.front_middle_list[-10:-1])) > 1:
            return
        if self.robot_is_straight:
            wall = self.get_wall_coordinates()
            self.add_wall(wall)

            self.add_empty_space_according_to_laser_info()

            self.rows = len(self.map)
            self.columns = len(self.map[0])

    def update_rows_and_columns(self):
        """Update map rows and columns."""
        new_rows = 0
        new_columns = 0

        if self.x_pos == self.previous_x and self.y_pos == self.previous_y:
            if self.direction == self.previous_dir:
                return 0, 0

        elif self.x_pos > len(self.map[0]) - 1 or self.y_pos > len(self.map) - 1:
            new_rows_and_columns = self.new_rows_and_columns()
            new_rows = new_rows_and_columns[0]
            new_columns = new_rows_and_columns[1]

        return new_rows, new_columns

    def new_rows_and_columns(self):
        """Return new rows and columns count."""
        new_rows = 0
        new_columns = 0

        if self.x_pos > len(self.map[0]) - 1:
            new_columns = self.x_pos - (len(self.map[0]) - 1)
        if self.y_pos > len(self.map) - 1:
            new_rows = self.y_pos - (len(self.map) - 1)

        return new_rows, new_columns

    def add_rows_or_columns_to_map(self, rows, columns):
        """Add new rows and columns to existing map."""
        while rows > 0:
            self.map.append(["?"] * self.columns)
            rows -= 1
        if columns > 0:
            for row in self.map:
                loop_nr = columns
                while loop_nr > 0:
                    row.append("?")
                    loop_nr -= 1

    def add_empty_space(self):
        """Add empty spaces to the map."""
        self.map[self.y_pos][self.x_pos] = " "
        if self.y_pos > self.previous_y:
            self.map[self.y_pos - 1][self.x_pos] = " "
        elif self.y_pos < self.previous_y:
            if self.y_pos + 1 > len(self.map) - 1:
                self.add_rows_or_columns_to_map(1, 0)
            self.map[self.y_pos + 1][self.x_pos] = " "
        elif self.x_pos > self.previous_x:
            while_loop = self.x_pos - self.previous_x
            while while_loop > 0:
                self.map[self.y_pos][self.x_pos - while_loop] = " "
                while_loop -= 1
        elif self.x_pos < self.previous_x:
            if self.x_pos + 1 > len(self.map[0]) - 1:
                self.add_rows_or_columns_to_map(0, 1)
            self.map[self.y_pos][self.x_pos + 1] = " "

    def get_wall_coordinates(self):
        """Return wall coordinates."""
        x = None
        y = None
        if self.direction == "left" and 2.0 > self.front_middle_laser > 0:
            x = int(self.x_pos - 1 - int(self.front_middle_laser // self.cell_size) * 2)
            y = self.y_pos
        elif self.direction == "right" and 2.0 > self.front_middle_laser > 0:
            x = int(self.x_pos + 1 + int(self.front_middle_laser // self.cell_size) * 2)
            y = self.y_pos
        elif self.direction == "up" and 2.0 > self.front_middle_laser > 0:
            x = self.x_pos
            y = int(self.y_pos + 1 + int(self.front_middle_laser // self.cell_size) * 2)
        elif self.direction == "down" and 2.0 > self.front_middle_laser > 0:
            x = self.x_pos
            y = int(self.y_pos - 1 - int(self.front_middle_laser // self.cell_size) * 2)

        if x is not None and x > len(self.map[0]) - 1:
            self.add_rows_or_columns_to_map(0, x - (len(self.map[0]) - 1))
        elif y is not None and y > len(self.map) - 1:
            self.add_rows_or_columns_to_map(y - (len(self.map) - 1), 0)

        if x is not None and y is not None:
            return self.get_wall_coordinates_2(x, y)

    def get_wall_coordinates_2(self, x, y):
        """Return wall coordinates extended."""
        if x is not None and x > len(self.map[0]) - 1:
            self.add_rows_or_columns_to_map(0, x - (len(self.map[0]) - 1))
        elif y is not None and y > len(self.map) - 1:
            self.add_rows_or_columns_to_map(y - (len(self.map) - 1), 0)

        if x is not None and y is not None:
            if x > len(self.map[0]) - 1:
                self.add_rows_or_columns_to_map(0, x - (len(self.map[0]) - 1))
            if y > len(self.map) - 1:
                self.add_rows_or_columns_to_map(y - (len(self.map) - 1), 0)

            if self.get_wall_coordinates_3(x, y) is not None:
                return x, y

    def get_wall_coordinates_3(self, x, y):
        """Return wall coordinates extended again."""
        if y == self.y_pos:
            if x > self.x_pos:
                while_loop = x - self.x_pos
                while while_loop > 0:
                    if self.map[y][x - while_loop] == "X":
                        return None
                    while_loop -= 1
            elif x < self.x_pos:
                while_loop = self.x_pos - x
                while while_loop > 0:
                    if self.map[y][x + while_loop] == "X":
                        return None
                    while_loop -= 1
        return self.get_wall_coordinates_4(x, y)

    def get_wall_coordinates_4(self, x, y):
        """Return wall coordinates extended again."""
        if x == self.x_pos:
            if y > self.y_pos:
                while_loop = y - self.y_pos
                while while_loop > 0:
                    if self.map[y - while_loop][x] == "X":
                        return None
                    while_loop -= 1
            elif y < self.y_pos:
                while_loop = self.y_pos - y
                while while_loop > 0:
                    if self.map[y + while_loop][x] == "X":
                        return None
                    while_loop -= 1
        return 0

    def add_wall(self, wall):
        """Add wall to the map."""
        if wall is not None:
            self.map[wall[1]][wall[0]] = "X"
            if wall[0] != self.x_pos:
                if wall[0] < self.x_pos:
                    while_loop = self.x_pos - wall[0]
                    while while_loop > 0:
                        self.map[wall[1]][wall[0] + 1] = " "
                        while_loop -= 1
            elif wall[0] > self.x_pos:
                while_loop = wall[0] - self.x_pos
                while while_loop > 0:
                    self.map[wall[1]][wall[0] - 1] = " "
                    while_loop -= 1
            else:
                self.add_wall_y(wall)

    def add_wall_y(self, wall):
        """Add wall y to the map."""
        if wall[1] != self.y_pos:
            if wall[1] < self.y_pos:
                while_loop = self.y_pos - wall[1]
                while while_loop > 0:
                    self.map[wall[1] + 1][wall[0]] = " "
                    while_loop -= 1
        elif wall[1] > self.y_pos:
            while_loop = wall[1] - self.y_pos
            while while_loop > 0:
                self.map[wall[1] - 1][wall[0]] = " "
                while_loop -= 1

    def add_empty_space_according_to_laser_info(self):
        """Add empty spaces to the map according to laser info - x."""
        if 2.0 > self.front_middle_laser > 0:
            while_loop = int(self.front_middle_laser // self.cell_size) * 2
            if self.direction == "left":
                while while_loop > 0:
                    self.map[self.y_pos][self.x_pos - while_loop] = " "
                    while_loop -= 1
            elif self.direction == "right":
                while while_loop > 0:
                    if self.x_pos + while_loop > len(self.map[0]) - 1:
                        self.add_rows_or_columns_to_map(0, while_loop)
                    self.map[self.y_pos][self.x_pos + while_loop] = " "
                    while_loop -= 1
            else:
                self.add_empty_space_according_to_laser_info_y()

    def add_empty_space_according_to_laser_info_y(self):
        """Add empty to the map according to laser info - y."""
        while_loop = int(self.front_middle_laser // self.cell_size) * 2
        if self.direction == "up":
            while while_loop > 0:
                if self.y_pos + while_loop > len(self.map) - 1:
                    self.add_rows_or_columns_to_map(while_loop, 0)
                self.map[self.y_pos + while_loop][self.x_pos] = " "
                while_loop -= 1
        elif self.direction == "down":
            while while_loop > 0:
                self.map[self.y_pos - while_loop][self.x_pos] = " "
                while_loop -= 1

    def get_map(self) -> str:
        """
        Print the known map.

        Returns:
          If the map is empty, must return None.
          The string representation of the map.
          Each cell should be one character + all neighboring cells/walls.
          The unknown spaces and walls should be denoted as "?"
          The walls should be marked as "X"

          An example:
            ?X?X???
            X   X??
            ? ? ?X?
            ? X   X
            ? ?X? ?
            ? X   X
            ? ? ?X?
            X   X??
            ?X?X???
        """
        if len(self.map) == 3:
            return None
        if self.direction == "right":
            self.add_rows_or_columns_to_map(0, 1)
        elif self.direction == "up":
            self.add_rows_or_columns_to_map(1, 0)
        answer = ""
        for list in reversed(self.map):
            answer += "".join(list) + "\n"
        print(answer.strip())
        return answer.strip()

    def calculate_imu_odometry(self):
        """Calculate imu."""
        self.last_imu_odometry = self.current_imu_odometry
        ul = ((self.current_encoders_list[0] - self.last_encoders_list[0]) * math.pi / 180 / self.time_delta)
        ur = ((self.current_encoders_list[1] - self.last_encoders_list[1]) * math.pi / 180 / self.time_delta)
        next_rot = self.current_rotation - self.last_rotation
        next_x = (self.radius / 2) * ((ul + ur) * math.cos(self.current_rotation))
        next_y = (self.radius / 2) * ((ul + ur) * math.sin(self.current_rotation))
        self.current_imu_odometry[0] = self.last_imu_odometry[0] + (next_x * self.time_delta)
        self.current_imu_odometry[1] = self.last_imu_odometry[1] + (next_y * self.time_delta)
        self.current_imu_odometry[2] = self.last_imu_odometry[2] + next_rot

    def spin(self):
        """Initialize spin."""
        for _ in range(10):
            self.sense()
            self.update_pose()
            self.update_map()
            self.robot.sleep(0.05)
        print(f"{self.get_map()}")
