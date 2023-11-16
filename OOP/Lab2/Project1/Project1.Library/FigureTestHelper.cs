namespace Project1.Library
{
    public static class FigureTestHelper
    {
        private static uint localeventcounter = 0;
        public static TNumber CalculatePerimeter<TNumber>(bool is3DFigure, TNumber[] testData, ref uint eventCounter) where TNumber : INumber<TNumber>
        {
            // Выполнить расчет периметра для фигуры на основе входных данных.
            // Счетчик должен увеличиваться при каждом срабатывании событий. Каждое событие должно выполниться один раз.
            TNumber result;
            Figure<TNumber> figure;
            if (!is3DFigure)
            {
                figure = new Cylinder<TNumber>(testData[0], testData[1]);
            }
            else
            {
                figure = new Square<TNumber>(testData[0]);
            }
            figure.CalculatePerimeterEvent += Figure_CalculatePerimeterEvent;
            result = figure.CalculatePerimeter();
            figure.Save();
            figure.CalculatePerimeterEvent -= Figure_CalculatePerimeterEvent;
            eventCounter = localeventcounter;
            return result;
            static void Figure_CalculatePerimeterEvent(object? sender, EventArgs e)
            {
                localeventcounter++;
            }
        }

        public static TNumber CalculateSquare<TNumber>(bool is3DFigure, TNumber[] testData, ref uint eventCounter) where TNumber : INumber<TNumber>
        {
            // Выполнить расчет площади для фигуры на основе входных данных.
            // Счетчик должен увеличиваться при каждом срабатывании событий. Каждое событие должно выполниться один раз.

            TNumber result;
            Figure<TNumber> figure;

            if (!is3DFigure)
            {
                figure = new Square<TNumber>(testData[0]);
            }
            else
            {
                figure = new Cylinder<TNumber>(testData[0], testData[1]);
            }
            figure.CalculatePerimeterEvent += Figure_CalculateSquareEvent;
            result = figure.CalculateSquare();
            figure.Save();
            figure.CalculatePerimeterEvent -= Figure_CalculateSquareEvent;
            eventCounter = localeventcounter;
            return result;

            static void Figure_CalculateSquareEvent(object? sender, EventArgs e)
            {
                localeventcounter++;
            }
        }

        public static TNumber CalculateVolume<TNumber>(bool is3DFigure, TNumber[] testData, ref uint eventCounter) where TNumber : INumber<TNumber>
        {
            // Выполнить расчет объема для фигуры на основе входных данных.
            // Счетчик должен увеличиваться при каждом срабатывании событий. Каждое событие должно выполниться один раз.
            TNumber result;
            Figure<TNumber> figure;
            if (!is3DFigure)
            {
                figure = new Square<TNumber>(testData[0]);
            }
            else
            {
                figure = new Cylinder<TNumber>(testData[0], testData[1]);
            }
            figure.CalculatePerimeterEvent += Figure_CalculateVolumeEvent;
            result = figure.CalculateVolume();
            figure.Save();
            figure.CalculatePerimeterEvent -= Figure_CalculateVolumeEvent;
            eventCounter = localeventcounter;
            return result;
            static void Figure_CalculateVolumeEvent(object? sender, EventArgs e)
            {
                localeventcounter++;
            }
        }
    }
}