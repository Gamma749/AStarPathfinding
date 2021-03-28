# AStarPathfinding

## Running the Program
* This project needs `pygame`, so if you do not have this installed run `pip
  install pygame`
* Run `python main.py`
* Draw walls (or click the walls button to switch to erase mode)
* Click run to see the path finding in action
* At the top of `AStarPathfinding.py` there is a variable `h_const` that
  determines how much to weight the heuristic of A Star

A GUI based project to show some A* pathfinding in practice. This project will generate a GUI of a grid of squares, one of which is a source and one of which is a target. The user can then draw (using the mouse) walls, or click the state button (lower right) to erase walls instead. Finally, clicking the START button begins pathfinding, showing the decisions made by the algorithm using color.

# TODO
I think that adding functionality to change where the source/target are should be doable, I am just pondering how to implement this in an intuative way.

Making some parts of the code more efficent, specifically around some of the loops.
