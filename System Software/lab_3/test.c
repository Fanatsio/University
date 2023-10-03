// Compile: x86_64-w64-mingw32-gcc screenshot.c -o screenshot.exe -Wall -mwindows
#include <windows.h>
#include <windowsx.h>
#include <wingdi.h>
#include <stdio.h>

#define ID_BEEP 1000
#define ID_QUIT 1001
#define ID_EDIT 1003
#define ID_MESS 1004

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
        WS_EX_CLIENTEDGE, szClassName, "ScreenshopApp", 
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
            edit = CreateWindowW(L"Edit", L"", WS_CHILD | WS_VISIBLE, 15, 15, 200, 25, hwnd, (HMENU)ID_EDIT, NULL, NULL);
            CreateWindowW(L"Button", L"Screenshot", WS_VISIBLE | WS_CHILD, 20, 250, 80, 25, hwnd, (HMENU)ID_BEEP, NULL, NULL);
            CreateWindowW(L"Button", L"Quit", WS_VISIBLE | WS_CHILD, 220, 250, 80, 25, hwnd, (HMENU)ID_QUIT, NULL, NULL);
            break;
        case WM_COMMAND:
            switch (LOWORD(wParam)) {
                case ID_BEEP:
                    char buff[1024];
                    GetWindowText(edit, buff, 1024);
                    int integerValue = atoi(buff);
                    for (int i = 25; i <= 100; i+=25) {
                        Sleep(integerValue * 1000);
                        HANDLE_WM_PAINT(hwnd, wParam, lParam, OnPaint);
                        CreateWindowW(L"Edit", L"Screenshot created", WS_CHILD | WS_VISIBLE, 50, i, 200, 25, hwnd, (HMENU)ID_MESS, NULL, NULL);
                    }
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

void SaveBitmapToFile(HBITMAP hBitmap, const char* filePath) {
    BITMAP bmp;
    GetObject(hBitmap, sizeof(BITMAP), &bmp);

    BITMAPFILEHEADER bmfh;
    BITMAPINFOHEADER bih;

    bih.biSize = sizeof(BITMAPINFOHEADER);
    bih.biWidth = bmp.bmWidth;
    bih.biHeight = bmp.bmHeight;
    bih.biPlanes = 1;
    bih.biBitCount = 32;
    bih.biCompression = BI_RGB;
    bih.biSizeImage = 0;
    bih.biXPelsPerMeter = 0;
    bih.biYPelsPerMeter = 0;
    bih.biClrUsed = 0;
    bih.biClrImportant = 0;

    DWORD dwBmpSize = ((bmp.bmWidth * bih.biBitCount + 31) / 32) * 4 * bmp.bmHeight;

    bmfh.bfType = 0x4D42;
    bmfh.bfSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + dwBmpSize;
    bmfh.bfReserved1 = 0;
    bmfh.bfReserved2 = 0;
    bmfh.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    FILE* file = fopen(filePath, "wb");
    if (!file) {
        return;
    }

    fwrite(&bmfh, sizeof(BITMAPFILEHEADER), 1, file);
    fwrite(&bih, sizeof(BITMAPINFOHEADER), 1, file);

    BYTE* pData = (BYTE*)malloc(dwBmpSize);
    if (!pData) {
        fclose(file);
        return;
    }

    HDC hDC = GetDC(NULL);
    GetDIBits(hDC, hBitmap, 0, bmp.bmHeight, pData, (BITMAPINFO*)&bih, DIB_RGB_COLORS);
    fwrite(pData, dwBmpSize, 1, file);
    ReleaseDC(NULL, hDC);

    fclose(file);
    free(pData);
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

        hOld = SelectBitmap(hBitmapdc, hBitmap);

        GetClientRect(hwnd, &rc);

        nWid = GetSystemMetrics(SM_CXSCREEN);
        nHt = GetSystemMetrics(SM_CYSCREEN);

        SaveBitmapToFile(hBitmap, "screenshot.bmp");

        DeleteDC(hBitmapdc);

        EndPaint(hwnd, &ps);
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