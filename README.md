# Solvable-Maze-Challenge

## How to use

### Solvable

1. Clone repository

2. Import the solvable function from solution.py into script

3. Call the solvable function with a maze string

```pyhton
maze = """
sxxxe
...x.
.xxx.
.....
"""
solvable(maze)
```

### Tests

```bash
python test_solution.py
```

---

## Resources / Process

I knew there was a lot of research around maze solving algorithms, so the first thing I did was to get a quick overview of different approaches ([Wikipedia](https://en.wikipedia.org/wiki/Maze-solving_algorithm), [astrolog.org](https://www.astrolog.org/labyrnth/algrithm.htm), and skimming a few quick stack overflow threads).

Of interest where BFS, DFS, Dijkstra's algorithm, A\*, and Recursive back-filling. I mainly used Wikipedia to get an idea of the worked and the pros/cons of the approaches.

After spending ~30 minutes on this I decided that it would be more fun and more in the spirit of the challenge to come up with my own approach, rather than to implement/modify a known algorithm. In saying that, I had just been reading about these other approaches so you can easily see their ‘influence’ _(e.g. using distance to goal)_.

I made the call to use the NumPy and queue libraries. For both libraries I made use of the docs.
For testing I used the unittest library, and again made use of the docs.

Writing and working out the core logic of the algorithm was done in under 2 hours. Adding tests took me a little over the 2 hours, and I don't know why but I then decided to add doc strings _(which don't add much/anything to such a simple project...)_. I probably should have spent that time redoing the testing!
