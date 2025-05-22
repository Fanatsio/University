namespace Kod
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.TextBox = new System.Windows.Forms.TextBox();
            this.resDataGridView = new System.Windows.Forms.DataGridView();
            this.Column1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Column2 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.StartButton = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.label9 = new System.Windows.Forms.Label();
            this.ShIlabel = new System.Windows.Forms.Label();
            this.ShDlabel = new System.Windows.Forms.Label();
            this.ShHlabel = new System.Windows.Forms.Label();
            this.HafILabel = new System.Windows.Forms.Label();
            this.HafHlabel = new System.Windows.Forms.Label();
            this.HafDlabel = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.label1 = new System.Windows.Forms.Label();
            this.TextLoadButton = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.resDataGridView)).BeginInit();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.SuspendLayout();
            // 
            // TextBox
            // 
            resources.ApplyResources(this.TextBox, "TextBox");
            this.TextBox.Name = "TextBox";
            // 
            // resDataGridView
            // 
            resources.ApplyResources(this.resDataGridView, "resDataGridView");
            this.resDataGridView.AllowUserToAddRows = false;
            this.resDataGridView.AllowUserToDeleteRows = false;
            this.resDataGridView.AllowUserToResizeColumns = false;
            this.resDataGridView.AllowUserToResizeRows = false;
            this.resDataGridView.BackgroundColor = System.Drawing.Color.White;
            this.resDataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.resDataGridView.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Column1,
            this.Column2});
            this.resDataGridView.Name = "resDataGridView";
            this.resDataGridView.RowHeadersVisible = false;
            // 
            // Column1
            // 
            resources.ApplyResources(this.Column1, "Column1");
            this.Column1.Name = "Column1";
            this.Column1.ReadOnly = true;
            // 
            // Column2
            // 
            resources.ApplyResources(this.Column2, "Column2");
            this.Column2.Name = "Column2";
            this.Column2.ReadOnly = true;
            // 
            // StartButton
            // 
            resources.ApplyResources(this.StartButton, "StartButton");
            this.StartButton.Name = "StartButton";
            this.StartButton.UseVisualStyleBackColor = true;
            this.StartButton.Click += new System.EventHandler(this.Button1_Click);
            // 
            // groupBox1
            // 
            resources.ApplyResources(this.groupBox1, "groupBox1");
            this.groupBox1.Controls.Add(this.label9);
            this.groupBox1.Controls.Add(this.ShIlabel);
            this.groupBox1.Controls.Add(this.ShDlabel);
            this.groupBox1.Controls.Add(this.ShHlabel);
            this.groupBox1.ForeColor = System.Drawing.Color.White;
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.TabStop = false;
            // 
            // label9
            // 
            resources.ApplyResources(this.label9, "label9");
            this.label9.Name = "label9";
            // 
            // ShIlabel
            // 
            resources.ApplyResources(this.ShIlabel, "ShIlabel");
            this.ShIlabel.Name = "ShIlabel";
            // 
            // ShDlabel
            // 
            resources.ApplyResources(this.ShDlabel, "ShDlabel");
            this.ShDlabel.Name = "ShDlabel";
            // 
            // ShHlabel
            // 
            resources.ApplyResources(this.ShHlabel, "ShHlabel");
            this.ShHlabel.Name = "ShHlabel";
            // 
            // HafILabel
            // 
            resources.ApplyResources(this.HafILabel, "HafILabel");
            this.HafILabel.Name = "HafILabel";
            // 
            // HafHlabel
            // 
            resources.ApplyResources(this.HafHlabel, "HafHlabel");
            this.HafHlabel.Name = "HafHlabel";
            // 
            // HafDlabel
            // 
            resources.ApplyResources(this.HafDlabel, "HafDlabel");
            this.HafDlabel.Name = "HafDlabel";
            // 
            // label8
            // 
            resources.ApplyResources(this.label8, "label8");
            this.label8.Name = "label8";
            // 
            // groupBox2
            // 
            resources.ApplyResources(this.groupBox2, "groupBox2");
            this.groupBox2.Controls.Add(this.label8);
            this.groupBox2.Controls.Add(this.HafILabel);
            this.groupBox2.Controls.Add(this.HafHlabel);
            this.groupBox2.Controls.Add(this.HafDlabel);
            this.groupBox2.ForeColor = System.Drawing.Color.White;
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.TabStop = false;
            // 
            // label1
            // 
            resources.ApplyResources(this.label1, "label1");
            this.label1.ForeColor = System.Drawing.Color.White;
            this.label1.Name = "label1";
            // 
            // TextLoadButton
            // 
            resources.ApplyResources(this.TextLoadButton, "TextLoadButton");
            this.TextLoadButton.Name = "TextLoadButton";
            this.TextLoadButton.UseVisualStyleBackColor = true;
            this.TextLoadButton.Click += new System.EventHandler(this.Button2_Click);
            // 
            // Form1
            // 
            resources.ApplyResources(this, "$this");
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoValidate = System.Windows.Forms.AutoValidate.EnablePreventFocusChange;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.Controls.Add(this.TextLoadButton);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.StartButton);
            this.Controls.Add(this.resDataGridView);
            this.Controls.Add(this.TextBox);
            this.Name = "Form1";
            this.ShowIcon = false;
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.WindowState = System.Windows.Forms.FormWindowState.Minimized;
            ((System.ComponentModel.ISupportInitialize)(this.resDataGridView)).EndInit();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox TextBox;
        private System.Windows.Forms.DataGridView resDataGridView;
        private System.Windows.Forms.Button StartButton;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Label ShIlabel;
        private System.Windows.Forms.Label ShDlabel;
        private System.Windows.Forms.Label ShHlabel;
        private System.Windows.Forms.Label HafILabel;
        private System.Windows.Forms.Label HafHlabel;
        private System.Windows.Forms.Label HafDlabel;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column1;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column2;
        private System.Windows.Forms.Button TextLoadButton;
    }
}

