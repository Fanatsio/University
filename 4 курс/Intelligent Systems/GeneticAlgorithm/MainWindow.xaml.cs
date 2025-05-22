using System;
using System.ComponentModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace GeneticAlgorithm
{
    public partial class MainWindow : Window
    {
        private readonly Random random = new();
        private readonly Item[] items = new Item[50];
        private readonly int[] quantities = new int[50];

        public MainWindow()
        {
            InitializeComponent();
            InitializeItems();
            PopulateGrid();
            UpdatePriceRange();
        }

        // Класс для представления товара
        public class Item : INotifyPropertyChanged
        {
            private int _price;
            private int _minQuantity;
            private int _maxQuantity;
            private int _selectedQuantity;

            public int Number { get; set; }
            public string Name { get; set; }

            public int Price
            {
                get => _price;
                set
                {
                    if (value <= 0)
                        throw new ArgumentException("Цена должна быть положительной.");
                    _price = value;
                    OnPropertyChanged(nameof(Price));
                    OnPropertyChanged(nameof(TotalCost));
                }
            }

            public int MinQuantity
            {
                get => _minQuantity;
                set
                {
                    if (value <= 0)
                        throw new ArgumentException("Минимальное количество должно быть положительным.");
                    _minQuantity = value;
                    OnPropertyChanged(nameof(MinQuantity));
                    if (_maxQuantity < _minQuantity)
                        MaxQuantity = _minQuantity;
                    if (_selectedQuantity < _minQuantity)
                        SelectedQuantity = _minQuantity;
                }
            }

            public int MaxQuantity
            {
                get => _maxQuantity;
                set
                {
                    if (value < _minQuantity)
                        throw new ArgumentException("Максимальное количество должно быть не меньше минимального.");
                    _maxQuantity = value;
                    OnPropertyChanged(nameof(MaxQuantity));
                    if (_selectedQuantity > _maxQuantity)
                        SelectedQuantity = _maxQuantity;
                }
            }

            public int SelectedQuantity
            {
                get => _selectedQuantity;
                set
                {
                    _selectedQuantity = value;
                    OnPropertyChanged(nameof(SelectedQuantity));
                    OnPropertyChanged(nameof(TotalCost));
                }
            }

            public int TotalCost => Price * SelectedQuantity;

            public event PropertyChangedEventHandler PropertyChanged;
            protected void OnPropertyChanged(string propertyName)
            {
                PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
            }
        }

        // Инициализация товаров
        private void InitializeItems()
        {
            string[] names = new string[]
            {
                "Игрушечная машина", "Кукла", "Пазлы", "Мягкая игрушка", "Конструктор", "Книга", "Раскраска", "Фломастеры", "Мяч", "Скакалка",
                "Настольная игра", "Кубики", "Каляка-Маляка", "Детский рюкзак", "Робот-игрушка", "Лото", "Игровой набор", "Песочный набор", "Свинка-копилка", "Творческий набор",
                "Игрушечный телефон", "Музыкальная игрушка", "Трюмо детское", "Кухонный набор", "Детская палатка", "Самокат", "Велосипед", "Ролики", "Кукольный домик", "Детская посуда",
                "Мольберт", "Набор для рисования", "Пальчиковые краски", "Конструктор Лего", "Детский микроскоп", "Настольный футбол", "Детская машина на радиоуправлении", "Игровая консоль",
                "Качели", "Батут", "Детский бассейн", "Надувной круг", "Детские лыжи", "Санки", "Машинка-каталка", "Песочница", "Караоке-микрофон", "Лабиринт", "Рюкзак с игрушкой", "Развивающая игра"
            };

            // Генерация цен
            int[] prices = new int[50];
            for (int i = 0; i < 17; i++) prices[i] = random.Next(1, 10);
            for (int i = 17; i < 34; i++) prices[i] = random.Next(10, 100);
            for (int i = 34; i < 50; i++) prices[i] = random.Next(100, 1000);

            // Генерация мин/макс количеств
            for (int i = 0; i < 50; i++)
            {
                int min = random.Next(1, 5);
                int max = random.Next(min + 2, min + 6);
                items[i] = new Item
                {
                    Number = i + 1,
                    Name = names[i],
                    Price = prices[i],
                    MinQuantity = min,
                    MaxQuantity = max,
                    SelectedQuantity = random.Next(min, max + 1)
                };
                this.quantities[i] = items[i].SelectedQuantity;
            }
        }

        // Заполнение таблицы
        private void PopulateGrid()
        {
            ItemsGrid.ItemsSource = null;
            ItemsGrid.ItemsSource = items;
        }

        // Обновление диапазона цен
        private void UpdatePriceRange()
        {
            int minPrice = items.Sum(item => item.Price * item.MinQuantity);
            int maxPrice = items.Sum(item => item.Price * item.MaxQuantity);
            PriceRangeLabel.Text = $"Диапазон цен: от {minPrice} до {maxPrice}";
        }

        // Валидация ввода чисел
        private void NumberValidation(object sender, TextCompositionEventArgs e)
        {
            e.Handled = !char.IsDigit(e.Text, 0);
        }

        // Валидация вставки текста
        private void NumberValidationPaste(object sender, DataObjectPastingEventArgs e)
        {
            if (e.DataObject.GetDataPresent(typeof(string)))
            {
                string text = (string)e.DataObject.GetData(typeof(string));
                if (!int.TryParse(text, out _))
                {
                    e.CancelCommand();
                }
            }
            else
            {
                e.CancelCommand();
            }
        }

        // Обработка редактирования ячейки
        private void ItemsGrid_CellEditEnding(object sender, DataGridCellEditEndingEventArgs e)
        {
            if (e.EditAction == DataGridEditAction.Commit)
            {
                var item = e.Row.Item as Item;
                var textBox = e.EditingElement as TextBox;
                if (textBox == null || item == null) return;

                try
                {
                    int value = int.Parse(textBox.Text);
                    string columnName = e.Column.Header.ToString();

                    switch (columnName)
                    {
                        case "Цена за шт.":
                            item.Price = value;
                            break;
                        case "Мин. кол-во":
                            item.MinQuantity = value;
                            break;
                        case "Макс. кол-во":
                            item.MaxQuantity = value;
                            break;
                    }
                }
                catch (ArgumentException ex)
                {
                    MessageBox.Show(ex.Message, "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    e.Cancel = true;
                }
                catch
                {
                    MessageBox.Show("Введите корректное число!", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    e.Cancel = true;
                }

                UpdatePriceRange();
            }
        }

        // Обработчик кнопки "Запустить"
        private void StartButton_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(TargetSum.Text) || string.IsNullOrEmpty(Iterations.Text))
            {
                MessageBox.Show("Введите сумму и количество итераций!", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            if (!int.TryParse(TargetSum.Text, out int targetSum) || targetSum <= 0 || targetSum > 1_000_000)
            {
                MessageBox.Show("Введите корректную сумму (1–1,000,000)!", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            if (!int.TryParse(Iterations.Text, out int iterations) || iterations <= 0 || iterations > 100_000)
            {
                MessageBox.Show("Введите корректное количество итераций (1–100,000)!", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            // Генетический алгоритм
            (int[] bestSolution, int usedIterations, bool isPerfect) = RunGeneticAlgorithm(targetSum, iterations);

            // Обновление выбранных количеств
            for (int i = 0; i < 50; i++)
            {
                items[i].SelectedQuantity = bestSolution[i];
            }

            // Обновление таблицы и диапазона цен
            PopulateGrid();
            UpdatePriceRange();

            // Вывод результатов
            int finalSum = items.Sum(item => item.TotalCost);
            int difference = Math.Abs(finalSum - targetSum);
            ResultSumLabel.Text = $"Итоговая сумма: {finalSum}";
            DifferenceLabel.Text = $"Разница с желаемой суммой: {difference}";
            IterationResultLabel.Text = isPerfect
                ? $"Найдено идеальное решение на итерации {usedIterations}"
                : $"Идеальное решение не найдено, использовано итераций: {usedIterations}";
        }

        // Генетический алгоритм
        private (int[] bestSolution, int usedIterations, bool isPerfect) RunGeneticAlgorithm(int targetSum, int maxIterations)
        {
            const int populationSize = 10;
            int[][] population = new int[populationSize][];
            int[] fitnesses = new int[populationSize];

            // Инициализация популяции
            for (int i = 0; i < populationSize; i++)
            {
                population[i] = new int[50];
                for (int j = 0; j < 50; j++)
                {
                    population[i][j] = random.Next(items[j].MinQuantity, items[j].MaxQuantity + 1);
                }
                fitnesses[i] = CalculateFitness(population[i], targetSum);
            }

            int[] bestSolution = (int[])population[0].Clone();
            int bestFitness = fitnesses[0];
            int usedIterations = 0;
            bool isPerfect = false;

            for (int iter = 0; iter < maxIterations; iter++)
            {
                usedIterations = iter + 1;

                // Создание новой популяции
                int[][] newPopulation = new int[populationSize][];
                newPopulation[0] = (int[])population[Array.IndexOf(fitnesses, fitnesses.Min())].Clone(); // Элитизм: сохраняем лучшую особь

                for (int i = 1; i < populationSize; i++)
                {
                    // Турнирный отбор
                    int parent1 = TournamentSelection(fitnesses);
                    int parent2 = TournamentSelection(fitnesses);

                    // Одноточечное скрещивание
                    newPopulation[i] = Crossover(population[parent1], population[parent2]);

                    // Мутация
                    Mutate(newPopulation[i]);
                }

                // Оценка новой популяции
                for (int i = 0; i < populationSize; i++)
                {
                    fitnesses[i] = CalculateFitness(newPopulation[i], targetSum);
                    if (fitnesses[i] < bestFitness)
                    {
                        bestFitness = fitnesses[i];
                        bestSolution = (int[])newPopulation[i].Clone();
                    }
                }

                // Проверка на точное совпадение
                if (bestFitness == 0)
                {
                    isPerfect = true;
                    break;
                }

                population = newPopulation;
            }

            return (bestSolution, usedIterations, isPerfect);
        }

        // Турнирный отбор
        private int TournamentSelection(int[] fitnesses)
        {
            const int tournamentSize = 3;
            int bestIndex = random.Next(fitnesses.Length);
            int bestFitness = fitnesses[bestIndex];

            for (int i = 1; i < tournamentSize; i++)
            {
                int index = random.Next(fitnesses.Length);
                if (fitnesses[index] < bestFitness)
                {
                    bestFitness = fitnesses[index];
                    bestIndex = index;
                }
            }

            return bestIndex;
        }

        // Одноточечное скрещивание
        private int[] Crossover(int[] parent1, int[] parent2)
        {
            int[] child = new int[50];
            int crossoverPoint = random.Next(1, 49);

            for (int i = 0; i < crossoverPoint; i++)
            {
                child[i] = parent1[i];
            }
            for (int i = crossoverPoint; i < 50; i++)
            {
                child[i] = parent2[i];
            }

            return child;
        }

        // Мутация
        private void Mutate(int[] individual)
        {
            const double mutationRate = 0.05;
            for (int i = 0; i < 50; i++)
            {
                if (random.NextDouble() < mutationRate)
                {
                    individual[i] = random.Next(items[i].MinQuantity, items[i].MaxQuantity + 1);
                }
            }
        }

        // Вычисление приспособленности
        private int CalculateFitness(int[] solution, int targetSum)
        {
            int total = 0;
            for (int i = 0; i < 50; i++)
            {
                total += solution[i] * items[i].Price;
            }
            return Math.Abs(total - targetSum);
        }
    }
}