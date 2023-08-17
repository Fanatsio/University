#include <windows.h>
#include <strsafe.h>
#include <commctrl.h>
#include <stdarg.h>

#define NEW_FILE_NAME L"Пустой файл"
#define WM_USER_CARETMOVE (WM_USER+0)
#define ACC_EDIT_DELETEWORD 0

enum linebreak {
    LINEBREAK_UNIX,
    LINEBREAK_WIN
};

enum encoding {
    ENCODING_UTF8,
    ENCODING_UTF16
};

struct format {
    enum encoding encoding;
    enum linebreak linebreak;
    BOOL bom;
};

CONST struct format Internal_format = {
    .encoding = ENCODING_UTF16,
    .linebreak = LINEBREAK_WIN,
    .bom = FALSE
};

CONST struct format Default_format = {
    .encoding = ENCODING_UTF8,
    .bom = FALSE,
    .linebreak = LINEBREAK_WIN
};

struct bom { UINT32 data; SIZE_T size; };

static HWND Window = NULL;
static INT Width = 640, Height = 480;

static struct {
    HFONT editor, filename;
} Fonts;

enum Gui_Enums {
    GUI_TEXT_BOX, GUI_STATIC_TEXT,
    GUI_MENU_NEW, GUI_MENU_LOAD, GUI_MENU_SAVE, GUI_MENU_ABOUT, GUI_MENU_WWRAP
};

static struct {
    HWND text_box, filename, status;
    HMENU menu, menu_file, menu_edit, menu_help;
    HACCEL edit_accels;
} Gui;

static struct {
    INT filename_height, margin, reduced_margin;
} Layout;

static struct {
    struct format format;
    BOOL is_new;
} Settings;

static void error_box_winerror(PCWSTR caption) {
    CONST DWORD err = GetLastError();
    WCHAR buf[128];
    if (FAILED(StringCbPrintfW(buf, sizeof(buf), L"%ls\n%d (0x%X)", caption, err, err)))
        StringCbCopyW(buf, sizeof(buf), L"Failed to format the error message");
    
    MessageBoxW(Window, 
                buf,
                L"Unexpected error",
                MB_OK | MB_ICONERROR | MB_DEFBUTTON1 | MB_APPLMODAL);

}

static void fatal(PCWSTR caption) {
    error_box_winerror(caption);
    ExitProcess(GetLastError());
}

static void error_box(PCWSTR caption, PCWSTR msg) {
    MessageBoxW(Window, 
               msg,
               caption,
               MB_OK | MB_ICONERROR | MB_DEFBUTTON1 | MB_APPLMODAL);
}

static void error_box_format(PCWSTR caption, PCWSTR msg, ...) {
    va_list args;
    va_start(args, msg);
    WCHAR buf[256];
    if (FAILED(StringCbVPrintfW(buf, sizeof(buf), msg, args)))
        StringCbCopyW(buf, sizeof(buf), L"Failed to format the error message");
    MessageBoxW(Window, 
               buf,
               caption,
               MB_OK | MB_ICONERROR | MB_DEFBUTTON1 | MB_APPLMODAL);
    va_end(args);    
}

static void resize_status_bar() {
    INT sizes[4] = {
        max(Width-330, 1), 
        max(Width-230, 1), 
        max(Width-130, 1), 
        -1
    };
    SendMessageW(Gui.status, SB_SETPARTS, (WPARAM)4, (LPARAM)sizes);
    SendMessageW(Gui.status, WM_SIZE, 0, 0);
}

static HWND add_status_bar() {
    HWND sbar = CreateWindowW(
            STATUSCLASSNAMEW,
            L"",
            WS_CHILD | WS_VISIBLE | SBARS_SIZEGRIP,
            0, 0, 0, 0,
            Window,
            NULL,
            (HINSTANCE)GetWindowLongPtr(Window, GWLP_HINSTANCE),
            NULL
        );
    if (!sbar)
        fatal(L"Failed to create the status bar");

    return sbar;
}

