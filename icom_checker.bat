@echo off
REM start logFile
set logFile=logFile.txt

echo Script started at %date% %time% >> %logFile%

setlocal enabledelayedexpansion

REM need to further streamline, just prompt AC folder. the relative folder to toFGC and toFAC can be hardcoded
set /p buildFolderAC=Choose build folder for AC:
set /p buildFolderGC=Choose build folder for GC:
set "file_AC=%buildFolderAC%\core\pkg\icom\icom_export.sdh" 
set "file_GC=%buildFolderGC%\adapt\gen\tofac\core\pkg\icom\icom_export.sdh"
set "search_word=INTERFACEID"

set "line1="
set "line2="

REM Find the line containing the search word/phrase in AC
for /f "tokens=*" %%a in ('type "%file_AC%" ^| findstr "%search_word%"') do (
    set "line1=%%a"
    set "line1=!line1:*] =!" 
    echo "AC: !line1!"
    goto :found1
)

:found1

REM Find the line containing the search word/phrase in GC
for /f "tokens=*" %%a in ('type "%file_GC%" ^| find "%search_word%"') do (
    set "line2=%%a"
    set "line2=!line2:*] =!"
    echo "GC: !line2!"
    goto :found2
)

:found2

REM Compare the two lines
if not defined line1 (
    if not defined line2 (
        echo "INTERFACEID" not found in either file.
    ) else (
        echo "INTERFACEID" not found in %file_AC%.
    )
) else if not defined line2 (
    echo "INTERFACEID" not found in %file_GC%.
) else (
    if "!line1!"=="!line2!" (
        echo Your folders are synced. Congratulations
        echo Script finished at %date% %time%
        exit /b
    ) else (
        echo Your folders are not synced. Proceeding with ICOM build syncing...
        timeout /t 2 >nul
        echo Please gitclean project folders before running ICOM sync
        timeout /t 5
        goto :proceedWithBuild
    )
)


:proceedWithBuild
REM can be made more streamlined. For now this works as MVP :)
:retryA
set /p buildAC=Choose build variant for AC:
IF EXIST "%buildAC%" (
    echo You have chosen: %buildAC%
) else (
    echo Batch file not found.
	goto retryA
)


:retryB
set /p buildGC=Choose build variant for GC:
IF EXIST "%buildGC%" (
    echo You have chosen: %buildGC%
) else (
    echo Batch file not found.
	goto retryB
)

REM ---------- KIV ----------------
REM set /p ACorGC=Choose which system to run first: 
REM find total time required to do whole ICOM sync

REM ---RUN AC BUILD--- 
echo running AC batch file: %buildAC%
timeout /t 5
call "%buildFolderAC%\%buildAC%.bat"
echo SUCCESS: Successfully run AC project build

REM ---COPY AC TO GC FOLDER---
echo copying files from AC to GC
xcopy "%buildFolderAC%\adapt\gen\ToFGC\core\pkg" "%buildFolderGC%\core\pkg" /E /I /H /Y
echo SUCCESS: copied files from AC to GC
timeout /t 2

REM ---RUN GC BUILD--- 
echo running GC batch file: %buildGC%
timeout /t 5
call "%buildFolderGC%\%buildGC%.bat"
echo SUCCESS: Successfully run GC project build

REM ---COPY GC TO AC FOLDER---
echo copying files from GC to AC
xcopy "%buildFolderGC%\adapt\gen\tofac\core\pkg" "%buildFolderAC%\core\pkg" /E /I /H /Y
echo SUCCESS: copied files from GC to AC
timeout /t 2

REM ---RUN AC BUILD--- 
timeout /t 5
echo Please gitclean project folders before running ICOM sync
echo running AC batch file %buildAC%
call "%buildFolderAC%\%buildAC%"
echo SUCCESS: Successfully run AC project build

endlocal

REM end logFile
echo Script finished at %date% %time% >> %logFile%
exit /b