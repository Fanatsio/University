*README_HELP

  Introduction to VP-Expert Release 2.1 Hypertext README File
  
  You will see a series of labels on the bottom of the screen.
  Pointing and clicking on these with the mouse will cause the
  corresponding hypertext index to be displayed or the program
  to end.

  Alternatively, you can point and click on the hyperwords in
  the text.  On EGA and VGA displays these words will appear in 
  white on other display types they will simply be in upper case.
  The word "index" above is a hyperword.

  NOTE: If you do not have a mouse, use the following method to
  select a hyperword: Press the TAB key, type the desired
  hyperword, then press ENTER. Use "index" to get a list of all
  the possible topics.  When you wish to exit, simply type "exit".
*VPXHELP

   The VP-Expert Help System has been improved in several ways.

    - Each topic is now cross referenced to related topics.
    - Several new keystroke commands have been added that work
      while in a given help topic.

        Ctrl-Home : Takes you to the first topic in the list.
        Ctrl-End  : Takes you to the last topic in the list.
        Ctrl-PgUp : Takes you to the previous topic in the list.
        Ctrl-PgDn : Takes you to the next topic in the list.

    - The help text file and index file (VPXHELP.HLP & VPXHELP.IDX)
      have been compressed into a single file called VPXHELP.CHP.
    - A program has been added to allow you to create your own
      custom help files for use with VPX.  Run the batch file called
      MYHELP.BAT on the Samples Files Disk for to get information on
      creating your own help files.
*EDITOR_HELP

  EDITOR_HELP:

  Because of the memory requirements of VP-Expert and the VP-Expert
  Editor there is not enough free RAM available to run the Help
  system from within the Editor.  If you want to access the Help
  system from within the Editor you will need to run the Editor
  directly from DOS.  To do this type VPXE MYFILE.KBS  at the DOS 
  prompt.  At this point you can press F1 to access the help system.
*LOAD_PATH

  LOAD_PATH:

  VP-Expert has been enhanced so that it will now search for its
  support files in the directory from which it was loaded rather
  than the current directory.  This means you can put your \VPX
  subdirectory in your path and run the program from any other
  directory on your hard disk drive.  For example, if you keep all
  of your KBS files in a subdirectory called \KBS, rather than
  using the Path command in VP-Expert to access these files you
  can simply switch to the \KBS subdirectory before starting VP-Expert.
*INDUCTION

  INDUCTION:
  
  VP-Expert's induction facility now supports approximately
  500 examples instead of the previous limit of 126.  This allows
  for much larger decision tables to be quickly converted into
  executable expert systems.
*USING_PATHS

  USING_PATHS:
  
  All clauses and statements which refer to DOS files (e.g. SHIP,
  RECEIVE, CALL, etc) now support a DOS path in the following order
  of precedence.
  
   1) Current DOS Directory
   2) Path specified using PATH menu command.
   3) "Hard-coded" path using the actual clause or statement itself.
*NETWORKS

  VP-Expert has been tested under a NOVELL Network and works properly
  except for these limitations:

   - Two users cannot edit the same file at the same time.
   - Two users cannot access the same DBF file using GET or PUT at
     the same time.
   - Two users cannot access the same WKS file using WKS or PWKS at
     the same time.
     
   If two people attempt to access the same file with the above commands
   or any of the others which need to open a file for Read/Write access
   (SHIP, REPORT, FDISPLAY, or SAVEFACTS) the second person will get
   an Access Denied Runtime Error.
   
   The following clauses open files on a read only basis and can be
   used jointly: (MENU, RECEIVE, SHOWTEXT, HYPERTEXT, LOADFACTS).
*GMODE_CHANGES

  GMODE_CHANGES:

  The default state for the mouse in GMODE consultations is now OFF.
  If you wish to use the mouse you must include a MOUSEON before the
  GMODE clause.  Previously the default was ON.

  In VP-Expert version 2.0, 2.01, and 2.02 it was necessary to issue
  a TMODE statement at the end of a GMODE consultation to restore the
  video to TMODE to display the menus.  This is no longer necessary
  in version 2.1, and in fact using it will cause a screen flash at
  the end of the consultation.
*MOUSE_LIMITS

  MOUSE_LIMITS:

  If you are using a Logitech(tm) mouse with an EGA display and intend
  to use GMODE 16 you should be sure to include your MOUSEON statement
  BEFORE the GMODE statement.  If the MOUSEON is issued after the GMODE
  statement the range of the mouse will be limited to the top half of
  the display.  This does not happen with the Microsoft mouse.

  VP-Expert does not currently support the IN-PORT Microsoft mouse on
  a Hercules display when using GMODE 8.  If you are using a serial
  version of the Microsoft mouse with a mouse driver version lower 
  than 6.0 you should have no problem.

  We are working to correct these problems with the vendors.
*HALTING_KBS

  HALTING_KBS:

  Previously you could use Ctrl-C or Ctrl-Break to terminate a
  consultation in progress.  This has been changed.  If you wish
  quit a consultation in TEXT (TMODE) mode use the /Quit command when
  prompted at the bottom of the screen.  If the consultation
  is in GMODE (text or graphics) you can use the <Escape> key.
