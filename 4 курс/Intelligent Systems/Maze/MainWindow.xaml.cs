using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Shapes;

namespace Maze
{
    public partial class MainWindow : Window
    {
        private readonly MazeSolver maze;
        private readonly MazeController mazeController;
        private List<List<Point>> allPaths = new();
        private int currentPathIndex = 0;
        private bool isEditing = false;

        public MainWindow()
        {
            InitializeComponent();

            int[,] mazeArray = {
                { 2, 0, 0, 0, 0, 0, 0, 0, 0, 3 },
                { 0, 1, 1, 0, 1, 1, 1, 1, 0, 1 },
                { 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 },
                { 0, 1, 1, 0, 1, 0, 1, 1, 1, 0 },
                { 0, 0, 0, 0, 0, 0, 1, 0, 1, 0 },
                { 1, 0, 1, 1, 3, 0, 1, 1, 3, 0 },
                { 0, 0, 1, 1, 1, 0, 1, 1, 1, 0 },
                { 0, 1, 1, 1, 1, 0, 1, 1, 0, 0 },
                { 0, 0, 0, 0, 1, 0, 1, 0, 0, 1 },
                { 1, 0, 1, 3, 0, 0, 0, 0, 1, 1 }
            };

            int cellSize = 40;
            maze = new MazeSolver(mazeArray, cellSize);
            mazeController = new MazeController(maze);
            maze.Draw(MazeCanvas);
        }

        private void ImportButton_Click(object sender, RoutedEventArgs e)
        {
            var fileDialog = new Microsoft.Win32.OpenFileDialog
            {
                Filter = "Text files (*.txt)|*.txt"
            };

            if (fileDialog.ShowDialog() == true)
            {
                _ = new MazeFileHandler();
                int[,]? loadedMaze = MazeFileHandler.LoadMazeFromTxt(fileDialog.FileName);

                if (loadedMaze != null)
                {
                    maze.SetCells(loadedMaze);
                    maze.Draw(MazeCanvas);
                }
            }
        }

        private void ExportButton_Click(object sender, RoutedEventArgs e)
        {
            var fileDialog = new Microsoft.Win32.SaveFileDialog
            {
                Filter = "Text files (*.txt)|*.txt"
            };

            if (fileDialog.ShowDialog() == true)
            {
                _ = new MazeFileHandler();
                MazeFileHandler.SaveMazeToTxt(maze.Cells, fileDialog.FileName);
            }
        }

        private void FindAllPaths_Click(object sender, RoutedEventArgs e)
        {
            MazeSolver.ClearHighlights(MazeCanvas);
            List<Point> starts = maze.FindAllStarts();
            List<Point> ends = maze.FindAllExits();

            if (starts.Any(start => start == new Point(-1, -1)) ||  ends == null ||  ends.Count == 0)
    {
                RouteInfo.Text = "Старт или конец не найдены!";
                return;
            }

            allPaths.Clear();
            allPaths = mazeController.FindAllPaths(starts, ends);

            var sortedPaths = allPaths.OrderBy(path => path.Count).ToList();

            PathsListBox.Items.Clear();
            for (int i = 0; i < sortedPaths.Count; i++)
            {
                var path = sortedPaths[i];
                int length = path.Count;
                PathsListBox.Items.Add($"Маршрут [{i + 1}] ({length})");
            }

            RouteInfo.Text = sortedPaths.Count == 0 ? "Пути не найдены!" : $"Найдено путей: {sortedPaths.Count}";
        }

        private void PathsListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (PathsListBox.SelectedItem != null)
            {
                MazeSolver.ClearHighlights(MazeCanvas);

                int selectedIndex = PathsListBox.SelectedIndex;

                if (selectedIndex >= 0 && selectedIndex < allPaths.Count)
                {
                    var selectedPath = allPaths[selectedIndex];
                    HighlightPath(selectedPath, "Yellow");
                }
            }
        }

        private void HighlightPath(List<Point> path, string color)
        {
            foreach (var point in path)
            {
                var child = MazeCanvas.Children
                    .OfType<Rectangle>()
                    .FirstOrDefault(r => Canvas.GetLeft(r) == point.X * maze.CellSize && Canvas.GetTop(r) == point.Y * maze.CellSize);

                if (child != null && (child.Fill != Brushes.Blue && child.Fill != Brushes.Red))
                {
                    child.Fill = color == "Yellow" ? Brushes.Yellow : Brushes.Green;
                }
            }
        }