static void change_format(CONST struct format format) {
    Settings.format = format;
    static PCWSTR encodings[] = {
        [ENCODING_UTF8 ] = L"UTF-8",
        [ENCODING_UTF16] = L"UTF-16"
    };

    WCHAR buf[128];
    StringCbPrintfW(buf, sizeof(buf), L"%ls%ls", encodings[Settings.format.encoding], Settings.format.bom ? L" with BOM" : L"");
    SendMessageW(Gui.status, SB_SETTEXTW, 3, (LPARAM)buf);

    StringCbPrintfW(buf, sizeof(buf), L"%ls", Settings.format.linebreak == LINEBREAK_UNIX ? L"Unix (LF)" : L"Windows (CRLF)");
    SendMessageW(Gui.status, SB_SETTEXTW, 2, (LPARAM)buf);
}

static void change_status_pos(CONST ULONGLONG row, CONST ULONGLONG col) {
    WCHAR buf[128];
    StringCbPrintfW(buf, sizeof(buf), L"Ln %llu, Col %llu", row, col);
    SendMessageW(Gui.status, SB_SETTEXTW, 1, (LPARAM)buf);
}

static LRESULT CALLBACK EditProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_KEYDOWN:
        case WM_LBUTTONDOWN:
        case WM_LBUTTONUP:  
        case EM_SETSEL:
        case WM_CLEAR:
            PostMessageW(Window, WM_USER_CARETMOVE, MAKEWPARAM(GetDlgCtrlID(hwnd), 0), (LPARAM)hwnd);
        break;
        case WM_COMMAND:
            switch(HIWORD(wParam)) {
                case 1:
                    switch (LOWORD(wParam)) {
                        case ACC_EDIT_DELETEWORD: {                                
                            HLOCAL textH = (HLOCAL)SendMessageW(hwnd, EM_GETHANDLE, 0, 0);
                            PCWSTR text = LocalLock(textH);
                            CONST ULONGLONG text_length = GetWindowTextLengthW(hwnd);

                            DWORD sel_start, sel_end;
                            SendMessageW(hwnd, EM_GETSEL, (WPARAM)&sel_start, (LPARAM)&sel_end);
                            if (sel_start != sel_end) {
                                SendMessageW(hwnd, WM_CLEAR, 0, 0);
                                break;
                            }

                            ULONGLONG start = sel_start;
                            for (; start > 0 && iswspace(text[start-1]); start--);
                            for (; start > 0 && !iswspace(text[start-1]); start--);

                            SendMessageW(hwnd, WM_SETREDRAW, FALSE, 0);
                                SendMessageW(hwnd, EM_SETSEL, start, sel_start);
                                SendMessageW(hwnd, WM_CLEAR, 0, 0);
                            SendMessageW(hwnd, WM_SETREDRAW, TRUE, 0);

                            LocalUnlock(textH);

                            return 0;
                        } break;
                    }
                break;
            }
        break;
    }
    return CallWindowProcW((WNDPROC)GetWindowLongPtrW(hwnd, GWLP_USERDATA), hwnd, uMsg, wParam, lParam);
}

static HWND add_text_box(CONST UINT id, CONST BOOL wrap) {
    HWND text_box = CreateWindowExW(
        WS_EX_CLIENTEDGE,
        WC_EDITW,
        L"",
        WS_CHILD | WS_VISIBLE | WS_BORDER | ES_MULTILINE | WS_VSCROLL | (wrap ? ES_AUTOHSCROLL | WS_HSCROLL : 0),
        0,0,0,0,
        Window,
        (HMENU)(UINT_PTR)id,
        (HINSTANCE)GetWindowLongPtr(Window, GWLP_HINSTANCE),
        NULL
    );
    if (!text_box)
        fatal(L"Failed to create the text box");
    SendMessageW(text_box, WM_SETFONT, (WPARAM)Fonts.editor, TRUE);
    SetWindowLongPtrW(text_box, GWLP_USERDATA, (LONG_PTR)SetWindowLongPtrW(text_box, GWLP_WNDPROC, (LONG_PTR)EditProc));
    return text_box;
}

static HWND add_static_text(CONST UINT id) {
    HWND static_text = CreateWindowW(
        WC_STATICW,
        L"",
        WS_CHILD | WS_VISIBLE | SS_SIMPLE,
        0, 0, 0, 0,
        Window,
        (HMENU)(UINT_PTR)id,
        (HINSTANCE)GetWindowLongPtr(Window, GWLP_HINSTANCE),
        NULL
    );
    if (!static_text)
        fatal(L"Failed to create the static text");
    SendMessageW(static_text, WM_SETFONT, (WPARAM)Fonts.filename, TRUE);
    return static_text;
}

