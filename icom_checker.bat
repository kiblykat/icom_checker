@echo off
REM start logFile

set logFile=logFile.txt

echo Script started at %date% %time% >> %logFile%

setlocal enabledelayedexpansion

REM need to further streamline, just prompt AC/GC folder. the relative folder to toFGC and toFAC can be hardcoded
:retryFolderAC
set /p buildFolderAC=Choose build folder for AC:
IF NOT EXIST "%buildFolderAC%" (
    echo AC Project Folder not found. Please check misspelling.
	goto retryFolderAC
)

:retryFolderGC
set /p buildFolderGC=Choose build folder for GC:
IF NOT EXIST "%buildFolderGC%" (
    echo GC Project Folder not found. Please check misspelling.
	goto retryFolderGC
)

set "file_AC=%buildFolderAC%\core\pkg\icom\icom_export.sdh" 
set "file_GC=%buildFolderGC%\adapt\gen\tofac\core\pkg\icom\icom_export.sdh"
set "search_word=INTERFACEID"

set "line1="
set "line2="

REM Find the line containing the search word/phrase in AC
for /f "tokens=*" %%a in ('type "%file_AC%" ^| findstr "%search_word%"') do (
    set "line1=%%a"
    echo "AC: !line1!"
    goto :found1
)

:found1

REM Find the line containing the search word/phrase in GC
for /f "tokens=*" %%a in ('type "%file_GC%" ^| find "%search_word%"') do (
    set "line2=%%a"
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
        echo Press any key to continue...
        pause > nul
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
:retryBuildAC
set /p buildAC=Choose build variant for AC:
IF EXIST "%buildFolderAC%\%buildAC%.bat" (
    echo You have chosen: %buildAC%.bat
) else (
    echo Batch file not found.
    echo Your chosen directory: "%buildFolderAC%\%buildAC%.bat"
	goto retryBuildAC
)


:retryBuildGC
set /p buildGC=Choose build variant for GC:
IF EXIST "%buildFolderGC%\%buildGC%.bat" (
    echo You have chosen: %buildGC%.bat
) else (
    echo Batch file not found.
    echo Your chosen directory: "%buildFolderGC%\%buildGC%.bat"
	goto retryBuildGC
)

REM ---------- KIV ----------------
REM set /p ACorGC=Choose which system to run first: 
REM find total time required to do whole ICOM sync

REM ---RUN AC BUILD--- 
echo running AC batch file: %buildAC%
echo "%buildFolderAC%\%buildAC%.bat"
REM enter project folder due to relative path within build batch
cd "%buildFolderAC%\%buildAC%"
echo Current folder: %CD%

timeout /t 5
CALL "%buildFolderAC%\%buildAC%.bat"
echo SUCCESS: Successfully run AC project build

REM ---COPY AC TO GC FOLDER---
echo copying files from AC to GC
xcopy "%buildFolderAC%\adapt\gen\ToFGC\core\pkg" "%buildFolderGC%\core\pkg" /E /I /H /Y
echo SUCCESS: copied files from AC to GC
timeout /t 2

REM ---RUN GC BUILD--- 
echo running GC batch file: %buildGC%
echo "%buildFolderGC%\%buildGC%.bat"
REM enter project folder due to relative path within build batch
cd "%buildFolderGC%\%buildGC%"
echo Current folder: %CD%

timeout /t 5
CALL "%buildFolderGC%\%buildGC%.bat"
echo SUCCESS: Successfully run GC project build

REM ---COPY GC TO AC FOLDER---
echo copying files from GC to AC
xcopy "%buildFolderGC%\adapt\gen\tofac\core\pkg" "%buildFolderAC%\core\pkg" /E /I /H /Y
echo SUCCESS: copied files from GC to AC
timeout /t 2

REM ---RUN AC BUILD--- 
echo running AC batch file: %buildAC%
echo "%buildFolderAC%\%buildAC%.bat"
REM enter project folder due to relative path within build batch
cd "%buildFolderAC%\%buildAC%"
echo Current folder: %CD%

timeout /t 5
CALL "%buildFolderAC%\%buildAC%.bat"
echo SUCCESS: Successfully run AC project build


REM ---AC: GET_PRG, GET_SYM---
echo AC: Running get_prg and get_sym
CALL %buildFolderAC%\tool\integration\tool\deliver\core\get_prg.bat
CALL %buildFolderAC%\tool\integration\tool\deliver\core\get_sym.bat

REM ---GC: GET_PRG, GET_SYM---
echo GC: Running get_prg and get_sym
CALL %buildFolderGC%\tool\integration\tool\deliver\core\get_prg.bat
CALL %buildFolderGC%\tool\integration\tool\deliver\core\get_sym.bat

endlocal

REM end logFile
echo Script finished at %date% %time% >> %logFile%
echo Press any key to continue...
pause > nul
exit /b