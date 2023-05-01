#include <windows.h>
#include <WinUser.h>
#include <tchar.h>
#include <math.h>
#include <string.h>
#include <stdbool.h>

HINSTANCE	capInstance;
HWND		hwnd;
HWND		capHwnd;

char bmp_index = 'a';

int width	= 0;
int height	= 0;

RECT captureCoord;
BYTE lClickNum = 0;

bool setTransparentWindow( HWND, int );
HWND createCaptureWindow( int, RECT );

LRESULT CALLBACK WndProc( HWND, UINT, WPARAM, LPARAM );
LRESULT CALLBACK captureProc( HWND, UINT, WPARAM, LPARAM );

HBITMAP CopyDCToBitmap(HDC hScrDC, LPRECT lpRect);
BOOL SaveBmp(HBITMAP hBitmap, LPCWSTR FileName);

int WINAPI WinMain( __in HINSTANCE hInstance, __in_opt HINSTANCE hPrevInstance, __in_opt LPSTR lpCmdLine, __in int nShowCmd )
{
	char appName[] = "Capture your window!";
	capInstance = hInstance;

	width = GetSystemMetrics( SM_CXVIRTUALSCREEN );
	height = GetSystemMetrics( SM_CYVIRTUALSCREEN );

	WNDCLASSEX wncx;
	ZeroMemory(&wncx, sizeof(wncx));
	
	wncx.cbSize = sizeof(WNDCLASSEX);
	wncx.cbClsExtra	= 0;
	wncx.cbWndExtra	= 0;
	wncx.hbrBackground	= (HBRUSH) GetStockObject( TRANSPARENT );
	wncx.hCursor	= LoadCursor( NULL, IDC_ARROW );
	wncx.hIcon		= LoadIcon( NULL, IDI_APPLICATION );
	wncx.hIconSm	= NULL;
	wncx.hInstance	= hInstance;
	wncx.style		= CS_VREDRAW | CS_HREDRAW;
	wncx.lpszClassName	= appName;
	wncx.lpszMenuName	= _T( "Menu" );
	wncx.lpfnWndProc	= (WNDPROC) WndProc;

	if(!RegisterClassEx(&wncx))
	{
		MessageBox( NULL, _T( "Register window class failed!" ), _T( "Failed" ), MB_OK );
		return -1;
	}

	hwnd = CreateWindow( appName, _T( "Capture your window" ), WS_POPUP | WS_SYSMENU | WS_SIZEBOX, 0, 0, width, height, NULL, NULL, hInstance, NULL );
	MessageBox( NULL, _T( "Select an area of the screen by clicking on two points with the mouse\nTo close the program, press the right mouse button" ), _T( "Instruction" ), MB_OK );
	if( NULL == hwnd )
	{
		MessageBox( NULL, _T( "Create window failed!" ), _T( "Failed" ), MB_OK );
		return -1;
	}

	ShowWindow( hwnd, nShowCmd );
	UpdateWindow( hwnd );

	MSG msg;
	ZeroMemory( &msg, sizeof( msg ) );

	while( WM_QUIT != msg.message )
	{
		if( PeekMessage( &msg, NULL, 0U, 0U, PM_REMOVE ) )
		{
			TranslateMessage( &msg );
			DispatchMessage( &msg );
		}			
		else
		{
			WaitMessage();
		}
	}

	return (int) msg.wParam;
}


LRESULT CALLBACK WndProc( HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam )
{
	switch( msg )
	{
		case WM_CREATE:
		{		
			if( !setTransparentWindow( hwnd, 90 ) )
			{
				MessageBox( NULL, _T( "Set transparent window failed!" ), _T( "Failed" ), MB_OK );
			}
		}
		return 0;

		case WM_LBUTTONDOWN:
		{
			if( lClickNum > 1 )
				return 0;

			POINT mousePos;
			GetCursorPos( &mousePos );

			if( lClickNum++ == 0 )
			{
				captureCoord.left = mousePos.x;
				captureCoord.top  = mousePos.y;
			}
			else
			{
				captureCoord.right  = mousePos.x;
				captureCoord.bottom = mousePos.y;

				if( !createCaptureWindow( SW_SHOW, captureCoord ) )
				{
					MessageBox( NULL, _T( "Create window failed!" ), _T( "Failed" ), MB_OK );
				}
				else
				{
					MSG msg;
					ZeroMemory( &msg, sizeof( msg ) );

					while( WM_QUIT != msg.message )
					{
						if( PeekMessage( &msg, NULL, 0U, 0U, PM_REMOVE ) )
						{
							TranslateMessage( &msg );
							DispatchMessage( &msg );
						}			
						else
						{
							WaitMessage();
						}
					}
				}
			}
		}
		return 0;

		case WM_RBUTTONDOWN:
		{
			PostQuitMessage( 0 );
		}
		return 0;

		case WM_DESTROY:
		{
			PostQuitMessage( 0 );
		}
		return 0;

		default:
			return DefWindowProc( hwnd, msg, wParam, lParam );
	}
}

