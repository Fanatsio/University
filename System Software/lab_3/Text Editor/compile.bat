windres -i rds,rc -o outres.coff
gcc main.c outres.coff -lUser32 -lComdlg32 -lgdi32 -lMsimg32 -lComctl32 -o editor.exe -mwindows