static void add_menu_button(HMENU menu, CONST UINT id, PCWSTR title) {
    MENUITEMINFOW info;
    info.cbSize = sizeof(MENUITEMINFOW);
    info.fMask = MIIM_STRING | MIIM_ID;
    info.wID = id;
    info.dwTypeData = (PWSTR)title;
    if (!(InsertMenuItemW(menu, GetMenuItemCount(menu), TRUE, &info)))
        fatal(L"Failed to insert the menu button");
}

static void add_menu_checkbox(HMENU menu, CONST UINT id, PCWSTR title) {
    MENUITEMINFOW info;
    info.cbSize = sizeof(MENUITEMINFOW);
    info.fMask = MIIM_STRING | MIIM_ID | MIIM_CHECKMARKS | MIIM_STATE;
    info.hbmpChecked = NULL;
    info.hbmpUnchecked = NULL;
    info.fState = MFS_UNCHECKED;
    info.wID = id;
    info.dwTypeData = (PWSTR)title;

    if (!InsertMenuItemW(menu, GetMenuItemCount(menu), TRUE, &info))
        fatal(L"Failed to insert a menu checkbox");
}

static void add_menu_submenu(HMENU menu, CONST HMENU submenu, PCWSTR title) {
    MENUITEMINFOW info;
    info.cbSize = sizeof(MENUITEMINFOW);
    info.fMask = MIIM_STRING | MIIM_SUBMENU;
    info.hSubMenu = submenu;
    info.dwTypeData = (PWSTR)title;

    if (!(InsertMenuItemW(menu, GetMenuItemCount(menu), TRUE, &info)))
        fatal(L"Failed to insert a menu submenu");
}

static void change_filename(PCWSTR fname) {
    SetWindowTextW(Gui.filename, fname);
    RECT wr;
    GetClientRect(Gui.filename, &wr);
    MapWindowPoints(Gui.filename, Window, (PPOINT)&wr, 2);
    InvalidateRect(Window, &wr, TRUE);
}

static void resize() {
    static BOOL b = 0;
    RECT status_rect;
    SendMessageW(Gui.status, SB_GETRECT, 0, (LPARAM)&status_rect);

    SetWindowPos(
        Gui.filename, NULL, 
        Layout.margin, 
        Layout.reduced_margin, 
        Width-Layout.margin*2, 
        Layout.filename_height,
        SWP_NOZORDER);
    SetWindowPos(Gui.text_box , NULL, 
        Layout.margin, 
        Layout.reduced_margin*2+Layout.filename_height, 
        Width-Layout.margin*2, 
        Height-Layout.reduced_margin*3-Layout.filename_height-(status_rect.bottom-status_rect.top), 
        SWP_NOZORDER);
    resize_status_bar(Gui.status);
}

static void toggle_wwrap() {
    BOOL wrap;
    {
        MENUITEMINFOW info;
        info.cbSize = sizeof(info);
        info.fMask = MIIM_STATE;
        GetMenuItemInfoW(Gui.menu_edit, GUI_MENU_WWRAP, FALSE, &info);
        wrap = info.fState & MFS_CHECKED;
        info.fState = (wrap ? MFS_UNCHECKED : MFS_CHECKED);
        if (!SetMenuItemInfoW(Gui.menu_edit, GUI_MENU_WWRAP, FALSE, &info))
            fatal(L"Toggle change word-wrap");
    }
    HWND newtbox = add_text_box(GUI_TEXT_BOX, wrap);

    {
        HLOCAL textH = (HLOCAL)SendMessage(Gui.text_box, EM_GETHANDLE, 0, 0);
        PCWSTR text = LocalLock(textH);
        SetWindowTextW(newtbox, text);
        LocalUnlock(textH);
    }

    DestroyWindow(Gui.text_box);
    Gui.text_box = newtbox;
    resize();
}

