#include "lab04_sqlite.h"

#include <gtk/gtk.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define UI_FILE "lab04.glade"

enum
{
    CHILD_ID = 0,
    FIO,
    DATE,
    POL,
    DOC_ID,
    DOC,
    SERT_ID,
    SERT
};

struct MainWindowObjects
{
    GtkWindow *main_window;
    GtkTreeView *treeview;
    GtkListStore *liststore;
    GtkAdjustment *adjustment;
    GtkTreeViewColumn *column_child_id;
    GtkTreeViewColumn *column_fio;
    GtkTreeViewColumn *column_date;
    GtkTreeViewColumn *column_pol;
    GtkTreeViewColumn *column_doc_id;
    GtkTreeViewColumn *column_sert_id;
    GtkTextView *lbl_fio;
    GtkTextView *lbl_date;
    GtkTextView *lbl_pol;
    GtkTextView *lbl_doc;
    GtkTextView *lbl_sert;
} mainWindowObjects;

int flag = 1;

int callback(void *not_used, int argc, char **argv, char **col_names)
{
    GtkTreeIter iter;
    
    if (argc == 8)
    {
        gtk_list_store_append(GTK_LIST_STORE(mainWindowObjects.liststore), &iter);
        gtk_list_store_set(GTK_LIST_STORE(mainWindowObjects.liststore), &iter, CHILD_ID,
                           atoi(argv[CHILD_ID]), FIO, argv[FIO], DATE, argv[DATE], POL, argv[POL],
                           DOC_ID, atoi(argv[DOC_ID]), DOC, argv[DOC], SERT_ID, atoi(argv[SERT_ID]), SERT, argv[SERT], -1);
    }
    return 0;
}



int main(int argc, char **argv)
{
    GtkBuilder *builder;
    GError *error = NULL;
    gtk_init(&argc, &argv);

    builder = gtk_builder_new();

    if (!gtk_builder_add_from_file(builder, UI_FILE, &error))
    {
        g_warning("%s\n", error->message);
        g_free(error);
        return (1);
    }

    mainWindowObjects.main_window = GTK_WINDOW(gtk_builder_get_object(builder, "main_window"));
    mainWindowObjects.treeview =
        GTK_TREE_VIEW(gtk_builder_get_object(builder, "treeview_components"));
    mainWindowObjects.liststore =
        GTK_LIST_STORE(gtk_builder_get_object(builder, "liststore_components"));

    mainWindowObjects.column_fio =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_fio"));

    mainWindowObjects.column_date =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_date"));
    mainWindowObjects.column_pol =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_pol"));
    mainWindowObjects.column_child_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_child_id"));
    mainWindowObjects.column_doc_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_doc_id"));
    mainWindowObjects.column_sert_id =
        GTK_TREE_VIEW_COLUMN(gtk_builder_get_object(builder, "cln_sert_id"));
    mainWindowObjects.lbl_fio = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_fio"));
    mainWindowObjects.lbl_date = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_date"));
    mainWindowObjects.lbl_pol = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_pol"));
    mainWindowObjects.lbl_doc = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_doc"));
    mainWindowObjects.lbl_sert = GTK_TEXT_VIEW(gtk_builder_get_object(builder, "lbl_sert"));
    gtk_builder_connect_signals(builder, &mainWindowObjects);
    
    g_object_unref(G_OBJECT(builder));
    gtk_widget_show_all(GTK_WIDGET(mainWindowObjects.main_window));

    sqlite_get_data(1);

    gtk_main();
}

G_MODULE_EXPORT void on_btnsave_clicked(GtkWidget *button, gpointer data)
{
    GtkTreeIter iter;
    gboolean reader =
        gtk_tree_model_get_iter_first(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter);
    while (reader)
    {
         
        gint childid;
        gchar *fio;
        gchar *date;
        gchar *pol;
        gint doc_id;
        gint sert_id;
        
        gtk_tree_model_get(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter, CHILD_ID, &childid,
                           FIO, &fio, DATE, &date, POL, &pol, DOC_ID, &doc_id, SERT_ID, &sert_id, -1);
        sqlite_update(childid, fio, date, pol, doc_id, sert_id);
        reader = gtk_tree_model_iter_next(GTK_TREE_MODEL(mainWindowObjects.liststore), &iter);
    }
    gtk_list_store_clear(mainWindowObjects.liststore);
    sqlite_get_data(1);
}

