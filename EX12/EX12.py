"""EX12 - Potential Field Gradient Descent."""
import PiBot
import math


class Robot:
    """The robot class."""

    def __init__(self, attraction_threshold: float = 0.2,
                 attraction_coefficient: float = 2.0,
                 repulsion_threshold: float = 0.4,
                 repulsion_coefficient: float = 1.0):
        """Initialize variables."""
        self.robot = PiBot.PiBot()
        self.obstacles = []
        self.attraction_threshold = attraction_threshold
        self.attraction_coefficient = attraction_coefficient
        self.repulsion_threshold = repulsion_threshold
        self.repulsion_coefficient = repulsion_coefficient

    @staticmethod
    def distance(first: tuple, second: tuple) -> float:
        """
        Calculate the Euclidean distance between two points.

        Returns:
          The distance between two points.
        """
        return math.sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)

    def set_robot(self, robot: PiBot.PiBot()) -> None:
        """Se the API reference."""
        self.robot = robot

    def set_obstacles(self, obstacles: tuple) -> None:
        """
        Set the obstacles.

        Set the obstacles (i.e., repulsive potential sources) for
        potential field planning.

        Arguments:
          obstacles -- the tuple of 2-tuples defining the obstacles.
                       E.g., ((1, 1), (2, 2), ...)
        """
        self.obstacles = []
        for obstacle in obstacles:
            self.obstacles.append((obstacle[0], obstacle[1]))

    def compute_attractor_gradient(self, point: tuple, goal: tuple) -> tuple:
        """
        Compute the attraction gradient (the vector pointing toward the goal).

        Args:
          point -- the point where the gradient is calculated at.
                   Tuple with x, y coordinates
          goal -- the goal as tuple with x, y coordinates
        Returns:
          Returns gradient vector
        """
        d = Robot.distance(point, goal)
        if d <= self.attraction_threshold:
            u_att_x = self.attraction_coefficient * (point[0] - goal[0])
            u_att_y = self.attraction_coefficient * (point[1] - goal[1])
        else:
            u_att_x = (self.attraction_threshold
                       * self.attraction_coefficient * (point[0] - goal[0])) / d
            u_att_y = (self.attraction_threshold *
                       self.attraction_coefficient * (point[1] - goal[1])) / d
        return u_att_x, u_att_y

    def compute_repulsion_gradient(self, point: tuple,
                                   obstacles: tuple) -> tuple:
        """
        Compute the repulsion gradient.

        Compute the repulsion gradient (the combined vector pointing away
        from the obstacles).

        Args:
          point -- the point where the gradient is calculated at.
                   Tuple with x, y coordinates
          obstacles -- the obstacles as a tuple with tuples with x, y
                       coordinates
        Returns:
          Returns gradient vector
        """
        u_rep_x = 0
        u_rep_y = 0
        for obstacle in obstacles:
            d = Robot.distance(point, obstacle)
            if d <= self.repulsion_threshold:
                deg = math.atan2(obstacle[1] - point[1],
                                 obstacle[0] - point[0])
                x = point[0] + d * math.cos(deg)
                y = point[1] + d * math.sin(deg)
                u_rep_x += self.repulsion_coefficient * ((1 / self.repulsion_threshold) - (1 / d)) \
                           * (1 / d) ** 2 * ((point[0] - x) / d)
                u_rep_y += self.repulsion_coefficient \
                           * ((1 / self.repulsion_threshold) - (1 / d)) \
                           * (1 / d) ** 2 * ((point[1] - y) / d)
        return u_rep_x, u_rep_y

    def calculate_plan(self, start_pos: tuple, target_pos: tuple, step_distance: float, target_margin: float = 0.1)\
            -> list:
        """
        Determine the path from start_pos to target_pos or multiple targets through waypoints.

        Args:
          start_pos -- initial coordinates (x, y) as floats
          target_pos -- tuple containing target coordinates (x, y) as floats
          step_distance -- the length of each step in the path (in meters)
          target_margin -- the acceptable deviation from the target
                           to terminate the algorithm

        Returns:
          Pathway to reach the target as a list of coordinates
          (e.g., [(0, 0.5), (0, 1), (0, 1.5), (0, 2)])
        """
        barriers = tuple(self.obstacles)
        route = []
        while True:
            x_gradient = (self.compute_attractor_gradient(start_pos, target_pos)[0]
                          +
                          self.compute_repulsion_gradient(start_pos, barriers)[0])
            y_gradient = (self.compute_attractor_gradient(start_pos, target_pos)[1] +
                          self.compute_repulsion_gradient(start_pos, barriers)[1])

            gradient_magnitude = math.sqrt(x_gradient ** 2 + y_gradient ** 2)
            normalized_vector = (-(x_gradient / gradient_magnitude), -(y_gradient / gradient_magnitude))

            start_pos = (start_pos[0] + normalized_vector[0] * step_distance,
                         start_pos[1] + normalized_vector[1] * step_distance)

            route.append(start_pos)
            if self.distance(route[-1], target_pos) <= target_margin:
                break
        return route


def test():
    """Testing function."""
    robot = Robot(attraction_coefficient=2, repulsion_coefficient=0.5,
                  repulsion_threshold=2)
    import straight  # or any other data file
    data = straight.get_data()
    robot.set_obstacles(data[1])
    plan = robot.calculate_plan((0, 0), data[0], 0.1, 0.1)
    # plot(plan)
    print(f"{list(map(lambda x: (round(x[0], 3), round(x[1], 3)), plan))}")


def plot(plan: tuple):
    """Plot with matplotlib."""
    import matplotlib.pyplot
    zipped = list(zip(*plan))
    matplotlib.pyplot.plot(zipped[0], zipped[1])
    matplotlib.pyplot.axis([0, max(max(zipped[0]), max(zipped[1])), 0,
                            max(max(zipped[0]), max(zipped[1]))])
    matplotlib.pyplot.savefig("fig.png")


def main():
    """Initialize main entry point."""
    robot = Robot()
    robot.set_obstacles(((0.2, 3), (-0.3, 4)))
    plan = robot.calculate_plan((0, 0), (0, 6), 0.15)
    print(f"{list(map(lambda x: (round(x[0], 3), round(x[1], 3)), plan))}")


if __name__ == "__main__":
    main()
    # test()