static PCWSTR choose_file(CONST BOOL save) {
    static WCHAR buf[512];
    static OPENFILENAMEW opts;
    opts.lStructSize = sizeof(OPENFILENAMEW);
    opts.hwndOwner = Window;
    opts.hInstance = (HINSTANCE)GetWindowLongPtr(Window, GWLP_HINSTANCE);
    opts.lpstrFilter = L"Text documents (*.txt)\0*.txt\0All files (*)\0*\0";
    opts.lpstrCustomFilter = NULL;
    opts.nFilterIndex = 2;
    opts.lpstrFile = buf;
    if (Settings.is_new)
        opts.lpstrFile[0] = L'\0';
    else
        GetWindowTextW(Gui.filename, opts.lpstrFile, sizeof(buf));
    opts.nMaxFile = sizeof(buf);
    opts.lpstrFileTitle = NULL;
    opts.lpstrInitialDir = NULL;
    opts.lpstrTitle = NULL;
    opts.nFileOffset = 0;
    opts.nFileExtension = 5;
    opts.lpstrDefExt = NULL;
    opts.FlagsEx = 0;

    if (save) {
        if (!GetSaveFileNameW(&opts)) return NULL;
    } else {
        if (!GetOpenFileNameW(&opts)) return NULL;
    }

    return opts.lpstrFile;
}

static CONST struct bom get_bom(CONST enum encoding encoding) {
    struct bom bom;
    switch (encoding) {
        case ENCODING_UTF16:
            bom.data = 0xFEFF;
            bom.size = 2;
        break;
        case ENCODING_UTF8:
            bom.data = 0xBFBBEF;
            bom.size = 3;
        break;
        default:
            bom.data = 0;
            bom.size = 0;
        break;
    }
    return bom;
}

