%module my
%{
   #define SWIG_FILE_WITH_INIT
   #include "my.h"
%}

%include "carrays.i"
%array_functions(int,intArray)
%include "my.h"
