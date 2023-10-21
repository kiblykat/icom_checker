@echo off
setlocal enabledelayedexpansion

set "file_AC=C:\Users\ASUS\Desktop\gitProj\icom_checker\icom_export.sdh"
set "file_GC=C:\Users\ASUS\Desktop\gitProj\icom_checker\icom_export_2.sdh"
set "search_word=INTERFACEID"

set "line1="
set "line2="

REM Find the line containing the search word/phrase in the first file
for /f "tokens=*" %%a in ('type "%file_AC%" ^| find /n "%search_word%"') do (
    set "line1=%%a"
    set "line1=!line1:*] =!"
    echo "AC: !line1!"
    goto :found1
)

:found1

REM Find the line containing the search word/phrase in the second file
for /f "tokens=*" %%a in ('type "%file_GC%" ^| find /n "%search_word%"') do (
    set "line2=%%a"
    set "line2=!line2:*] =!"
    echo "GC: !line2!"
    goto :found2
)

:found2

REM Compare the two lines
if not defined line1 (
    if not defined line2 (
        echo The search word/phrase was not found in either file.
    ) else (
        echo The search word/phrase was not found in %file_AC%.
    )
) else if not defined line2 (
    echo The search word/phrase was not found in %file_GC%.
) else (
    if "!line1!"=="!line2!" (
        echo Lines containing the search word/phrase are the same.
    ) else (
        echo Lines containing the search word/phrase are different.
    )
)

endlocal
