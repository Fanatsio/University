namespace HorseStep
{
    public partial class Form1 : Form
    {
        private const int CellSize = 50;

        public Form1()
        {
            InitializeComponent();
        }

        private void DrawChessBoard(int width, int height, List<Point> path)
        {
            panel1.Controls.Clear();
            panel1.Size = new Size(width * CellSize + CellSize, height * CellSize + CellSize);

            AddColumnLabels(width);
            AddRowLabels(height);
            DrawCells(width, height, path);
        }

        private void AddColumnLabels(int width)
        {
            for (int col = 0; col < width; col++)
            {
                var colLabel = CreateLabel(CellSize + col * CellSize, 0, (col + 1).ToString());
                panel1.Controls.Add(colLabel);
            }
        }

        private void AddRowLabels(int height)
        {
            for (int row = 0; row < height; row++)
            {
                var rowLabel = CreateLabel(0, CellSize + row * CellSize, (row + 1).ToString());
                panel1.Controls.Add(rowLabel);
            }
        }

        private static Label CreateLabel(int x, int y, string text)
        {
            return new Label
            {
                Size = new Size(CellSize, CellSize),
                Location = new Point(x, y),
                Text = text,
                TextAlign = ContentAlignment.MiddleCenter,
                Font = new Font("Arial", 9),
                BackColor = Color.LightGray
            };
        }

        private void DrawCells(int width, int height, List<Point> path)
        {
            for (int row = 0; row < height; row++)
            {
                for (int col = 0; col < width; col++)
                {
                    var cell = new Panel
                    {
                        Size = new Size(CellSize, CellSize),
                        Location = new Point(CellSize + col * CellSize, CellSize + row * CellSize),
                        BackColor = (row + col) % 2 == 0 ? Color.White : Color.Black
                    };
                    panel1.Controls.Add(cell);

                    var point = new Point(col, row);
                    int stepNumber = path.IndexOf(point) + 1;
                    if (stepNumber > 0)
                    {
                        AddStepNumberToCell(cell, stepNumber);
                    }
                }
            }
        }

        private static void AddStepNumberToCell(Panel cell, int stepNumber)
        {
            var numberLabel = new Label
            {
                Size = new Size(CellSize, CellSize),
                Location = new Point(0, 0),
                Text = stepNumber.ToString(),
                ForeColor = Color.Red,
                TextAlign = ContentAlignment.MiddleCenter,
                Font = new Font("Arial", 9, FontStyle.Bold),
                BackColor = Color.Transparent
            };
            cell.Controls.Add(numberLabel);
        }

        private static List<Point> FindKnightTour(int boardWidth, int boardHeight, Point start)
        {
            var solver = new KnightTourSolver(boardWidth, boardHeight);
            return solver.Solve(start, out _);
        }

        private static bool IsBoardValid(int width, int height)
        {
            if (width > height) (width, height) = (height, width);

            if (width == 3 && (height < 4 || (height > 4 && height < 7)))
            {
                MessageBox.Show("Обход коня невозможен с текущими размерами доски. " +
                                "\nЕсли одна сторона равна 3, другая должна быть 4 или не меньше 7.");
                return false;
            }

            if (width == 4 && height == 4)
            {
                MessageBox.Show("Обход коня невозможен с текущими размерами доски. " +
                                "\nНа доске 4×4 решение невозможно.");
                return false;
            }

            if (height < 3 || width < 3)
            {
                MessageBox.Show("Обход коня невозможен с текущими размерами доски. " +
                                "\nСтороны должны быть больше 4");
                return false;
            }

            return true;
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            if (!TryGetBoardSize(out int width, out int height) ||
                !TryGetStartPosition(width, height, out Point start))
            {
                MessageBox.Show("Пожалуйста, введите корректные значения.");
                return;
            }

            if (!IsBoardValid(width, height)) return;

            var watch = System.Diagnostics.Stopwatch.StartNew();
            var path = FindKnightTour(width, height, start);
            watch.Stop();

            if (path.Count > 0)
            {
                DrawChessBoard(width, height, path);
                MessageBox.Show($"Решение найдено.\nВремя: {watch.ElapsedMilliseconds} мс\nКоличество шагов: {path.Count}");
            }
            else
            {
                MessageBox.Show("Решение не найдено. \nПопробуйте выбрать другую стартовую позицию.");
            }
        }

        private bool TryGetBoardSize(out int width, out int height)
        {
            height = 0;
            return int.TryParse(textBox1.Text, out width) && width > 0 &&
                   int.TryParse(textBox2.Text, out height) && height > 0;
        }

        private bool TryGetStartPosition(int width, int height, out Point start)
        {
            start = Point.Empty;
            if (!int.TryParse(textBox3.Text, out int startX) || startX < 1 || startX > width ||
                !int.TryParse(textBox4.Text, out int startY) || startY < 1 || startY > height)
            {
                return false;
            }
            start = new Point(startX - 1, startY - 1);
            return true;
        }
    }

    public class KnightTourSolver(int boardWidth, int boardHeight)
    {
        private readonly int _boardWidth = boardWidth;
        private readonly int _boardHeight = boardHeight;
        private readonly (int dx, int dy)[] _moves =
        {
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        };

        public List<Point> Solve(Point start, out int attempts)
        {
            attempts = 0;
            var path = new List<Point> { start };
            var visitedCells = new bool[_boardWidth, _boardHeight];
            visitedCells[start.X, start.Y] = true;

            int currentX = start.X;
            int currentY = start.Y;

            for (int step = 1; step < _boardWidth * _boardHeight; step++)
            {
                attempts++;
                var possibleMoves = GetValidMoves(currentX, currentY, visitedCells);

                if (!possibleMoves.Any())
                    return [];

                var (x, y) = possibleMoves
                    .OrderBy(m => GetDegree(m.x, m.y, visitedCells))
                    .First();

                currentX = x;
                currentY = y;
                path.Add(new Point(currentX, currentY));
                visitedCells[currentX, currentY] = true;
            }

            return path;
        }

        private IEnumerable<(int x, int y)> GetValidMoves(int x, int y, bool[,] visited)
        {
            foreach (var (dx, dy) in _moves)
            {
                int nextX = x + dx;
                int nextY = y + dy;
                if (IsValid(nextX, nextY, visited))
                {
                    yield return (nextX, nextY);
                }
            }
        }

        private bool IsValid(int x, int y, bool[,] visited) =>
            x >= 0 && x < _boardWidth && y >= 0 && y < _boardHeight && !visited[x, y];

        private int GetDegree(int x, int y, bool[,] visited)
        {
            return _moves.Count(move => IsValid(x + move.dx, y + move.dy, visited));
        }
    }
}
