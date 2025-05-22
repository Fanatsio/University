namespace Lab2.Library
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
            TNumber result;
            Figure<TNumber> figure;

            if (is3DFigure)
            {
                figure = new Prism<TNumber>(testData[0], testData[1]);
            }
            else
            {
                figure = new Trapezoid<TNumber>(testData[0], testData[1], testData[2], testData[3]);
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
            TNumber result;
            Figure<TNumber> figure;

            if (is3DFigure)
            {
                figure = new Prism<TNumber>(testData[0], testData[1]);
            }
            else
            {
                figure = new Trapezoid<TNumber>(testData[0], testData[1], testData[2], testData[3]);
            }

            figure.CalculateSquareEvent += CalculateEvent;
            result = figure.CalculateSquare();
            figure.Save();
            figure.CalculateSquareEvent -= CalculateEvent;

            eventCounter = localEventCounter;
            return result;
        }

        public static TNumber CalculateVolume<TNumber>(bool is3DFigure, TNumber[] testData, ref uint eventCounter) where TNumber : INumber<TNumber>
        {
            TNumber result;
            Figure<TNumber> figure;

            if (is3DFigure)
            {
                figure = new Prism<TNumber>(testData[0], testData[1]);
            }
            else
            {
                figure = new Trapezoid<TNumber>(testData[0], testData[0], testData[0], testData[0]);
            }

            figure.CalculateVolumeEvent += CalculateEvent;
            result = figure.CalculateVolume();
            figure.Save();
            figure.CalculateVolumeEvent -= CalculateEvent;

            eventCounter = localEventCounter;
            return result;
        }
    }
}