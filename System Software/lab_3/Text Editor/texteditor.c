#include <windows.h>
#include <commctrl.h>

#define ID_QUIT 1001
#define ID_TEXT 1002
#define ID_EDIT 1003
#define OnMenu1Clicked 1004
#define OnMenu2Clicked 1005
#define OnMenu3Clicked 1006
#define IDC_CHILD_EDIT	101
#define IDC_MAIN_STATUS	103
#define ON_COPY 1007
#define ON_PASTE 1008
#define ON_CUT 1009
#define ON_SAVE 1010

HWND edit;
HWND g_hMainWindow = NULL;

BOOL SaveTextFileFromEdit(HWND hEdit, LPCTSTR pszFileName)
{
    HANDLE hFile;
    BOOL bSuccess = FALSE;

    hFile = CreateFile(pszFileName, GENERIC_WRITE, 0, NULL,
        CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE)
    {
        DWORD dwTextLength;

        dwTextLength = GetWindowTextLength(hEdit);
        if (dwTextLength > 0)
        {
            LPWSTR pszText;
            DWORD dwBufferSize = dwTextLength + 1;

            pszText = (LPWSTR)GlobalAlloc(GPTR, dwBufferSize);
            if (pszText != NULL)
            {
                if (GetWindowText(hEdit, (LPSTR)pszText, dwBufferSize))
                {
                    DWORD dwWritten;

                    if (WriteFile(hFile, pszText, dwTextLength, &dwWritten, NULL))
                        bSuccess = TRUE;
                }
                GlobalFree(pszText);
            }
        }
        CloseHandle(hFile);
    }
    return bSuccess;
}

void DoFileSave(HWND hwnd)
{
    OPENFILENAME ofn;
    char szFileName[MAX_PATH] = "";

    ZeroMemory(&ofn, sizeof(ofn));

    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwnd;
    ofn.lpstrFilter = "Text Files (*.txt)\0*.txt\0All Files (*.*)\0*.*\0";
    ofn.lpstrFile = szFileName;
    ofn.nMaxFile = MAX_PATH;
    ofn.lpstrDefExt = "txt";
    ofn.Flags = OFN_EXPLORER | OFN_PATHMUSTEXIST | OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT;

    if (GetSaveFileName(&ofn))
    {
        HWND hEdit = GetDlgItem(hwnd, ID_EDIT);
        if (SaveTextFileFromEdit(hEdit, szFileName))
        {
            SendDlgItemMessage(g_hMainWindow, IDC_MAIN_STATUS, SB_SETTEXT, 0, (LPARAM)"Saved...");
            SendDlgItemMessage(g_hMainWindow, IDC_MAIN_STATUS, SB_SETTEXT, 1, (LPARAM)szFileName);

            SetWindowText(hwnd, szFileName);
        }
    }
}

BOOL LoadTextFileToEdit(HWND hEdit, LPCTSTR pszFileName)
{
    HANDLE hFile;
    BOOL bSuccess = FALSE;

    hFile = CreateFile(pszFileName, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile != INVALID_HANDLE_VALUE)
    {
        DWORD dwFileSize;

        dwFileSize = GetFileSize(hFile, NULL);
        if (dwFileSize != 0xFFFFFFFF)
        {
            LPWSTR pszFileText;

            pszFileText = (LPWSTR)GlobalAlloc(GPTR, dwFileSize + 1);
            if (pszFileText != NULL)
            {
                DWORD dwRead;

                if (ReadFile(hFile, pszFileText, dwFileSize, &dwRead, NULL))
                {
                    pszFileText[dwFileSize] = 0;
                    if (SetWindowText(hEdit, (LPCSTR)pszFileText))
                        bSuccess = TRUE;
                }
                GlobalFree(pszFileText);
            }
        }
        CloseHandle(hFile);
    }
    return bSuccess;
}

