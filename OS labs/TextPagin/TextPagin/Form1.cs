namespace TextPagin
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            dataGridView1.Columns.Add("Id", "Номер");
            dataGridView1.Columns.Add("Contetnt", "Значение");
        }

        private void buttonRun_Click(object sender, EventArgs e)
        {
            String textFile = "";
            String line;
            try
            {
                StreamReader sr = new StreamReader(textPathFile.Text.Trim());
                line = sr.ReadLine();
                while (line != null)
                {
                    textFile += line;
                    line = sr.ReadLine();
                }
                sr.Close();
                Console.ReadLine();
            }
            catch
            {
                MessageBox.Show("Ошибка при попытке прочитать файл");
                return;
            }

            if (textFile.Length == 0)
            {
                MessageBox.Show("Пустой файл");
                return;
            }

            dataGridView1.Rows.Clear();            

            int blockLength;
            try
            {
               blockLength = Int32.Parse(textCount.Text.ToLower().Trim());
            }
            catch 
            {
                MessageBox.Show("В поле count нужно ввести число");
                return;
            }

            string block;
            string resultFind = "";
            string findValue = textSearch.Text.ToLower();
            int index = 0;

            for (int i = 0; i < textFile.Length; i += blockLength)
            {
                if (textFile.Length - i > blockLength)
                    block = textFile.Substring(i, blockLength);
                else
                    block = textFile.Substring(i, textFile.Length - i);

                index++;
                dataGridView1.Rows.Add((index).ToString(), block);

                if (block.Contains(findValue))
                {
                    resultFind += index.ToString() + " ";
                }
            }

            textBox1.Text = resultFind;
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }
    }
}