*VGA_SUPPORT

  VGA_SUPPORT:

  VP-Expert does not currently support GMODE 18 (640x480) correctly.
  We recommend using GMODE 16 instead.  We are working to remove this
  limitation.
*CHOICES
  
  CHOICES:

  The maximum number of choices that can be displayed is 60 for a runtime
  system and 24 for a non-runtime system.  If you have more than the 
  allowed number of choices a warning will be generated that the menu 
  has been truncated.  The last issue of our newsletter (README.PSI) 
  incorrectly stated that the limit would be 160.
*CHAINING

  CHAINING:

  It is now possible to chain in GMODE without clearing the screen.
  Make sure that the knowledge base that you are chaining FROM does
  not issue a GMODE or TMODE clause prior to the CHAIN command.
  Additionally, make sure the knowledge base you are chaining TO
  does not issue a GMODE or TMODE clause because this will clear the
  display.

  In addition, it is no longer necessary to have an EXECUTE statement.
  in the knowledge base you are chaining to.
*EXECUTE

  EXECUTE:

  When you consult a KBS file which contains an EXECUTE statement you
  will always be returned to DOS when the consultation ends.  This is
  to allow you to run several consultations in a row from a batch file.
  For development purposes it is best not use the EXECUTE command since
  you will have to restart VP-Expert each time you run a consultation
  if you do.
*GCOLOR

  GCOLOR:

  The GCOLOR clause can now be used to change the color of text displayed
  with the GDISPLAY clause.
*GBCOLOR

  GBCOLOR:
 
  The GBCOLOR clause now works as documented.

*HERCULES

  Special instructions for users of Hercules(tm) display adapters

  If you plan on using GMODE 8 in VP-Expert 2.1, you must run
  VPXHERC.COM before executing VP-Expert.  This program loads
  special RAM-resident video display drivers which provide
  Hercules support during .KBS execution.  Upon executing 
  VP-Expert, these drivers will remain in memory (using about 7K
  of RAM) until you re-boot your computer.

  You should also make sure that you are running your Hercules
  card in "full" mode.  This is accomplished by typing:
  HGC FULL  <enter>
  at the DOS prompt.

  The HGC.COM utility should be provided with your Hercules card.
*CALL_SYNTAX

    CALL & CCALL
    IMPORTANT NOTE:
    VP-Expert now supports passing command line parameters to
    external programs.  As a result, any existing knowledge
    bases which use CALL or CCALL will need to be modified.

    THE NEW SYNTAX FOR CALL AND CCALL IS:

        CALL  program_name,"parameter1 parameter2 etc."
        CCALL program_name,"parameter1 parameter2 etc."

    If no parameters are passed you must still include a
    comma and two double quotes after the program name. i.e.

       CALL program_name,""

    ADDITIONAL NOTES:
    - The maximum length of the command line string is 63 characters.
    - BCALL does not support command line arguments.
    - See CALL_SYNTAX2 for an example using variables.   
*CALL_SYNTAX2       

    CALL & CCALL (continued)

    Using variables in command line strings:

    Besides being able to pass literal text strings to a called 
    program, you can also use variables inside of the quotes.
    You can embed variables in the string by including them in
    curly brackets.  For example:
    
                       program = MYPROG
                       parameter1 = TESTFILE
                       CALL @program,"{parameter1} -c"
                       
     Would be equivalent to:
     
                      MYPROG TESTFILE -c
*COUNT

  COUNT:

  COUNT is now a reserved word.  Make sure you don't use it as a
  variable name or you will get a syntax error.
*PWKS

  The PWKS Clause

    The PWKS clause now has the ability to write any type of
    data to cells of a WKS file. In addition, PWKS can now be
    used to store data into cells which did not previously
    contain data.

    Notes:  When using PWKS to replace existing data in a spreadsheet
    file the PWKS clause does not remove the existing data.  To remove
    the existing data from the file it is necessary to retrieve and 
    resave it using your spreadsheet program.
*FILE_LIST

  FILE_LIST:
  
  The main Program Disk contains a file called FILES.LST which describes
  all of the files contained on the VP-Expert Program Disk as well as
  the Sample Files Disk.  You can view this file by using the DOS 
  command:
  
       A>TYPE FILES.LST
       
  or print it using the DOS command:
  
       A>COPY FILES.LST PRN
       
  Please Note: This list is more up to date than the list found in the
               VP-Expert Manual.
  
*INDEXER

  INDEXER:

  The INDEXER.BAS program has been rewritten in assembly language and
  is now about 100 times faster.  The new file is called INDEXER.COM
  and works identically to INDEXER.BAS.
*INDEX
HELP TOPIC LIST:

  CALL_SYNTAX               CALL_SYNTAX2              CHAINING                  
  CHOICES                   COUNT                     EDITOR_HELP               
  EXECUTE                   FILE_LIST                 GBCOLOR                   
  GCOLOR                    GMODE_CHANGES             HALTING_KBS               
  HERCULES                  INDEX                     INDEXER                   
  INDUCTION                 LOAD_PATH                 MOUSE_LIMITS              
  NETWORKS                  PWKS                      README_HELP               
  USING_PATHS               VGA_SUPPORT               VPXHELP                   

   If you don't have a mouse you can always get to this screen by typing
   INDEX into the formfield below.