void DoFileOpen(HWND hwnd)
{
    OPENFILENAME ofn;
    char szFileName[MAX_PATH] = "";

    ZeroMemory(&ofn, sizeof(ofn));

    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwnd;
    ofn.lpstrFilter = "Text Files (*.txt)\0*.txt\0All Files (*.*)\0*.*\0";
    ofn.lpstrFile = szFileName;
    ofn.nMaxFile = MAX_PATH;
    ofn.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST | OFN_HIDEREADONLY;
    ofn.lpstrDefExt = "txt";

    if (GetOpenFileName(&ofn))
    {
        HWND hEdit = GetDlgItem(hwnd, IDC_CHILD_EDIT);
        if (LoadTextFileToEdit(edit, szFileName))
        {
            SendDlgItemMessage(g_hMainWindow, IDC_MAIN_STATUS, SB_SETTEXT, 0, (LPARAM)"...");
            SendDlgItemMessage(g_hMainWindow, IDC_MAIN_STATUS, SB_SETTEXT, 1, (LPARAM)szFileName);

            SetWindowText(hwnd, szFileName);
        }
    }
}

void MainWndAddMenu(HWND hwnd)
{
    HMENU RootMenu = CreateMenu();
    HMENU SubMenu = CreateMenu();
    HMENU SubMenu2 = CreateMenu();
    HMENU SubMenu3 = CreateMenu();
    AppendMenu(SubMenu, MF_STRING, ON_SAVE,"Save");
    AppendMenu(SubMenu, MF_STRING, OnMenu2Clicked, "Open");
    AppendMenu(SubMenu2, MF_STRING, OnMenu3Clicked, "About the program");
    AppendMenu(SubMenu3, MF_STRING, ON_COPY, "Copy");
    AppendMenu(SubMenu3, MF_STRING, ON_PASTE, "Paste");
    AppendMenu(SubMenu3, MF_STRING, ON_CUT, "Cut");
    AppendMenu(RootMenu, MF_POPUP, (UINT_PTR)SubMenu, "File");
    AppendMenu(RootMenu, MF_POPUP, (UINT_PTR)SubMenu2, "Reference");
    AppendMenu(RootMenu, MF_POPUP, (UINT_PTR)SubMenu3, "Edit");
    SetMenu(hwnd, RootMenu);
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    switch (msg)
    {
    case WM_CREATE:
        edit = CreateWindowW(L"Edit", L"",
            WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL,
            15, 15, 300, 200, hwnd, (HMENU)ID_EDIT, NULL, NULL);
        CreateWindowW(L"Button", L"Quit", WS_VISIBLE | WS_CHILD, 220, 250, 80, 25, hwnd,
            (HMENU)ID_QUIT, NULL, NULL);
        MainWndAddMenu(hwnd);
        break;
    case WM_COMMAND:
        switch (wParam)
        {
        case ON_SAVE:
            DoFileSave(hwnd);
            break;
        case OnMenu2Clicked:
            DoFileOpen(hwnd);
            break;
        case OnMenu3Clicked:
            MessageBox(hwnd, "A simple text editor\nDeveloper: Dmitry Rechuk", "About the program", MB_OK);
            break;
        case ON_CUT:
            SendDlgItemMessage(hwnd, ID_EDIT, WM_CUT, 0, 0);
            break;
        case ON_COPY:
            SendDlgItemMessage(hwnd, ID_EDIT, WM_COPY, 0, 0);
            break;
        case ON_PASTE:
            SendDlgItemMessage(hwnd, ID_EDIT, WM_PASTE, 0, 0);
            break;
        default:
            break;
        }
        switch (LOWORD(wParam))
        {
        case ID_TEXT:;
            char buff[1024];
            GetWindowText(edit, buff, 1024);
            MessageBox(NULL, buff, "Info!", MB_ICONINFORMATION | MB_OK);
            break;
        case ID_QUIT:
            PostQuitMessage(0);
            break;
        }
        break;
    case WM_CLOSE:
        DestroyWindow(hwnd);
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    WNDCLASSEX wc;
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = 0;
    wc.lpfnWndProc = WndProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszMenuName = NULL;
    wc.lpszClassName = "myWindowClass";
    wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if (!RegisterClassEx(&wc))
    {
        MessageBox(NULL, "Window Registration Failed!", "Error!", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }
    HWND hwnd;
    hwnd =
        CreateWindowEx(WS_EX_CLIENTEDGE, "myWindowClass", "Nameless", WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT, CW_USEDEFAULT, 350, 330, NULL, NULL, hInstance, NULL);
    if (hwnd == NULL)
    {
        MessageBox(NULL, "Window Creation Failed!", "Error!", MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG Msg;
    while (GetMessage(&Msg, NULL, 0, 0) > 0)
    {
        TranslateMessage(&Msg);
        DispatchMessage(&Msg);
    }
    return Msg.wParam;
}
