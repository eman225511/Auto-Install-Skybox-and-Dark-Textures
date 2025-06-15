@echo off
setlocal

:: Set console color (light cyan on black)
color 0B

:: Variable setup
set "rbx_versions=%LOCALAPPDATA%\Roblox\Versions"
set "dark_textures=%~dp0dark"
set "skybox_textures=%~dp0skybox"
set "rbx_storage=%LOCALAPPDATA%\Roblox\rbx-storage"
set "assets=%~dp0assets"

:: Header
echo.                                           
echo ============================================================
echo "         Roblox Dark Textures & Skybox Installer         "
echo ============================================================
echo.

:: Install Dark textures 
echo [QUESTION] Do you want to install DARK textures? (Y/N)
set /p install_dark_textures=
if /i not "%install_dark_textures%"=="Y" (
    echo.
    echo [INFO] Dark textures installation cancelled.
    goto :Skybox
)

if not exist "%rbx_versions%" (
    echo [ERROR] Roblox versions folder not found!
    goto :end
)

for /d %%V in ("%rbx_versions%\*") do (
    if exist "%%V\PlatformContent\pc\textures" (
        echo [*] Replacing textures in %%V\PlatformContent\pc\textures
        del /q "%%V\PlatformContent\pc\textures\*" >nul 2>&1
        xcopy /e /y /i "%dark_textures%\*" "%%V\PlatformContent\pc\textures\" >nul
    )
)

cls

:Skybox
:: Skybox patch installation
echo ============================================================
echo                Skybox Patch Installation
echo ============================================================
echo [QUESTION] Do you want to install the SKYBOX patch? (Y/N)
set /p install_skybox=

if /i not "%install_skybox%"=="Y" (
    echo.
    echo [INFO] Skybox installation cancelled.
    goto :end
)

if not exist "%assets%" (
    echo [ERROR] Assets folder not found!
    goto :end
)

mkdir "%rbx_storage%\a5" 2>nul
mkdir "%rbx_storage%\73" 2>nul
mkdir "%rbx_storage%\6c" 2>nul
mkdir "%rbx_storage%\92" 2>nul
mkdir "%rbx_storage%\78" 2>nul

copy /Y "%assets%\a564ec8aeef3614e788d02f0090089d8" "%rbx_storage%\a5\" 2>nul
attrib +R "%rbx_storage%\a5\a564ec8aeef3614e788d02f0090089d8" 2>nul

copy /Y "%assets%\7328622d2d509b95dd4dd2c721d1ca8b" "%rbx_storage%\73\" 2>nul
attrib +R "%rbx_storage%\73\7328622d2d509b95dd4dd2c721d1ca8b" 2>nul

copy /Y "%assets%\a50f6563c50ca4d5dcb255ee5cfab097" "%rbx_storage%\a5\" 2>nul
attrib +R "%rbx_storage%\a5\a50f6563c50ca4d5dcb255ee5cfab097" 2>nul

copy /Y "%assets%\6c94b9385e52d221f0538aadaceead2d" "%rbx_storage%\6c\" 2>nul
attrib +R "%rbx_storage%\6c\6c94b9385e52d221f0538aadaceead2d" 2>nul

copy /Y "%assets%\9244e00ff9fd6cee0bb40a262bb35d31" "%rbx_storage%\92\" 2>nul
attrib +R "%rbx_storage%\92\9244e00ff9fd6cee0bb40a262bb35d31" 2>nul

copy /Y "%assets%\78cb2e93aee0cdbd79b15a866bc93a54" "%rbx_storage%\78\" 2>nul
attrib +R "%rbx_storage%\78\78cb2e93aee0cdbd79b15a866bc93a54" 2>nul

cls

:: Install skybox textures
echo ============================================================
echo                Choose a Skybox Texture
echo ============================================================
setlocal enabledelayedexpansion
set count=0

for /d %%S in ("%skybox_textures%\*") do (
    set /a count+=1
    set "skybox_folder[!count!]=%%~nxS"
    echo   [!count!] %%~nxS
)

if %count%==0 (
    echo [ERROR] No skybox textures found.
    goto :end
)

echo.
set /p skybox_choice=Enter the number of the skybox you want to install: 

if not defined skybox_folder[%skybox_choice%] (
    echo [ERROR] Invalid choice.
    goto :end
)

set "chosen_skybox=%skybox_textures%\!skybox_folder[%skybox_choice%]!"

for /d %%V in ("%rbx_versions%\*") do (
    if exist "%%V\PlatformContent\pc\textures\sky" (
        echo [*] Installing skybox in %%V\PlatformContent\pc\textures\sky
        del /q "%%V\PlatformContent\pc\textures\sky\*.tex" >nul 2>&1
        copy /y "%chosen_skybox%\*.tex" "%%V\PlatformContent\pc\textures\sky\" >nul
    )
)
endlocal

:end
echo.
echo ============================================================
echo   Done! Press any key to exit.
echo ============================================================
pause >nul