bool setTransparentWindow( HWND hwnd, int trans_degree )
{
	SetWindowLong( hwnd, GWL_EXSTYLE, GetWindowLong( hwnd, GWL_EXSTYLE ) ^ 0x80000 ); 

	HINSTANCE hInst = LoadLibrary( _T( "User32.DLL" ) );   
	if( hInst )   
	{   
		typedef BOOL (WINAPI *MYFUNC) ( HWND, COLORREF, BYTE, DWORD );   
		MYFUNC fun = NULL; 

		fun = (MYFUNC) GetProcAddress( hInst, "SetLayeredWindowAttributes" ); 

		if( fun )
			fun( hwnd, 0, trans_degree, 2 );   

		FreeLibrary( hInst );   
	} 
	else
		return false;

	return true;
}

HBITMAP CopyDCToBitmap(HDC hScrDC, LPRECT lpRect)
{
	HDC hMemDC; 
	HBITMAP hBitmap,hOldBitmap; 
	int nX, nY, nX2, nY2; 
	int nWidth, nHeight; 
	if (IsRectEmpty(lpRect))
		return NULL;
	nX = lpRect->left;
	nY = lpRect->top;
	nX2 = lpRect->right;
	nY2 = lpRect->bottom;
	nWidth = nX2 - nX;
	nHeight = nY2 - nY;
	hMemDC = CreateCompatibleDC(hScrDC);
	hBitmap = CreateCompatibleBitmap(hScrDC, nWidth, nHeight);
	hOldBitmap = (HBITMAP)SelectObject(hMemDC, hBitmap);
	StretchBlt(hMemDC,0,0,nWidth,nHeight,hScrDC,nX,nY,nWidth,nHeight,SRCCOPY);
	hBitmap = (HBITMAP)SelectObject(hMemDC, hOldBitmap);

	DeleteDC(hMemDC);
	DeleteObject(hOldBitmap);
	return hBitmap;
}

BOOL SaveBmp(HBITMAP hBitmap, LPCWSTR FileName)
{
	HDC hDC;
	int iBits;
	WORD wBitCount;
	DWORD dwPaletteSize=0, dwBmBitsSize=0, dwDIBSize=0, dwWritten=0; 
	BITMAP Bitmap; 
	BITMAPFILEHEADER bmfHdr; 
	BITMAPINFOHEADER bi; 
	LPBITMAPINFOHEADER lpbi; 
	HANDLE fh, hDib, hPal,hOldPal=NULL; 

	hDC = CreateDC( _T( "DISPLAY" ), NULL, NULL, NULL);
	iBits = GetDeviceCaps(hDC, BITSPIXEL) * GetDeviceCaps(hDC, PLANES); 
	DeleteDC(hDC); 
	if (iBits <= 1) wBitCount = 1; 
	else if (iBits <= 4) wBitCount = 4; 
	else if (iBits <= 8) wBitCount = 8; 
	else wBitCount = 24; 

	GetObject(hBitmap, sizeof(Bitmap), (LPSTR)&Bitmap);
	bi.biSize = sizeof(BITMAPINFOHEADER);
	bi.biWidth = Bitmap.bmWidth;
	bi.biHeight = Bitmap.bmHeight;
	bi.biPlanes = 1;
	bi.biBitCount = wBitCount;
	bi.biCompression = BI_RGB;
	bi.biSizeImage = 0;
	bi.biXPelsPerMeter = 0;
	bi.biYPelsPerMeter = 0;
	bi.biClrImportant = 0;
	bi.biClrUsed = 0;

	dwBmBitsSize = ((Bitmap.bmWidth * wBitCount + 31) / 32) * 4 * Bitmap.bmHeight;

	hDib = GlobalAlloc(GHND,dwBmBitsSize + dwPaletteSize + sizeof(BITMAPINFOHEADER)); 
	lpbi = (LPBITMAPINFOHEADER)GlobalLock(hDib); 
	*lpbi = bi; 
	hPal = GetStockObject(DEFAULT_PALETTE); 
	if (hPal) 
	{ 
		hDC = GetDC(NULL); 
		hOldPal = SelectPalette(hDC, (HPALETTE)hPal, FALSE); 
		RealizePalette(hDC); 
	}
	GetDIBits(hDC, hBitmap, 0, (UINT) Bitmap.bmHeight, (LPSTR)lpbi + sizeof(BITMAPINFOHEADER) 
		+dwPaletteSize, (BITMAPINFO *)lpbi, DIB_RGB_COLORS); 

	if (hOldPal) 
	{ 
		SelectPalette(hDC, (HPALETTE)hOldPal, TRUE); 
		RealizePalette(hDC); 
		ReleaseDC(NULL, hDC); 
	} 
	fh = CreateFile(FileName, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL | FILE_FLAG_SEQUENTIAL_SCAN, NULL); 

	if (fh == INVALID_HANDLE_VALUE) return FALSE; 

	bmfHdr.bfType = 0x4D42;
	dwDIBSize = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + dwPaletteSize + dwBmBitsSize; 
	bmfHdr.bfSize = dwDIBSize; 
	bmfHdr.bfReserved1 = 0; 
	bmfHdr.bfReserved2 = 0; 
	bmfHdr.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER) + dwPaletteSize; 
	WriteFile(fh, (LPSTR)&bmfHdr, sizeof(BITMAPFILEHEADER), &dwWritten, NULL); 
	WriteFile(fh, (LPSTR)lpbi, dwDIBSize, &dwWritten, NULL); 
	GlobalUnlock(hDib); 
	GlobalFree(hDib); 
	CloseHandle(fh); 
	return TRUE;
}

