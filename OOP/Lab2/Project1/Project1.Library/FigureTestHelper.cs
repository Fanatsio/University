namespace Project1.Library
{
    public static class FigureTestHelper
    {
        private static uint localEventCounter = 0;

        public static void CalculateEvent(object? sender, EventArgs e)
        {
            localEventCounter++;
        }

        public static TNumber CalculatePerimeter<TNumber>(bool is3DFigure, TNumber[] testData, ref uint eventCounter) where TNumber : INumber<TNumber>
        {
            // Выполнить расчет периметра для фигуры на основе входных данных.
            // Счетчик должен увеличиваться при каждом срабатывании событий. Каждое событие должно выполниться один раз.
            TNumber result;
            Figure<TNumber> figure;

            if (is3DFigure)
            {
                figure = new Ellipsoid<TNumber>(testData[0], testData[1], testData[2]);
            }
            else
            {
                figure = new Ellipse<TNumber>(testData[0], testData[1]);
            }

            figure.CalculatePerimeterEvent += CalculateEvent;
            result = figure.CalculatePerimeter();
            figure.Save();
            figure.CalculatePerimeterEvent -= CalculateEvent;

            eventCounter = localEventCounter;
            return result;
        }

        public static TNumber CalculateSquare<TNumber>(bool is3DFigure, TNumber[] testData, ref uint eventCounter) where TNumber : INumber<TNumber>
        {
            // Выполнить расчет площади для фигуры на основе входных данных.
            // Счетчик должен увеличиваться при каждом срабатывании событий. Каждое событие должно выполниться один раз.
            TNumber result;
            Figure<TNumber> figure;

            if (is3DFigure)
            {
                figure = new Ellipsoid<TNumber>(testData[0], testData[1], testData[2]);
            }
            else
            {
                figure = new Ellipse<TNumber>(testData[0], testData[1]);
            }

            figure.CalculatePerimeterEvent += CalculateEvent;
            result = figure.CalculateSquare();
            figure.Save();
            figure.CalculatePerimeterEvent -= CalculateEvent;

            eventCounter = localEventCounter;
            return result;
        }

        public static TNumber CalculateVolume<TNumber>(bool is3DFigure, TNumber[] testData, ref uint eventCounter) where TNumber : INumber<TNumber>
        {
            // Выполнить расчет объема для фигуры на основе входных данных.
            // Счетчик должен увеличиваться при каждом срабатывании событий. Каждое событие должно выполниться один раз.
            TNumber result;
            Figure<TNumber> figure;

            if (is3DFigure)
            {
                figure = new Ellipsoid<TNumber>(testData[0], testData[1], testData[2]);
            }
            else
            {
                figure = new Ellipse<TNumber>(testData[0], testData[1]);
            }

            figure.CalculatePerimeterEvent += CalculateEvent;
            result = figure.CalculateVolume();
            figure.Save();
            figure.CalculatePerimeterEvent -= CalculateEvent;

            eventCounter = localEventCounter;
            return result;
        }
    }
}