G_MODULE_EXPORT void on_btn_add_clicked(GtkWidget *button, gpointer data)
{
    int doc_id, sert_id;
    GtkTextIter start, end;
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_fio);
    gchar *fio, *date, *pol, *doc, *sert;
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    fio = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_date);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    date = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_pol);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    pol = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_doc);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    doc = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    buffer = gtk_text_view_get_buffer(mainWindowObjects.lbl_sert);
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    sert = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    if (!strcmp(sert, "1236")) sert_id = 3;
        else if (!strcmp(sert, "1235")) sert_id = 2;
        else sert_id = 1;
    if (!strcmp(doc, "Колпаков Дмитрий Романович")) doc_id = 3;
        else if (!strcmp(doc, "Амелин Максим Евгеньевич")) doc_id = 2;
        else doc_id = 1;
    sqlite_insert(fio, date, pol, doc_id, sert_id);
    gtk_list_store_clear(GTK_LIST_STORE(mainWindowObjects.liststore));
    sqlite_get_data(1);
}

G_MODULE_EXPORT void on_btn_del_clicked(GtkWidget *button, gpointer data)
{
    GList *_list;
	GtkTreeIter iter;
	GtkTreeModel *model;
	GtkTreeSelection *sel;


	sel = gtk_tree_view_get_selection(mainWindowObjects.treeview);

	for(_list = gtk_tree_selection_get_selected_rows(sel, &model); _list; _list = g_list_next(_list))
	{
		GtkTreePath *path = _list->data;
		int child_id;

		gtk_tree_model_get_iter(model, &iter, path);
		gtk_tree_model_get(model, &iter, CHILD_ID, &child_id, -1);
        sqlite_delete(child_id);
	}

	g_list_foreach(_list, (GFunc)gtk_tree_path_free, NULL);
	g_list_free(_list);
    gtk_list_store_clear(GTK_LIST_STORE(mainWindowObjects.liststore));
    sqlite_get_data(1);
}

G_MODULE_EXPORT void on_fio_edited(GtkCellRendererText *renderer, gchar *path,
                                                         gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, FIO, new_text, -1);
    }
}

G_MODULE_EXPORT void on_date_edited(GtkCellRendererText *renderer, gchar *path,
                                                         gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, DATE, new_text, -1);
    }
}

G_MODULE_EXPORT void on_pol_edited(GtkCellRendererText *renderer, gchar *path,
                                                         gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, POL, new_text, -1);
    }
}

G_MODULE_EXPORT void on_doc_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        int id;
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (!strcmp(new_text, "Иванов Иван Иванович")) id = 1;
        else if (!strcmp(new_text, "Амелин Максим Евгеньевич")) id = 2;
        else id = 3;
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, DOC, new_text, DOC_ID, id, -1);
    }
}

G_MODULE_EXPORT void on_sert_edited(GtkCellRendererText *renderer, gchar *path,
                                                      gchar *new_text, gpointer data)
{
    if (g_ascii_strcasecmp(new_text, "") != 0)
    {
        int id;
        GtkTreeIter iter;
        GtkTreeModel *model;
        model = gtk_tree_view_get_model(mainWindowObjects.treeview);
        if (!strcmp(new_text, "1234")) id = 1;
        else if (!strcmp(new_text, "1235")) id = 2;
        else id = 3;
        if (gtk_tree_model_get_iter_from_string(model, &iter, path))
            gtk_list_store_set(GTK_LIST_STORE(model), &iter, SERT, new_text, SERT_ID, id, -1);
    }
}

G_MODULE_EXPORT void on_show_hidden_toggled(GtkToggleButton *button, gpointer data)
{
    if (!flag)
    {
        flag = 1;
        gtk_list_store_clear(GTK_LIST_STORE(mainWindowObjects.liststore));
        sqlite_get_data(flag);
    }
    else{
        flag = 0;
        gtk_list_store_clear(GTK_LIST_STORE(mainWindowObjects.liststore));
        sqlite_get_data(flag);
    }
}

G_MODULE_EXPORT void on_btnabout_clicked(GtkButton *button, gpointer data)
{
    GtkWidget *dialog = gtk_dialog_new_with_buttons(
        "О программе", mainWindowObjects.main_window,
        GTK_DIALOG_MODAL | GTK_DIALOG_DESTROY_WITH_PARENT, "_OK", GTK_RESPONSE_NONE, NULL);
    GtkWidget *content_area = gtk_dialog_get_content_area(GTK_DIALOG(dialog));
    gtk_container_set_border_width(GTK_CONTAINER(content_area), 15);
    GtkWidget *label = gtk_label_new("\nРазработчик: Максим Амелин\n");
    gtk_container_add(GTK_CONTAINER(content_area), label);
    gtk_widget_show(label);
    gtk_dialog_run(GTK_DIALOG(dialog));
    gtk_widget_destroy(dialog);
}

G_MODULE_EXPORT void on_window_destroy(GtkWidget *window, gpointer data)
{
    gtk_main_quit();
}

G_MODULE_EXPORT void on_btnexit_clicked(GtkWidget *window, gpointer data)
{
    gtk_main_quit();
}
