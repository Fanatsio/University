// Compile: x86_64-w64-mingw32-gcc screenshot.c -o screenshot.exe -Wall -mwindows
#include <windows.h>
#include <windowsx.h>

#define ID_BEEP 1000
#define ID_QUIT 1001
#define ID_EDIT 1003

LRESULT CALLBACK WindowProcedure (HWND, UINT, WPARAM, LPARAM);
void CaptureScreen(HWND);
void OnPaint(HWND hwnd);

char szClassName[ ] = "Screenshot";

HBITMAP hBitmap = NULL;
HWND edit;

int WINAPI WinMain (HINSTANCE hThisInstance, HINSTANCE hPrevInstance, LPSTR lpszArgument, int nFunsterStil) {
    HWND hwnd;
    MSG messages;
    WNDCLASSEX wincl;
    HDC dc;

    wincl.hInstance = hThisInstance;
    wincl.lpszClassName = szClassName;
    wincl.lpfnWndProc = WindowProcedure;
    wincl.style = CS_DBLCLKS;
    wincl.cbSize = sizeof (WNDCLASSEX);
    wincl.hIcon = LoadIcon (NULL, IDI_APPLICATION);
    wincl.hIconSm = LoadIcon (NULL, IDI_APPLICATION);
    wincl.hCursor = LoadCursor (NULL, IDC_ARROW);
    wincl.lpszMenuName = NULL;
    wincl.cbClsExtra = 0;
    wincl.cbWndExtra = 0;
    wincl.hbrBackground = (HBRUSH) COLOR_BACKGROUND;

    if (!RegisterClassEx (&wincl)) {
        return 0;
    }
    
    hwnd = CreateWindowEx(
        WS_EX_CLIENTEDGE, szClassName, "Hello from WinAPI!", 
        WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 
        350, 330, NULL, NULL, hThisInstance, NULL
    );

    CaptureScreen(hwnd);

    ShowWindow (hwnd, SW_MAXIMIZE);


    while (GetMessage (&messages, NULL, 0, 0)) {
        TranslateMessage(&messages);
        DispatchMessage(&messages);
    }

    return messages.wParam;
}

LRESULT CALLBACK WindowProcedure (HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
        case WM_CREATE:
            edit = CreateWindowW(L"Edit", L"",
                                    WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL,
                                    15, 15, 200, 25, hwnd, (HMENU)ID_EDIT, NULL, NULL);
            CreateWindowW(L"Button", L"Screenshot", WS_VISIBLE | WS_CHILD, 20, 250, 80, 25, hwnd,
                          (HMENU)ID_BEEP, NULL, NULL);
            CreateWindowW(L"Button", L"Quit", WS_VISIBLE | WS_CHILD, 220, 250, 80, 25, hwnd,
                          (HMENU)ID_QUIT, NULL, NULL);
            break;
        case WM_COMMAND:
            switch (LOWORD(wParam)) {
                case ID_BEEP:
                    char buff[1024];
                    GetWindowText(edit, buff, 1024);
                    int integerValue = atoi(buff);
                    Sleep(integerValue * 1000);                         // доделать функцию создания скриншотов через заданные промежутки
                    HANDLE_WM_PAINT(hwnd, wParam, lParam, OnPaint);     // Разобраться с функцией OnPaint()
                    break;
                case ID_QUIT:
                    PostQuitMessage(0);
                    break;
            }
            break;
        case WM_DESTROY:
            PostQuitMessage (0);
            break;
        default:
            return DefWindowProc (hwnd, message, wParam, lParam);
    }
    return 0;
}

void OnPaint(HWND hwnd) {
    HDC hBitmapdc, hWindowdc;
    HBITMAP hOld;
    PAINTSTRUCT ps;
    RECT rc;
    int nWid, nHt;

    if (hBitmap) {
        hWindowdc = BeginPaint(hwnd, &ps);
        hWindowdc = GetDC(hwnd);

        hBitmapdc = CreateCompatibleDC(hWindowdc);

        hOld = SelectBitmap(hBitmapdc,hBitmap);

        GetClientRect(hwnd,&rc);

        nWid = GetSystemMetrics(SM_CXSCREEN);
        nHt = GetSystemMetrics(SM_CYSCREEN);

        StretchBlt(                                 // Переместить отображение скриншотов в отдельное окно
            hWindowdc, 0, 0, rc.right, rc.bottom,   // Или сделать функцию сохранения .jpg
            hBitmapdc, 0, 0, nWid, nHt, SRCCOPY
        );

        DeleteDC(hBitmapdc);

        EndPaint(hwnd,&ps);
    }
}

void CaptureScreen(HWND hParent) {
    HDC hDesktopdc,hBitmapdc;
    int nWid, nHt;
    HBITMAP hOriginal;

    hDesktopdc = GetWindowDC(HWND_DESKTOP);
    if (hDesktopdc) {
        nWid = GetSystemMetrics(SM_CXSCREEN);
        nHt = GetSystemMetrics(SM_CYSCREEN);

        hBitmap = CreateCompatibleBitmap(hDesktopdc,nWid,nHt);
        hBitmapdc = CreateCompatibleDC(hDesktopdc);
        hOriginal = (HBITMAP)SelectBitmap(hBitmapdc, hBitmap);

        BitBlt(hBitmapdc,0,0,nWid,nHt,
        hDesktopdc,0,0,SRCCOPY);

        DeleteDC(hBitmapdc);

        ReleaseDC(HWND_DESKTOP, hDesktopdc);

        UpdateWindow(hParent);
    }
}