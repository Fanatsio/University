using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Shapes;

namespace Maze
{
    public class MazeSolver
    {
        public int[,] Cells { get; private set; }
        public int CellSize { get; private set; }

        public MazeSolver(int[,] cells, int cellSize)
        {
            Cells = cells;
            CellSize = cellSize;
        }

        public void Draw(Canvas canvas)
        {
            canvas.Children.Clear();

            for (int i = 0; i < Cells.GetLength(0); i++)
            {
                for (int j = 0; j < Cells.GetLength(1); j++)
                {
                    Rectangle rect = new()
                    {
                        Width = CellSize,
                        Height = CellSize,
                        Stroke = Brushes.Black,
                        Fill = Cells[i, j] switch
                        {
                            0 => Brushes.White,
                            1 => Brushes.Black,
                            2 => Brushes.Blue,
                            3 => Brushes.Red,
                            _ => Brushes.Transparent
                        }
                    };
                    Canvas.SetLeft(rect, j * CellSize);
                    Canvas.SetTop(rect, i * CellSize);
                    canvas.Children.Add(rect);
                }
            }
        }

        public int[,] GetCells()
        {
            return Cells;
        }
        public void SetCells(int[,] cells)
        {
            Cells = cells;
        }

        public Brush ToggleCell(int x, int y)
        {
            // Меняем состояние ячейки
            Cells[y, x] = Cells[y, x] == 1 ? 0 : 1;

            // Возвращаем цвет в зависимости от нового состояния ячейки
            return Cells[y, x] == 1 ? Brushes.Black : Brushes.White;
        }

        public Point FindPoint(int value)
        {
            for (int i = 0; i < Cells.GetLength(0); i++)
            {
                for (int j = 0; j < Cells.GetLength(1); j++)
                {
                    if (Cells[i, j] == value)
                        return new Point(j, i);
                }
            }
            return new Point(-1, -1);
        }

    public List<Point> FindAllStarts()
    {
        List<Point> starts = new();
        for (int i = 0; i < Cells.GetLength(0); i++)
        {
            for (int j = 0; j < Cells.GetLength(1); j++)
            {
                if (Cells[i, j] == 2) // Предположим, что 2 обозначает стартовые точки
                {
                    starts.Add(new Point(j, i)); // j - по оси X, i - по оси Y
                }
            }
        }
        return starts;
    }

    public List<Point> FindAllExits()
    {
        List<Point> exits = new();
        for (int i = 0; i < Cells.GetLength(0); i++)
        {
            for (int j = 0; j < Cells.GetLength(1); j++)
            {
                if (Cells[i, j] == 3) // Предположим, что 3 обозначает выходы
                {
                    exits.Add(new Point(j, i)); // j - по оси X, i - по оси Y
                }
            }
        }
        return exits;
    }

    public static void ClearHighlights(Canvas canvas)
        {
            foreach (var child in canvas.Children.OfType<Rectangle>())
            {
                if (child.Fill == Brushes.Yellow || child.Fill == Brushes.Green)
                {
                    child.Fill = Brushes.White;
                }
            }
        }
    }
}

