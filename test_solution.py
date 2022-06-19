import unittest
from unittest.mock import patch
import numpy as np

from solution import parse_maze, get_neighbors, get_indices, manhattan_distance, solvable

# TODO: add setUp / tearDown, read more about python unit testing - this is horrible!


class TestParseMaze(unittest.TestCase):
    def test_is_string(self):
        """
        parse_maze fails when given a non-string parameter
        """
        self.assertRaises(TypeError, parse_maze, True)
        self.assertRaises(TypeError, parse_maze, [])

    def test_incorrect_string_shape(self):
        """
        parse_maze fails when maze isn't a rectangle
        """
        maze = """
        se
        ....
        """
        self.assertRaises(ValueError, parse_maze, maze)

    def test_shape(self):
        """
        parse_maze returns array has correct shape
        """
        maze = """
          sxe.
          ....
          xxx.
        """
        actual = parse_maze(maze)
        self.assertIsInstance(actual, np.ndarray)
        self.assertEqual(actual.shape, (3, 4))

    def test_values(self):
        """
        Test if returned array contains correct values
        """
        maze = """
          sxx
          ...
          xxe
        """
        actual = parse_maze(maze)
        self.assertEqual(actual[0, 0], 's')
        self.assertEqual(actual[2, 2], 'e')
        self.assertEqual(actual[1, 1], '.')


class TestGetNeighbors(unittest.TestCase):
    def test_all_directions(self):
        """
        get_neighbors returns top, bottom, left and right neighbors
        """
        maze = np.array([['.', '.', '.'],
                         ['.', '.', '.'],
                         ['.', '.', '.']])
        actual = get_neighbors((1, 1), maze, 'x')
        self.assertEqual(len(actual), 4)
        self.assertIn((0, 1), actual)
        self.assertIn((1, 2), actual)
        self.assertIn((1, 0), actual)
        self.assertIn((2, 1), actual)

    def test_edges(self):
        """
        get_neighbors correctly accounts for edges
        """
        maze = np.array([['.', '.'], ['.', '.']])
        top_left = get_neighbors((0, 0), maze, 'x')
        expected = [(0, 1), (1, 0)].sort()
        self.assertEqual(top_left.sort(), expected)
        bottom_right = get_neighbors((1, 1), maze, 'x')
        self.assertEqual(bottom_right.sort(), expected)

    def test_handles_walls(self):
        """
        get_neighbors doesn't return cells that are walls
        """
        maze = np.array([['.', 'x'], ['.', '.']])
        actual = get_neighbors((0, 0), maze, 'x')
        self.assertEqual(actual, [(1, 0)])


class TestGetIndices(unittest.TestCase):
    def test_not_found(self):
        """
        get_indices raises exception if value not in array
        """
        maze = np.array([['.']])
        self.assertRaises(ValueError, get_indices, 's', maze)

    def test_multiple(self):
        """
        get_indices raises exception if multiple values found
        """
        maze = np.array([['s', 's']])
        self.assertRaises(ValueError, get_indices, 's', maze)

    def test_correct(self):
        """
        get_indices returns the correct indices
        """
        maze = np.array([['.', 's'], ['.', 'e']])
        self.assertEqual(get_indices('s', maze), (0, 1))
        self.assertEqual(get_indices('e', maze), (1, 1))


class TestManhattanDistance(unittest.TestCase):
    def test_correct(self):
        self.assertEqual(manhattan_distance((1, 1), (3, 5)), 6)
        self.assertEqual(manhattan_distance((9, 7), (2, 4)), 10)


class TestSolvable(unittest.TestCase):
    # TODO: Mock other functions so just testing solvable logic
    # the tests below aren't good, but I didn't want to spend too much time
    def test_true(self):
        """
        solvable correctly returns true for solvable maps
        """
        maze = """
          xx.exx
          ...xxx
          .x....
          xxxx..
          x.x..s
        """
        self.assertTrue(solvable(maze))
        self.assertFalse(solvable("sxe"))

    def test_false(self):
        """
        solvable correctly returns false for unsolvable maps
        """
        self.assertFalse(solvable("sxe"))


if __name__ == '__main__':
    unittest.main()
