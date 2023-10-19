@echo off
setlocal enabledelayedexpansion
@echo "choose ur env: //todo"

set "file_AC=D:\Projects\WHUD\AC\core\pkg\icom\icom_export.sdh"
set "file_GC=D:\Projects\WHUD\GC\adapt\gen\tofac\core\pkg\icom\icom_export.sdh
set "search_word=INTERFACEID"

set "line1="
set "line2="

REM Find the line containing the search word/phrase in AC
for /f "tokens=*" %%a in ('type "%file_AC%" ^| find /n "%search_word%"') do (
    set "line1=%%a"
    set "line1=!line1:*]=!"
    echo !line1!
    goto :found1
)
@echo %%a
:found1

@echo line1
