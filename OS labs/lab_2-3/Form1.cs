namespace lab_3
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            CheckForIllegalCrossThreadCalls = false;
            button1.Click += Button1_Click;
        }

        Mutex mutexObj = new();
        private Random r = new();
        int i = 0;
        int xInitial = 385;
        int yInitial = 191;
        void Moving()
        {
            mutexObj.WaitOne();
            int x = r.Next(701);
            int y = r.Next(421);
            button1.Location = new Point(x, y);
            string b = button1.Location.ToString();
            textBox2.Text = b;
            i++;
            button1.Text = i.ToString();
            Count(x, y);
            mutexObj.ReleaseMutex();
        }

        void Count(int xCurrent, int yCurrent)
        {
            int xResult = Math.Abs(xCurrent - xInitial);
            int yResult = Math.Abs(yCurrent - yInitial);
            textBox3.Text = xResult.ToString();
            textBox4.Text = yResult.ToString();
            xInitial = xCurrent;
            yInitial = yCurrent;
        }

        void Result()
        {
            string resultX = textBox3.Text;
            string resultY = textBox4.Text;
            textBox3.Text = resultX;
            textBox4.Text = resultY;
        }

        private void Button1_Click(object? sender, EventArgs e)
        {
            textBox1.Text = button1.Location.ToString();
            Thread one = new(Moving);
            one.Start();
            Thread two = new(Result);
            two.Start();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}