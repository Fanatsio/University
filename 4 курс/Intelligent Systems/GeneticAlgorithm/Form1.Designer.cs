namespace GeneticAlgorithm
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            List_of_things = new DataGridView();
            Column6 = new DataGridViewTextBoxColumn();
            Column1 = new DataGridViewTextBoxColumn();
            Column2 = new DataGridViewTextBoxColumn();
            Column4 = new DataGridViewTextBoxColumn();
            Column3 = new DataGridViewTextBoxColumn();
            Column5 = new DataGridViewTextBoxColumn();
            label5 = new Label();
            start = new Button();
            label3 = new Label();
            Sum = new TextBox();
            label1 = new Label();
            label4 = new Label();
            Count_it = new TextBox();
            label6 = new Label();
            ((System.ComponentModel.ISupportInitialize)List_of_things).BeginInit();
            SuspendLayout();
            // 
            // List_of_things
            // 
            List_of_things.AllowUserToAddRows = false;
            List_of_things.AllowUserToDeleteRows = false;
            List_of_things.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
            List_of_things.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            List_of_things.Columns.AddRange(new DataGridViewColumn[] { Column6, Column1, Column2, Column4, Column3, Column5 });
            List_of_things.Location = new Point(0, 0);
            List_of_things.Margin = new Padding(4);
            List_of_things.Name = "List_of_things";
            List_of_things.RowHeadersVisible = false;
            List_of_things.RowHeadersWidth = 70;
            List_of_things.Size = new Size(700, 367);
            List_of_things.TabIndex = 1;
            List_of_things.CellEndEdit += List_of_things_CellEndEdit;
            // 
            // Column6
            // 
            Column6.HeaderText = "№";
            Column6.Name = "Column6";
            // 
            // Column1
            // 
            Column1.HeaderText = "Наименование продукта";
            Column1.Name = "Column1";
            Column1.Width = 180;
            // 
            // Column2
            // 
            Column2.HeaderText = "Минимальное Количество";
            Column2.Name = "Column2";
            // 
            // Column4
            // 
            Column4.HeaderText = "Максимальное Количество";
            Column4.Name = "Column4";
            // 
            // Column3
            // 
            Column3.HeaderText = "Цена за единицу";
            Column3.Name = "Column3";
            // 
            // Column5
            // 
            Column5.HeaderText = "Конечное Количество";
            Column5.Name = "Column5";
            // 
            // label5
            // 
            label5.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            label5.AutoSize = true;
            label5.BackColor = SystemColors.Control;
            label5.Location = new Point(13, 473);
            label5.Margin = new Padding(4, 0, 4, 0);
            label5.Name = "label5";
            label5.Size = new Size(86, 15);
            label5.TabIndex = 17;
            label5.Text = "Вышло итого:";
            // 
            // start
            // 
            start.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            start.BackColor = SystemColors.Control;
            start.Location = new Point(170, 532);
            start.Margin = new Padding(4);
            start.Name = "start";
            start.Size = new Size(190, 32);
            start.TabIndex = 16;
            start.Text = "Решить";
            start.UseVisualStyleBackColor = true;
            start.Click += Start_Click;
            // 
            // label3
            // 
            label3.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            label3.AutoSize = true;
            label3.BackColor = SystemColors.Control;
            label3.Location = new Point(13, 409);
            label3.Margin = new Padding(4, 0, 4, 0);
            label3.Name = "label3";
            label3.Size = new Size(57, 15);
            label3.TabIndex = 14;
            label3.Text = "Бюджет:";
            // 
            // Sum
            // 
            Sum.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            Sum.Location = new Point(150, 409);
            Sum.Margin = new Padding(4);
            Sum.Name = "Sum";
            Sum.Size = new Size(246, 21);
            Sum.TabIndex = 12;
            Sum.KeyPress += Sum_KeyPress;
            // 
            // label1
            // 
            label1.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            label1.AutoSize = true;
            label1.BackColor = SystemColors.Control;
            label1.Location = new Point(13, 384);
            label1.Margin = new Padding(4, 0, 4, 0);
            label1.Name = "label1";
            label1.Size = new Size(0, 15);
            label1.TabIndex = 10;
            // 
            // label4
            // 
            label4.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            label4.AutoSize = true;
            label4.BackColor = SystemColors.Control;
            label4.Location = new Point(13, 498);
            label4.Margin = new Padding(4, 0, 4, 0);
            label4.Name = "label4";
            label4.Size = new Size(0, 15);
            label4.TabIndex = 21;
            // 
            // Count_it
            // 
            Count_it.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            Count_it.Location = new Point(150, 438);
            Count_it.Margin = new Padding(4);
            Count_it.Name = "Count_it";
            Count_it.Size = new Size(246, 21);
            Count_it.TabIndex = 22;
            // 
            // label6
            // 
            label6.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            label6.AutoSize = true;
            label6.BackColor = SystemColors.Control;
            label6.Location = new Point(13, 438);
            label6.Margin = new Padding(4, 0, 4, 0);
            label6.Name = "label6";
            label6.Size = new Size(109, 15);
            label6.TabIndex = 23;
            label6.Text = "Кол-во итераций:";
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(700, 577);
            Controls.Add(label6);
            Controls.Add(Count_it);
            Controls.Add(label4);
            Controls.Add(label5);
            Controls.Add(start);
            Controls.Add(label3);
            Controls.Add(Sum);
            Controls.Add(label1);
            Controls.Add(List_of_things);
            Font = new Font("Microsoft Sans Serif", 9F, FontStyle.Regular, GraphicsUnit.Point);
            Name = "Form1";
            Text = "Генетический алгоритм";
            Load += Form1_Load;
            ((System.ComponentModel.ISupportInitialize)List_of_things).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
        }

        #endregion

        private System.Windows.Forms.DataGridView List_of_things;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Button start;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox Sum;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox Count_it;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column6;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column1;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column2;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column4;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column3;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column5;
    }
}
