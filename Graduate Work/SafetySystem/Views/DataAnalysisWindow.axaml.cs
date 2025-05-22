using Avalonia.Controls;

namespace SafetySystem.Views
{
    public partial class DataAnalysisWindow : Window
    {
        public DataAnalysisWindow()
        {
            InitializeComponent();
        }

        private void OnCloseWindow(object sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            this.Close();
        }
    }
}