static PVOID convert(PVOID src, CONST struct format from, CONST struct format to, CONST BOOL nullterm, CONST BOOL src_should_free, SIZE_T* new_size) {
    SIZE_T inter_size = 0;
    PWSTR inter = NULL;
    BOOL inter_should_free = FALSE;
    BOOL fail = FALSE;

    CONST struct bom from_bom = from.bom ? get_bom(from.encoding) : (struct bom){0};
    CONST struct bom to_bom   = to.bom   ? get_bom(to.encoding)   : (struct bom){0};

    switch (from.encoding) {
        case ENCODING_UTF16:
            inter = (PWSTR)((PBYTE)src + from_bom.size);
            inter_size = (lstrlenW((PCWSTR)src) + 1) * sizeof(WCHAR) - from_bom.size;
            inter_should_free = FALSE;
        break;
        case ENCODING_UTF8: {
            if (((PCHAR)src)[0] == '\0') {
                inter_size = sizeof(WCHAR);
                if (!(inter = HeapAlloc(GetProcessHeap(), 0, inter_size)))
                    fatal(L"Failed to allocate the conversion buffer");
                inter_should_free = TRUE;
                ((PWCHAR)inter)[0] = L'\0';
                break;
            }

            SIZE_T inter_length;
            if (!(inter_length = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, (PCHAR)src+from_bom.size, -1, NULL, 0))) {
                error_box_winerror(L"Invalid encoding");
                fail = TRUE;
                goto quit;
            }

            if (!(inter = HeapAlloc(GetProcessHeap(), 0, inter_length * sizeof(WCHAR))))
                fatal(L"Failed to allocate the conversion buffer");
            inter_should_free = TRUE;

            if (MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, (PCHAR)src+from_bom.size, -1, inter, inter_length) != inter_length) {
                error_box_winerror(L"Invalid encoding");
                fail = TRUE;
                goto quit;
            }

            inter_size = inter_length * sizeof(WCHAR);
        } break;
    }

    switch (to.linebreak) {
        case LINEBREAK_WIN: {
            SIZE_T newinter_length = 0;
            BOOL skip = TRUE;
            for (CONST WCHAR* wc = inter; *wc; wc++) {
                if (*wc == L'\n' && (wc-inter == 0 || *(wc-1) != L'\r')) {
                    skip = FALSE;
                    newinter_length++;
                }
                newinter_length++;
            }
            if (skip) break;
            PWSTR newinter;
            if (!(newinter = HeapAlloc(GetProcessHeap(), 0, (newinter_length + 1) * sizeof(WCHAR))))
                fatal(L"Failed to allocate the conversion buffer");
            {
                PWCHAR dc = newinter;
                CONST WCHAR* sc = inter;
                for (; *sc; dc++, sc++) {
                    if (*sc == L'\n' && (sc-inter == 0 || *(sc-1) != L'\r'))
                        *(dc++) = L'\r';
                    *dc = *sc; 
                }
                *dc = L'\0';
            }

            if (inter_should_free && !HeapFree(GetProcessHeap(), 0, inter))
                fatal(L"Failed to free the conversion buffer");

            inter = newinter;
            inter_size = (newinter_length + 1) * sizeof(WCHAR);
            inter_should_free = TRUE;
        } break;
        case LINEBREAK_UNIX: {
            SIZE_T newinter_length = 0;
            BOOL skip = TRUE;
            for (CONST WCHAR* wc = inter; *wc; wc++) {
                if (!wcsncmp(wc, L"\r\n", 2)) {
                    skip = FALSE;
                    newinter_length--;
                }

                newinter_length++;
            }

            if (skip) break;

            PWSTR newinter;
            if (!(newinter = HeapAlloc(GetProcessHeap(), 0, (newinter_length + 1) * sizeof(WCHAR))))
                fatal(L"Failed to allocate the conversion buffer");

            {
                PWCHAR dc = newinter;
                CONST WCHAR* sc = inter;
                for (; *sc; dc++, sc++) {
                    if (!wcsncmp(sc, L"\r\n", 2)) {
                        dc--;
                        continue;
                    }

                    *dc = *sc; 
                }
                *dc = L'\0';
            }

            if (inter_should_free && !HeapFree(GetProcessHeap(), 0, inter))
                fatal(L"Failed to free the conversion buffer");

            inter = newinter;
            inter_size = (newinter_length + 1) * sizeof(WCHAR);
            inter_should_free = TRUE;
        } break;
    }

    switch (to.encoding) {
        case ENCODING_UTF16: {
            
            SIZE_T newinter_size = inter_size + to_bom.size - (!nullterm)*sizeof(WCHAR);
            PVOID newinter;
            if (!(newinter = HeapAlloc(GetProcessHeap(), 0, newinter_size)))
                fatal(L"Failed to allocate the conversion buffer");

            memcpy(newinter, &to_bom.data, to_bom.size);
            memcpy((PBYTE)newinter + to_bom.size, inter, inter_size - (!nullterm)*sizeof(WCHAR));

            if (inter_should_free && !HeapFree(GetProcessHeap(), 0, inter))
                fatal(L"Failed to free the conversion buffer");

            inter = newinter;
            inter_size = newinter_size;
            inter_should_free = FALSE;
        } break;
        case ENCODING_UTF8: {

            SIZE_T newinter_size;
            PVOID newinter;

            if (inter[0] == L'\0') {
                newinter_size = nullterm ? sizeof(CHAR) : 0;
                if (!(newinter = HeapAlloc(GetProcessHeap(), 0, newinter_size)))
                    fatal(L"Failed to allocate the conversion buffer");

                if (nullterm) ((PCHAR)newinter)[0] = '\0';
            } else {
                if (!(newinter_size = WideCharToMultiByte(CP_UTF8, 0, inter, inter_size/sizeof(WCHAR)-(!nullterm), NULL, 0, NULL, NULL))) {
                    error_box_winerror(L"Invalid encoding");
                    fail = TRUE;
                    goto quit;
                }
                newinter_size += to_bom.size;

                if (!(newinter = HeapAlloc(GetProcessHeap(), 0, newinter_size)))
                    fatal(L"Failed to allocate the conversion buffer");

                memcpy(newinter, &to_bom.data, to_bom.size);
                if (WideCharToMultiByte(CP_UTF8, 0, inter, inter_size/sizeof(WCHAR)-(!nullterm), (PCHAR)newinter+to_bom.size, newinter_size-to_bom.size, NULL, NULL) != newinter_size-to_bom.size) {
                    error_box_winerror(L"Failed to convert the input string");
                    fail = TRUE;
                    goto quit;
                }
            }

            if (inter_should_free && !HeapFree(GetProcessHeap(), 0, inter))
                fatal(L"Failed to free the conversion buffer");

            inter = newinter;
            inter_size = newinter_size;
            inter_should_free = FALSE;
        } break;
    }

    quit:

    if (inter_should_free) {
        if (!HeapFree(GetProcessHeap(), 0, inter))
            fatal(L"Failed to free the conversion buffer");
        inter = NULL;
    }

    if (src_should_free && !HeapFree(GetProcessHeap(), 0, src))
        fatal(L"Failed to free the conversion buffer");

    if (new_size)
        *new_size = fail ? 0 : inter_size;

    return fail ? NULL : inter;
}

