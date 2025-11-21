@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build
set HTML_BUILD_DIR=%BUILDDIR%\html
set HTML_PUBLISH_DIR=..\docs

REM Check if sphinx-build is available
%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
    echo.
    echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
    echo.installed, then set the SPHINXBUILD environment variable to point
    echo.to the full path of the 'sphinx-build' executable. Alternatively you
    echo.may add the Sphinx directory to PATH.
    echo.
    echo.If you don't have Sphinx installed, grab it from
    echo.https://www.sphinx-doc.org/
    exit /b 1
)

if "%1" == "" goto help
if "%1" == "html" goto html
if "%1" == "clean" goto clean

REM Catch-all for other commands like latexpdf, epub, etc.
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:html
echo.Building HTML...
%SPHINXBUILD% -M html %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
if errorlevel 1 (
    echo.HTML build failed.
    goto end
)
echo.
echo.Syncing HTML output to publish directory...
REM Use robocopy to mirror the build output. /e = copy subdirs, /purge = delete destination files not in source.
robocopy "%HTML_BUILD_DIR%" "%HTML_PUBLISH_DIR%" /e /purge /xf .buildinfo /xf .buildinfo.bak /xd doctrees >NUL
echo.Build finished. The HTML pages are in %HTML_PUBLISH_DIR%.
goto end

:clean
echo.Cleaning custom publish directory...
REM Check if the publish directory exists before trying to remove it
if exist "%HTML_PUBLISH_DIR%" (
    rmdir /s /q "%HTML_PUBLISH_DIR%"
)
mkdir "%HTML_PUBLISH_DIR%"
echo.
echo.Running standard Sphinx clean...
%SPHINXBUILD% -M clean %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
