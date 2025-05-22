Program GoodScreen;  { THIS PROGRAM WILL DISPLAY GOOD SCREEN
                       FOR THE SMALL BUSINESS PURCHASING ASSISTANT }

uses Crt,
     Graph,   { library of graphics routines }
     Drivers, { all the BGI drivers }
     Fonts;   { all the BGI fonts }

var CheckBreak,
    FuncKey:    Boolean;
    Ch:         char;

Procedure CheckForDriversandfonts;

  Procedure Abort(Msg : string);
    begin
      Writeln(Msg, ': ', GraphErrorMsg(GraphResult));
      Halt(1);
    end;


begin {CheckForDriversandfonts}
  { Register all the drivers }
  if RegisterBGIdriver(@CGADriverProc) < 0 then
    Abort('CGA');
  if RegisterBGIdriver(@EGAVGADriverProc) < 0 then
    Abort('EGA/VGA');
  if RegisterBGIdriver(@HercDriverProc) < 0 then
    Abort('Herc');
  if RegisterBGIdriver(@ATTDriverProc) < 0 then
    Abort('AT&T');
  if RegisterBGIdriver(@PC3270DriverProc) < 0 then
    Abort('PC 3270');


  { Register all the fonts }
  if RegisterBGIfont(@GothicFontProc) < 0 then
    Abort('Gothic');
  if RegisterBGIfont(@SansSerifFontProc) < 0 then
    Abort('SansSerif');
  if RegisterBGIfont(@SmallFontProc) < 0 then
    Abort('Small');
  if RegisterBGIfont(@TriplexFontProc) < 0 then
    Abort('Triplex');

end;  {CheckForDriversandfonts}


Procedure SelectDriver;

var
     C,
     GraphDriver,
     GraphMode,
     ErrorCode : integer;

begin  {SelectDriver}

  GraphDriver := Detect;                  { It detects the hardware }
  InitGraph(GraphDriver, GraphMode, '');  { and activates the graphics }
  if GraphResult <> grOk then             { Checks for any errors }

  begin
    Writeln('Graphics init error: ', GraphErrorMsg(GraphDriver));
    Writeln('Sorry No Graphics Driver Were found.  Therefore, Program aborted...');
    Halt(1);
  end;

end;   {SelectDriver}


{ This Procedure will come only when the program is started it draws the
  3 borders that changes color and in it displays text. }

Procedure WaitToGo; { Wait for the user to continue }

var
  Ch : char;

 begin { WaitToGo }
    repeat until KeyPressed;
    Ch := ReadKey;
    if ch = #0 then ch := readkey;      { trap function keys }
    ClearDevice;                        { clear screen,  }
 end; { WaitToGo }

Procedure Good;

    Begin
       SetBKcolor(BLUE);
       Setcolor(LightCyan);
       Rectangle(0,0, GetMaxX, GetMaxY);         {draws full screen box}
       Setcolor(LightMagenta);
       Rectangle(5,5, GetMaxX-5, GetMaxY-5);            {   3   }
       Setcolor(LightCyan);
       Rectangle(10,10, GetMaxX-10, GetMaxY-10);        { Times }

       SetTextJustify(CenterText, CenterTExt);       { Centers text}

       SetTextStyle(Triplexfont, HorizDir, 6);
       SetColor(LightRed);
       SetUserCharSize(2, 1, 4, 2);          { REMINDER-this line will make next line bigger }
       OutTextXY(GetMaxX div 2, GetMaxY-400, 'Small Business');
       SetTextStyle(Triplexfont, HorizDir, 6);
       OutTextXY(GetMaxX div 2, GetMaxY-325, 'Acquisition Advisor');
       SetTextStyle(Triplexfont, HorizDir, 4);
       OutTextXY(GetMaxX div 2, GetMaxY-250, 'Recommends');
       OutTextXY(GetMaxX div 2, GetMaxY-200, 'that you');
       SetTextStyle(Triplexfont, HorizDir, 5);
       OutTextXY(GetMaxX div 2, GetMaxY-150, 'Purchase');
       SetTextStyle(Triplexfont, HorizDir, 1);
       OutTextXY(GetMaxX div 2, GetMaxY-100, 'this business ONLY after ALL evaluations are completed');

       SetColor(LightRed);
       SetTextStyle(SansSeriffont, HorizDir, 3);
       OutTextXY(GetMaxX div 2, GetMaxY-70 div 2, 'press any key to continue');
       WaitToGo;      { Waits for user to press any key }
       RestoreCrtMode; {Lets system goback to regular mode}
       CloseGraph;
    End;


Begin {GoodScreen}
     CheckBreak := False;      
     CheckForDriversandfonts;  {Checks to see if it has fonts that will be used by the program}
     SelectDriver;             {Selects appropriate Graphics Driver for the system}
     Good;                     {Main Graphic Good Screen}
End.  {GoodScreen}
