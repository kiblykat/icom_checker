@echo off
REM start logFile
set logFile=logFile.txt

echo Script started at %date% %time% >> %logFile%
setlocal enabledelayedexpansion

REM need to further streamline, just prompt AC folder. the relative folder to toFGC and toFAC can be hardcoded
set /p buildFolderAC=Choose build folder for AC:
set /p buildFolderGC=Choose build folder for GC:
set "file_AC=%buildFolderAC%\icom_export.sdh" 
set "file_GC=%buildFolderGC%\icom_export_2.sdh"
set "search_word=INTERFACEID"

set "line1="
set "line2="

REM Find the line containing the search word/phrase in AC
for /f "tokens=*" %%a in ('type "%file_AC%" ^| find /n "%search_word%"') do (
    set "line1=%%a"
    set "line1=!line1:*] =!"
    echo "AC: !line1!"
    goto :found1
)

:found1

REM Find the line containing the search word/phrase in GC
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
        echo "INTEFACEID" found in either file.
    ) else (
        echo "INTEFACEID" was not found in %file_AC%.
    )
) else if not defined line2 (
    echo "INTEFACEID" was not found in %file_GC%.
) else (
    if "!line1!"=="!line2!" (
        echo Your folders are synced. Congratulations
        exit /b
    ) else (
        echo Your folders are not synced. Proceeding with ICOM build syncing...
        timeout /t 1 >nul
        echo Please ensure clean project folders before running ICOM sync
        timeout /t 2 >nul
        goto :proceedWithBuild
    )
)


:proceedWithBuild
REM can be made more streamlined. For now this works as MVP :)
set /p buildAC=Choose build variant for AC:
set /p buildGC=Choose build variant for GC:

REM ---------- KIV ----------------
REM set /p ACorGC=Choose which system to run first: 
REM find total time required to do whole ICOM sync

REM ---RUN AC BUILD--- 
echo running AC batch file %buildAC%
echo running in 5 seconds
timeout /t 5
call "%buildFolderAC%\%buildAC%.bat"
echo finish running batch file

REM ---COPY AC TO GC FOLDER---
echo copying files from AC to GC
xcopy "%buildFolderAC%\toFGC" "%buildFolderGC%\copyAChere" /E /I /H /Y

REM ---RUN GC BUILD--- 
echo running AC batch file %buildGC%
timeout /t 5
call "%buildFolderGC%\%buildGC%.bat"
echo finish running batch file

REM ---COPY GC TO AC FOLDER---
echo copying files from GC to AC
xcopy "%buildFolderGC%\toFAC" "%buildFolderAC%\copyGChere" /E /I /H /Y

REM ---RUN AC BUILD--- 
echo running AC batch file %buildAC%
timeout /t 5
call "%buildFolderAC%\%buildAC%"
echo finish running batch file

endlocal

REM end logFile
echo Script finished at %date% %time% >> %logFile%