static CONST struct format get_format(LPCVOID src, CONST SIZE_T src_size) {

    struct format format = {0};

    if (IsTextUnicode(src, src_size, NULL)) {
        format.encoding = ENCODING_UTF16;
        CONST struct bom bom = get_bom(ENCODING_UTF16);
        if (src_size >= bom.size)
            format.bom = !memcmp(src, &bom.data, bom.size);
        format.linebreak = LINEBREAK_WIN;
        CONST WCHAR* start = (CONST WCHAR*)((PWSTR)src + (format.bom * bom.size));
        CONST WCHAR* wc = start;
        while (wc = wcschr(wc+1, L'\n')) {
            if (wc - start == 0 || *(wc-1) != L'\r') {
                format.linebreak = LINEBREAK_UNIX;
                break;
            }
        }
    } else {
        format.encoding = ENCODING_UTF8;
        CONST struct bom bom = get_bom(ENCODING_UTF8);
         if (src_size >= bom.size)
            format.bom = !memcmp(src, &bom.data, bom.size);
        format.linebreak = LINEBREAK_WIN;
        CONST CHAR* start = (CONST CHAR*)((PSTR)src + (format.bom * bom.size));
        CONST CHAR* c = start;
        while (c = strchr(c+1, '\n')) {
            if (c - start == 0 || *(c-1) != '\r') {
                format.linebreak = LINEBREAK_UNIX;
                break;
            }
        }

    }

    return format;
}

