using System.IO;
using System.Windows;
 
namespace Maze
{
    public class MazeFileHandler
    {
        public static int[,]? LoadMazeFromTxt(string filePath)
        {
            try
            {
                var lines = File.ReadAllLines(filePath);
                int rows = lines.Length;
                int cols = lines[0].Split(new char[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries).Length;

                int[,] maze = new int[rows, cols];

                for (int i = 0; i < rows; i++)
                {
                    var cells = lines[i].Split(new char[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
                    for (int j = 0; j < cols; j++)
                    {
                        maze[i, j] = int.Parse(cells[j]);
                    }
                }

                return maze;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при загрузке лабиринта: {ex.Message}");
                return null;
            }
        }

        public static void SaveMazeToTxt(int[,] maze, string filePath)
        {
            try
            {
                using (var writer = new StreamWriter(filePath))
                {
                    for (int i = 0; i < maze.GetLength(0); i++)
                    {
                        for (int j = 0; j < maze.GetLength(1); j++)
                        {
                            writer.Write(maze[i, j]);
                            if (j < maze.GetLength(1) - 1)
                            {
                                writer.Write(" ");
                            }
                        }
                        writer.WriteLine();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при сохранении лабиринта: {ex.Message}");
            }
        }
    }
}