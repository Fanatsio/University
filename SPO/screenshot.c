#include <windows.h>
#include <wingdi.h>

// Define the interval time between screenshots in milliseconds
#define INTERVAL_TIME 1000

// Define the file name of the screenshots
#define FILE_NAME "screenshot.bmp"

// Function to capture the screen and save the screenshot to a file
void CaptureScreen(HDC hdcScreen, int width, int height)
{
  // Create a compatible DC for the screen
  HDC hdcCompatible = CreateCompatibleDC(hdcScreen);

  // Create a bitmap compatible with the screen DC
  HBITMAP hBitmap = CreateCompatibleBitmap(hdcScreen, width, height);

  // Select the bitmap into the compatible DC
  HBITMAP hOldBitmap = SelectObject(hdcCompatible, hBitmap);

  // Copy the screen contents to the compatible DC
  BitBlt(hdcCompatible, 0, 0, width, height, hdcScreen, 0, 0, SRCCOPY);

  // Save the bitmap to a file
  SaveBitmapToFile(hBitmap, FILE_NAME);

  // Clean up the DC and bitmap
  SelectObject(hdcCompatible, hOldBitmap);
  DeleteDC(hdcCompatible);
  DeleteObject(hBitmap);
}

// Function to get the size of a bitmap in bytes
DWORD GetBitmapSize(HBITMAP hBitmap){
  BITMAP bmp = { 0 };
  GetObject(hBitmap, sizeof(BITMAP), &bmp);
  return bmp.bmWidthBytes * bmp.bmHeight;
}

// Function to save a bitmap to a file
void SaveBitmapToFile(HBITMAP hBitmap, const char* fileName)
{
  // Create a file for writing the bitmap
  HANDLE hFile = CreateFile(fileName, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

  // Create a bitmap file header
  BITMAPFILEHEADER bmfHeader = { 0 };
  bmfHeader.bfType = 0x4d42; // "BM"
  bmfHeader.bfSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + GetBitmapSize(hBitmap);
  bmfHeader.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

  // Write the bitmap file header to the file
  DWORD dwBytesWritten = 0;
  WriteFile(hFile, &bmfHeader, sizeof(BITMAPFILEHEADER), &dwBytesWritten, NULL);

  // Create a bitmap info header
  BITMAPINFOHEADER bmiHeader = { 0 };
  bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
  bmiHeader.biWidth = GetSystemMetrics(SM_CXSCREEN);
  bmiHeader.biHeight = GetSystemMetrics(SM_CYSCREEN);
  bmiHeader.biPlanes = 1;
  bmiHeader.biBitCount = 24;
  bmiHeader.biCompression = BI_RGB;

  // Write the bitmap info header to the file
  WriteFile(hFile, &bmiHeader, sizeof(BITMAPINFOHEADER), &dwBytesWritten, NULL);

  // Get the bitmap bits and write them to the file
  LPBYTE lpBits = NULL;
  DWORD dwBitsSize = GetBitmapSize(hBitmap);
  lpBits = (LPBYTE)GlobalAlloc(GMEM_FIXED, dwBitsSize);
  GetBitmapBits(hBitmap, dwBitsSize, lpBits);
  WriteFile(hFile, lpBits, dwBitsSize, &dwBytesWritten, NULL);

  // Clean up the file and bitmap bits
  CloseHandle(hFile);
  GlobalFree(lpBits);
}

// Main function
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow){
  // Get the screen DC
  HDC hdcScreen = GetDC(NULL);
  // Get the screen width and height
  int screenWidth = GetSystemMetrics(SM_CXSCREEN);
  int screenHeight = GetSystemMetrics(SM_CYSCREEN);

  // Loop to take screenshots at the specified interval time
  while (1)
  {
    // Capture the screen and save the screenshot to a file
    CaptureScreen(hdcScreen, screenWidth, screenHeight);

    // Wait for the specified interval time
    Sleep(INTERVAL_TIME);
  }

  // Release the screen DC
  ReleaseDC(NULL, hdcScreen);
  return 0;
}