static void save_to_file(PCWSTR fpath) {
    if (!fpath) return;
    SIZE_T src_size = (GetWindowTextLengthW(Gui.text_box)+1)*sizeof(WCHAR);
    PVOID src;
    if (!(src = HeapAlloc(GetProcessHeap(), 0, src_size)))
        fatal(L"Failed to allocate the conversion buffer");
    GetWindowTextW(Gui.text_box, src, src_size/sizeof(WCHAR));

    src = convert(src, Internal_format, Settings.format, FALSE, TRUE, &src_size);
    if (!src) return;

    HANDLE out = CreateFileW(fpath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (out == INVALID_HANDLE_VALUE) {
        error_box_winerror(L"Failed to open the output file");
        return;
    }

    DWORD numwritten;
    if (!WriteFile(out, src, src_size, &numwritten, NULL) || numwritten != src_size)
        fatal(L"Failed to write into the output file");

    if (!CloseHandle(out)) 
        fatal(L"Failed to close file handle");
    
    change_filename(fpath);
    Settings.is_new = FALSE;
}

static void new_file() {
    SetWindowTextW(Gui.text_box, L"");
    change_filename(NEW_FILE_NAME);
    change_format(Default_format);
    change_status_pos(1, 1);
    Settings.is_new = TRUE;
}

static void load_from_file(PCWSTR fpath) {
    if (!fpath) return;

    HANDLE in = CreateFileW(   fpath,
                               GENERIC_READ,
                               0, NULL,
                               OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 
                               NULL);
    if (in == INVALID_HANDLE_VALUE) {
        error_box_winerror(L"Failed to open the input file");
        return;
    }

    BOOL fail = FALSE;

    LARGE_INTEGER filesize;
    if (!GetFileSizeEx(in, &filesize))
        fatal(L"Failed to retrieve file size");

    CONST SIZE_T src_size = filesize.QuadPart;

    CONST SIZE_T maxchars = SendMessageW(Gui.text_box, EM_GETLIMITTEXT, 0, 0);
    if (src_size > maxchars * sizeof(WCHAR)) {
        error_box_format(
            L"Ошибка открытия файла", 
            L"Файл слишком большой (%d Байт!) Максимальный размер %d Байт (%d символов)", 
            src_size, 
            maxchars * sizeof(WCHAR), 
            maxchars);
        fail = TRUE;
        goto quit;
    }

    PVOID src;
    if (!(src = HeapAlloc(GetProcessHeap(), 0, src_size+sizeof(WCHAR) )))
        fatal(L"Failed to allocate the read buffer");

    DWORD numread;
    if (!ReadFile(in, src, src_size, &numread, NULL) || numread != src_size)
        fatal(L"Failed to read the input file");
    memset((PBYTE)src+src_size, 0, sizeof(WCHAR));

    struct format source_format = get_format(src, src_size);
    change_format(source_format);

    PWSTR converted = convert(src, source_format, Internal_format, TRUE, TRUE, NULL);
    if (!converted) {
        fail = TRUE;
        goto quit;
    }

    SetWindowTextW(Gui.text_box, converted);

    if (!HeapFree(GetProcessHeap(), 0, converted))
        fatal(L"Failed to free the conversion buffer");

    quit:

    if (!CloseHandle(in)) 
        fatal(L"Failed to close the file handle");

    if (!fail) {
        change_filename(fpath);
        Settings.is_new = FALSE;
    }
}

static LRESULT CALLBACK WndProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {

    switch (uMsg) {
        case WM_CREATE:
            Window = hwnd;
            Layout.margin = 10;
            Layout.reduced_margin = 5;

            {
                Fonts.filename = GetStockObject(DEFAULT_GUI_FONT);
                Layout.filename_height = 15;

                LOGFONTW font = {0};
                StringCbCopyW(font.lfFaceName, LF_FACESIZE, L"Consolas");
                font.lfHeight = 14;
                Fonts.editor = CreateFontIndirectW(&font);
            }

            Gui.filename = add_static_text(GUI_STATIC_TEXT);

            Gui.text_box = add_text_box(GUI_TEXT_BOX, TRUE);
            SetFocus(Gui.text_box);

            Gui.menu = CreateMenu();
            Gui.menu_file = CreateMenu();
            add_menu_button(Gui.menu_file, GUI_MENU_NEW, L"Создать");
            add_menu_button(Gui.menu_file, GUI_MENU_LOAD, L"Открыть");
            add_menu_button(Gui.menu_file, GUI_MENU_SAVE, L"Сохранить");

            Gui.menu_help = CreateMenu();
            add_menu_button(Gui.menu_help, GUI_MENU_ABOUT, L"О программе");
            add_menu_submenu(Gui.menu, Gui.menu_file, L"Файл");
            add_menu_submenu(Gui.menu, Gui.menu_help, L"Справка");

            SetMenu(Window, Gui.menu);
            Gui.status = add_status_bar();
            resize_status_bar();
            resize();
            new_file();
            ShowWindow(Window, TRUE);
            UpdateWindow(Window);
        break;
        case WM_DESTROY:
            PostQuitMessage(0);
        break;
        case WM_CLOSE:
            DestroyWindow(hwnd);
        break;
        case WM_SIZE: {
            if (wParam == SIZE_MINIMIZED) break;
            Width = LOWORD(lParam);
            Height = HIWORD(lParam);
            resize();
        } break;
        case WM_GETMINMAXINFO: {
            PMINMAXINFO mmi = (PMINMAXINFO) lParam;
            mmi->ptMinTrackSize.x = 320;
            mmi->ptMinTrackSize.y = 240;

        } break; 
        case WM_CTLCOLORSTATIC: {
            HDC dc = (HDC)wParam;
            SetTextColor(dc, GetSysColor(COLOR_WINDOWTEXT));
            SetBkMode(dc, TRANSPARENT);
            return (LRESULT)GetStockObject(NULL_BRUSH);
        } break;
        case WM_USER_CARETMOVE : {
            ULONGLONG row = SendMessageW(Gui.text_box, EM_LINEFROMCHAR, -1, 0);
            DWORD start;
            SendMessageW(Gui.text_box, EM_GETSEL, (WPARAM)&start, (LPARAM)NULL);
            LONGLONG col;
            do {
                col = (LONGLONG)start - SendMessageW(Gui.text_box, EM_LINEINDEX, row, 0);
            } while (col < 0 && row--);

            change_status_pos(row+1, col+1);
        } break;
        case WM_COMMAND:
            switch (HIWORD(wParam)) {
                case 0:
                    switch (LOWORD(wParam)) {
                        case GUI_MENU_NEW: {
                            new_file();
                        } break;
                        case GUI_MENU_SAVE: {
                            PCWSTR fname = choose_file(TRUE);
                            save_to_file(fname);
                        } break;
                        case GUI_MENU_LOAD: {
                            PCWSTR fname = choose_file(FALSE);
                            load_from_file(fname);
                        } break;
                        case GUI_MENU_WWRAP: {
                            toggle_wwrap();
                        } break;
                        case GUI_MENU_ABOUT: 
                            MessageBoxW(
                                Window, 
                                L"Этот текстовый редактор был сделан для второй лабораторной работы\n"
                                L"Написал студент группы 606-12, Речук Дмитрий Максимович.",
                                L"О программе",
                                MB_OK | MB_ICONINFORMATION);
                        break;
                    }
                break;
            }
        break;
        default:
            return DefWindowProcW(hwnd, uMsg, wParam, lParam);
    }
    return 0;
}

int WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR lpCmdLine, int nShowCmd) {

    {
        INITCOMMONCONTROLSEX icc;
        icc.dwSize = sizeof(INITCOMMONCONTROLSEX);
        icc.dwICC = ICC_STANDARD_CLASSES;
        InitCommonControlsEx(&icc);
    }

    {
        PCWSTR class = L"MainClass";
        PCWSTR title = L"Text editor";
        CONST DWORD window_style = WS_CAPTION | WS_SYSMENU | WS_SIZEBOX | WS_MAXIMIZEBOX | WS_MINIMIZEBOX;
        CONST HBRUSH bgcol = GetSysColorBrush(COLOR_WINDOW);

        {
            WNDCLASSEXW wc = {0};
            wc.cbSize = sizeof(WNDCLASSEXW);
            wc.lpszClassName = class;
            wc.hInstance = hInstance;
            wc.lpfnWndProc = WndProc;
            wc.hbrBackground = bgcol;
            wc.hIcon =   LoadImageW(hInstance, L"myIcon", IMAGE_ICON, 24, 24, LR_DEFAULTCOLOR);
            wc.hIconSm = LoadImageW(hInstance, L"myIcon", IMAGE_ICON, 16, 16, LR_DEFAULTCOLOR);
          
            if (!RegisterClassExW(&wc))
                fatal(L"Failed to register the main class");
        }

        INT wW, wH;
        {
            RECT wrect = {0, 0, Width, Height};
            AdjustWindowRect(&wrect, window_style, TRUE);

            wW = wrect.right-wrect.left;
            wH = wrect.bottom-wrect.top;
        }

        CreateWindowW( class, 
                       title,
                       window_style,
                       CW_USEDEFAULT, CW_USEDEFAULT, 
                       wW, wH,
                       NULL, NULL, hInstance, NULL);

        if (!Window)
            fatal(L"Failed to create the main window");
    }

    {
        INT argc;
        LPWSTR* argv = CommandLineToArgvW(GetCommandLineW(), &argc);

        if (argv != NULL && argc > 1) {
            load_from_file(argv[1]);
        }

        LocalFree(argv);
    }

    ACCEL acctable[2] = {
        {.fVirt = FCONTROL | FVIRTKEY, .key = VK_BACK, .cmd = ACC_EDIT_DELETEWORD},
        {0,0,0}
    };

    Gui.edit_accels = CreateAcceleratorTableW(acctable, 1);
    if (!Gui.edit_accels)
        fatal(L"Failed to create the accelerator table");

    MSG msg;
    BOOL stat;
    while (stat = GetMessageW(&msg, NULL, 0, 0)) {

        if (stat == -1)
            fatal(L"GetMessage error");
        if (GetFocus() != Gui.text_box || !TranslateAcceleratorW(Gui.text_box, Gui.edit_accels, &msg)) {
            TranslateMessage(&msg);
            DispatchMessageW(&msg);
        }
    }
    return 0;
}