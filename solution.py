import numpy as np
from queue import PriorityQueue

# hide incorrect shape warning and instead handle within parse_maze
# incorrect_shape_warning = {
#     "message": "^.*ndarray from ragged nested sequences",
#     "category": np.VisibleDeprecationWarning
# }
# np.warnings.filterwarnings(
#     'ignore', **incorrect_shape_warning)


def parse_maze(maze: str) -> np.ndarray:
    """
    Convert a string to a 2d numpy ndarray.

    Parameters
    ----------
    maze : str
      A string representation of a maze.
      Rows are delimited with a newline character.
      Each cell is one character.

    Returns
    -------
    np.ndarray
      An array representation of a maze.

    Examples
    -------
    >>> parse_maze("sxe\n.x.\n...")
    array([['s', 'x', 'e'],
           ['.', 'x', '.'],
           ['.', '.', '.']])
    """
    if type(maze) != str:
        raise TypeError("maze must be of type <str>")
    rows = maze.strip().split('\n')
    array = np.array([list(row.strip()) for row in rows])
    if (len(array.shape) != 2):
        raise ValueError("maze must be of a rectangle shape")
    return array


def get_neighbors(current: tuple, maze: np.ndarray, wall: str) -> list:
    """
    Get coordinates of all valid neighboring cells.

    Parameters
    ----------
    current : tuple
      The (x, y) values of the current cell.
    maze : np.ndarray
      Array representation of the maze
    wall : str
      Character representing a wall.
      Walls are not valid neighbors.

    Returns
    -------
    list
      list of tuples for all neighboring cells.

    Examples
    -------
    >>> maze = "s..x\n.x..\n.xxe"
    >>> get_neighbors((1,3), maze, 'x')
    [(1,2), (2,3)]
    """
    h, w = maze.shape
    x, y = current
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # check cell is within maze and not a wall
    # valid_indices should probably be it's own function
    def is_valid(x, y): return (x >= 0 and x < h) and (
        y >= 0 and y < w) and (maze[x, y] != wall)
    return [(x + dx, y + dy) for (dx, dy) in offsets if is_valid(x + dx, y + dy)]


def get_indices(value: str, maze: np.ndarray):
  # I shouldn't raise exceptions here as it makes the function less reusable.
  # I did it this way just to keep the solvable function cleaner - sorry
    """
    Get the indices of a given character from a numpy array.

    Note: raises an exception if value not found or more than one found.

    Parameters
    ----------
    value : str
      character to find
    maze : np.ndarray
      Array representation of the maze

    Returns
    -------
    tuple
      The indices of the given value

    Examples
    -------
    >>> maze = "s..x\n.x..\n.xxe"
    >>> get_neighbors((1,3), maze, 'x')
    [(1,2), (2,3)]
    """
    indices = np.where(maze == value)
    if len(indices[0]) != 1:
        raise ValueError(f"maze must contain exactly one {value} character")
    return indices


def manhattan_distance(cell1: tuple, cell2: tuple) -> int:
    """
    Calculates the Manhattan distance of two cells.

    Parameters
    ----------
    cell1 : tuple
      (x,y) cell indices 
    cell2 : np.ndarray
      (x,y) cell indices 

    Returns
    -------
    int
      The Manhattan distance of two cells

    Examples
    -------
    >>> manhattan_distance((2,3), (7,10))
    12
    """
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def solvable(maze_str: str, start: str = 's', end: str = 'e', wall: str = 'x') -> bool:
    """
    Checks if a given maze is solvable.

    Only checks non-diagonal moves.

    Parameters
    ----------
    maze_str : str
      String representation of a maze.
      Maze needs to be a rectangle and should have exactly
      one starting and one ending point.
    start : str
      Character indicating the starting point.
      Defaults to 's'.
    end : str
      Character indicating the ending point.
      Defaults to 'e'.
    end : str
      Character indicating walls.
      Defaults to 'x'.

    Returns
    -------
    bool
      True if the maze is solvable, otherwise False.

    Examples
    -------
    >>> solvable("sxe\n...")
    True

    >>> solvable("sxe\nx..")
    False
    """
    # these functions raise exceptions if maze setup is incorrect
    # this needs to be heavily refactored!
    maze = parse_maze(maze_str)
    initial = get_indices(start, maze)
    goal = get_indices(end, maze)

    # use PriorityQueue manhattan_distance to
    # prioritize exploring paths that are closest to the goal
    def scored(current): return (manhattan_distance(current, goal), current)
    queue = PriorityQueue()

    visited = []
    queue.put(scored(initial))
    while not queue.empty():
        _, current = queue.get()
        visited.append(current)
        neighbors = get_neighbors(current, maze, wall)
        # maze if solvable if goal coordinates is a valid neighbor
        if goal in neighbors:
            return True
        [queue.put(scored(cell)) for cell in neighbors if cell not in visited]

    # maze unsolvable if all paths in queue have been exhausted
    return False