        private void FindShortestPath_Click(object sender, RoutedEventArgs e)
        {
            if (allPaths.Count == 0)
            {
                RouteInfo.Text = "Сначала найдите все пути!";
                return;
            }

            MazeSolver.ClearHighlights(MazeCanvas);
            List<Point> starts = maze.FindAllStarts();
            List<Point> ends = maze.FindAllExits();

            allPaths.Clear();
            allPaths = mazeController.FindAllPaths(starts, ends);

            var sortedPaths = allPaths.OrderBy(path => path.Count).ToList();

            PathsListBox.Items.Clear();
            for (int i = 0; i < sortedPaths.Count; i++)
            {
                var path = sortedPaths[i];
                int length = path.Count;
                PathsListBox.Items.Add($"Маршрут [{i + 1}] ({length})");
            }

            allPaths = allPaths.OrderBy(p => p.Count).ToList();
            currentPathIndex = 0;
            HighlightPath(allPaths[currentPathIndex], "Green");
            RouteInfo.Text = $"Показан кратчайший путь. Длина: {allPaths[0].Count}";
        }

        private void ShowNextRoute_Click(object sender, RoutedEventArgs e)
        {
            if (allPaths.Count == 0)
            {
                RouteInfo.Text = "Сначала найдите все пути!";
                return;
            }

            MazeSolver.ClearHighlights(MazeCanvas);
            currentPathIndex = (currentPathIndex + 1) % allPaths.Count;
            HighlightPath(allPaths[currentPathIndex], "Yellow");
            RouteInfo.Text = $"Маршрут {currentPathIndex + 1} из {allPaths.Count}";
        }

        private void EditMaze_Click(object sender, RoutedEventArgs e)
        {
            isEditing = !isEditing;

            RouteInfo.Text = isEditing ? "Редактирование включено" : "Редактирование завершено";
            if (isEditing)
            {
                EditButton.Content = "Готово";
                AddClickHandlers();
            }
            else
            {
                EditButton.Content = "Изменить конфигурацию лабиринта";
                RemoveClickHandlers();
            }
        }

        private void AddClickHandlers()
        {
            foreach (Rectangle rect in MazeCanvas.Children.OfType<Rectangle>())
            {
                rect.MouseDown += Cell_MouseDown;
            }

            ToggleButtonsVisibility(true);
        }

        private void RemoveClickHandlers()
        {
            foreach (Rectangle rect in MazeCanvas.Children.OfType<Rectangle>())
            {
                rect.MouseDown -= Cell_MouseDown;
            }

            ToggleButtonsVisibility(false);
        }

        private void ToggleButtonsVisibility(bool isEditing)
        {
            AllPathsButton.Visibility = isEditing ? Visibility.Hidden : Visibility.Visible;
            ShortestRouteButton.Visibility = isEditing ? Visibility.Hidden : Visibility.Visible;
            NextRouteButton.Visibility = isEditing ? Visibility.Hidden : Visibility.Visible;
            ImportButton.Visibility = isEditing ? Visibility.Hidden : Visibility.Visible;
            ExportButton.Visibility = isEditing ? Visibility.Hidden : Visibility.Visible;
            PathsListBox.Visibility = isEditing ? Visibility.Hidden : Visibility.Visible;
        }

        private void DoneButton_Click(object sender, RoutedEventArgs e)
        {
            MazeSolver.ClearHighlights(MazeCanvas);
            isEditing = false;
            RouteInfo.Text = "Редактирование завершено.";
            RemoveClickHandlers();
        }

        private void Cell_MouseDown(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            if (sender is Rectangle rect)
            {
                int y = (int)(Canvas.GetLeft(rect) / maze.CellSize);
                int x = (int)(Canvas.GetTop(rect) / maze.CellSize);

                int selectedType = int.TryParse(((ComboBoxItem)CellTypeComboBox.SelectedItem)?.Tag?.ToString(), out int result) ? result : 0;

                Debug.WriteLine($"Выбранный тип:{selectedType}");

                int currentType = maze.Cells[x, y];

                if (currentType == selectedType)
                {
                    maze.Cells[x, y] = 0;
                    rect.Fill = Brushes.White;

                    Debug.WriteLine($"Ячейка изменена: ({x}, {y}) -> Тип:0");
                }
                else
                {
                    maze.Cells[x, y] = selectedType;

                    rect.Fill = selectedType switch
                    {
                        0 => Brushes.White, // Пустая клетка
                        1 => Brushes.Black, // Стена
                        2 => Brushes.Blue, // Вход
                        3 => Brushes.Red, // Выход
                        _ => Brushes.Transparent // Цвет по умолчанию
                    };

                    Debug.WriteLine($"Ячейка изменена: ({x}, {y}) -> Тип: {maze.Cells[x, y]}");
                }
            }
        }
    }
}