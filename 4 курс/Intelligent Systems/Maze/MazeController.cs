using System.Diagnostics;
using System.Windows;

namespace Maze
{
    public class MazeController
    {
        private readonly MazeSolver maze;

        public MazeController(MazeSolver maze)
        {
            this.maze = maze;
        }

        public List<List<Point>> FindAllPaths(List<Point> starts, List<Point> ends)
        {
            List<List<Point>> allPaths = new();

            foreach (var start in starts)
            {
                Debug.WriteLine($"Start at: ({start.X}, {start.Y})");
                foreach (var end in ends)
                {
                    Debug.WriteLine($"Exit at: ({end.X}, {end.Y})");
                    FindAllPaths(start, end, new List<Point>(), allPaths);
                }
            }
            return allPaths;
        }

        private void FindAllPaths(Point current, Point end, List<Point> currentPath, List<List<Point>> allPaths)
        {
            currentPath.Add(current);

            if (current == end)
            {
                allPaths.Add(new List<Point>(currentPath));
            }
            else
            {
                foreach (var neighbor in GetNeighbors(new Node(current), maze.Cells.GetLength(0), maze.Cells.GetLength(1)))
                {
                    if (!currentPath.Contains(neighbor.Position))
                    {
                        FindAllPaths(neighbor.Position, end, currentPath, allPaths);
                    }
                }
            }

            currentPath.RemoveAt(currentPath.Count - 1);
        }

        private IEnumerable<Node> GetNeighbors(Node node, int rows, int cols)
        {
            var neighbors = new List<Node>();
            var directions = new Point[] { new(0, -1), new(0, 1), new(-1, 0), new(1, 0) };

            foreach (var direction in directions)
            {
                int newX = (int)node.Position.X + (int)direction.X;
                int newY = (int)node.Position.Y + (int)direction.Y;

                if (newX >= 0 && newX < cols && newY >= 0 && newY < rows && maze.Cells[newY, newX] != 1)
                {
                    neighbors.Add(new Node(new Point(newX, newY)));
                }
            }

            return neighbors;
        }
    }
}