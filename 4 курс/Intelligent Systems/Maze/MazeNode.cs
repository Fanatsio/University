using System.Windows;

namespace Maze
{
    public class Node
    {
        public Point Position { get; }

        public Node(Point position)
        {
            Position = position;
        }
    }
}
