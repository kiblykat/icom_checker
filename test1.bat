@echo off
setlocal enabledelayedexpansion

set "searchKey=pause"
set "replace= " 

for /f "tokens=*" %%a in (pressKey.bat) do (
    set "line=%%a"
    
    set "line=!line:%search%=%replace%!"
    echo !line!
) > pressKey.bat
 
echo %line%
echo !line!