HWND createCaptureWindow( int nShowCmd, RECT coord )
{
	char captureName[] = "Get_it";

	WNDCLASSEX wncx;
	ZeroMemory( &wncx, sizeof( wncx ) );

	wncx.cbSize = sizeof( WNDCLASSEX );
	wncx.cbClsExtra	= 0;
	wncx.cbWndExtra	= 0;
	wncx.hbrBackground	= (HBRUSH) GetStockObject( TRANSPARENT );
	wncx.hCursor	= LoadCursor( NULL, IDC_WAIT );
	wncx.hIcon		= LoadIcon( NULL, IDI_APPLICATION );
	wncx.hIconSm	= NULL;
	wncx.hInstance	= capInstance;
	wncx.style		= CS_VREDRAW | CS_HREDRAW;
	wncx.lpszClassName	= captureName;
	wncx.lpszMenuName	= _T( "Menu" );
	wncx.lpfnWndProc	= (WNDPROC) captureProc;

	if( !RegisterClassEx( &wncx ) )
	{
		MessageBox( NULL, _T( "Register window class failed!" ), _T( "Failed" ), MB_OK );
		return 0;
	}

	int initX = min( coord.left, coord.right );
	int initY = min( coord.top, coord.bottom );
	int initWidth = abs( coord.right - coord.left );
	int initHeight = abs( coord.bottom - coord.top );

	capHwnd = CreateWindow( captureName, _T( "Capture your window" ), WS_POPUP | WS_SYSMENU | WS_SIZEBOX | WS_CHILD, initX, initY, initWidth, initHeight,
		hwnd, NULL, capInstance, NULL );

	if( NULL == capHwnd )
	{
		MessageBox( NULL, _T( "Create window failed!" ), _T( "Failed" ), MB_OK );
		return 0;
	}

	ShowWindow( capHwnd, nShowCmd );
	UpdateWindow( capHwnd );

	return capHwnd;
}

LRESULT CALLBACK captureProc( HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam )
{
	switch( msg )
	{
		case WM_CREATE:
		{
			if( !setTransparentWindow( hwnd, 60 ) )
			{
				MessageBox( NULL, _T( "Set transparent window failed!" ), _T( "Failed" ), MB_OK );
			}
			SetTimer(hwnd, 1, 5000, NULL);
			break;
		}
		return 0;
		case WM_PAINT:
		{
			PAINTSTRUCT ps;
			HDC hdc = BeginPaint( hwnd, &ps );
			EndPaint( hwnd, &ps );
			return 0;
		}
		case WM_KEYDOWN:
		{
			switch( wParam )
			{
			case VK_ESCAPE:
				lClickNum = 0;
				SendMessage( capHwnd, WM_DESTROY, wParam, lParam );
				break;

			default:
				break;
			}
		}
		return 0;

		case WM_TIMER:
		{
			wchar_t bmp_file[] = { ' ', '.', 'b', 'm', 'p', '\0' };
			bmp_file[0] = bmp_index++;

			GetWindowRect( capHwnd, &captureCoord );

			if( !SaveBmp( CopyDCToBitmap( GetDC( GetDesktopWindow() ), &captureCoord ), bmp_file ) )
			{
				MessageBox( NULL, _T( "Create bitmap failed!" ), _T( "Failed" ), MB_OK );
			}
			else
			{
				MessageBox( NULL, _T( "Create bitmap successfully!" ), _T( "Succeed" ), MB_OK );
			}
		}
		return 0;

		case WM_NCHITTEST:
		{
			UINT nHitTest;
			nHitTest = DefWindowProc(hwnd,msg,wParam,lParam);
			if(nHitTest == HTCLIENT && GetAsyncKeyState(MK_LBUTTON) < 0)
			{
				nHitTest = HTCAPTION;
			}
			return nHitTest;
		}

		case WM_RBUTTONDOWN:
		{
			PostQuitMessage(0);
		}
		return 0;

		case WM_DESTROY:
		{
			PostQuitMessage( 0 );
		}
		return 0;

		default:
			return DefWindowProc( hwnd, msg, wParam, lParam );
	}
}
