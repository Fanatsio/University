#include <windows.h>
#include <stdio.h>
#include <wingdi.h>
#include <stdbool.h>

// Function to capture a screenshot and save it to a JPEG file
void captureScreenshot(int count) {
    HDC hdcScreen = GetDC(NULL);
    
    int width = GetSystemMetrics(SM_CXSCREEN);
    int height = GetSystemMetrics(SM_CYSCREEN);
    
    HBITMAP hBitmap = CreateCompatibleBitmap(hdcScreen, width, height);
    HDC hdcMem = CreateCompatibleDC(hdcScreen);
    HBITMAP hOldBitmap = (HBITMAP)SelectObject(hdcMem, hBitmap);
    
    BitBlt(hdcMem, 0, 0, width, height, hdcScreen, 0, 0, SRCCOPY);
    
    SelectObject(hdcMem, hOldBitmap);
    DeleteDC(hdcMem);
    ReleaseDC(NULL, hdcScreen);
    
    char filename[100];
    sprintf(filename, "screenshot_%d.jpg", count);
    
    // Save the captured screenshot as a JPEG file
    SaveBitmapAsJPEG(hBitmap, filename, 90); // 90 is the JPEG quality
    
    DeleteObject(hBitmap);
}

// Function to save a bitmap as a JPEG file
void SaveBitmapAsJPEG(HBITMAP hBitmap, const char* filename, int quality) {
    BITMAP bmp;
    if (!GetObject(hBitmap, sizeof(BITMAP), &bmp)) {
        return;
    }
    
    BITMAPINFOHEADER bmi = {0};
    bmi.biSize = sizeof(BITMAPINFOHEADER);
    bmi.biWidth = bmp.bmWidth;
    bmi.biHeight = -bmp.bmHeight; // Negative height to make the image top-down
    bmi.biPlanes = 1;
    bmi.biBitCount = 24; // 24-bit RGB format
    bmi.biCompression = BI_RGB;
    
    unsigned char* buffer = NULL;
    HDC hdc = GetDC(NULL);
    
    HBITMAP hDIB = CreateDIBSection(hdc, (BITMAPINFO*)&bmi, DIB_RGB_COLORS, (void**)&buffer, NULL, 0);
    HDC hMemDC = CreateCompatibleDC(hdc);
    HBITMAP hOldBitmap = (HBITMAP)SelectObject(hMemDC, hDIB);
    
    BitBlt(hMemDC, 0, 0, bmp.bmWidth, bmp.bmHeight, hBitmap, 0, 0, SRCCOPY);
    
    SelectObject(hMemDC, hOldBitmap);
    DeleteDC(hMemDC);
    ReleaseDC(NULL, hdc);
    
    // Save the DIB (bitmap) as a JPEG file
    SaveDIBAsJPEG(hDIB, filename, quality);
    
    DeleteObject(hDIB);
}

// Function to save a DIB (bitmap) as a JPEG file
void SaveDIBAsJPEG(HBITMAP hDIB, const char* filename, int quality) {
    // Convert the DIB to JPEG and save it
    // Implement this function using Windows API functions or external library
}

DWORD WINAPI ScreenshotThread(LPVOID lpParam) {
    int intervalInSeconds = *(int*)lpParam;
    int screenshotCount = 1;
    
    while (1) {
        captureScreenshot(screenshotCount);
        printf("Screenshot %d captured\n", screenshotCount);
        
        screenshotCount++;
        Sleep(intervalInSeconds * 1000); // Sleep for the specified interval
    }
    
    return 0;
}

int main() {
    int intervalInSeconds = 5; // Set the interval between screenshots
    
    // Create a thread for capturing screenshots
    HANDLE hThread = CreateThread(NULL, 0, ScreenshotThread, &intervalInSeconds, 0, NULL);
    
    if (hThread == NULL) {
        printf("Failed to create thread\n");
        return 1;
    }
    
    // Wait for the thread to finish
    WaitForSingleObject(hThread, INFINITE);
    
    // Clean up the thread handle
    CloseHandle(hThread);
    
    return 0;
}
