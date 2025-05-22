using Avalonia.Controls;

namespace SafetySystem.Views
{
    public partial class RouteControlWindow : Window
    {
        public RouteControlWindow()
        {
            InitializeComponent();
        }

        private void OnCloseWindow(object sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            this.Close();
        }
    }
}