@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

:: ===========================================
:: AI Skill Factory - Local Windows Generator
:: ===========================================

echo ============================================
echo AI Skill Factory - Local Windows Generator
echo ============================================
echo.

:: Configuration
set "REPO_DIR=%~dp0"
set "GENERATOR_DIR=%REPO_DIR%generator"
set "VENV_DIR=%REPO_DIR%venv"
set "PYTHON_SCRIPT=generate.py"

:: Change to repository directory
cd /d "%REPO_DIR%"

:: Check for virtual environment
if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [Setup] Activating virtual environment...
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    echo [Setup] No venv found, using system Python...
)

:: Verify Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python and add it to PATH
    exit /b 1
)

:: Verify Claude CLI is available
claude --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Claude CLI not found!
    echo Please install: npm install -g @anthropic-ai/claude-code
    exit /b 1
)
echo [Setup] Claude CLI verified

:: Parse command line arguments
set "STRATEGY=auto"
set "TOPIC="
set "SKIP_GIT=0"
set "SKIP_VALIDATION=0"

:parse_args
if "%~1"=="" goto :check_args
if /i "%~1"=="--strategy" (
    set "STRATEGY=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--topic" (
    set "TOPIC=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--skip-git" (
    set "SKIP_GIT=1"
    shift
    goto :parse_args
)
if /i "%~1"=="--skip-validation" (
    set "SKIP_VALIDATION=1"
    shift
    goto :parse_args
)
if /i "%~1"=="--help" (
    goto :show_help
)
shift
goto :parse_args

:check_args
echo.
echo [Config] Strategy: %STRATEGY%
if defined TOPIC echo [Config] Topic: %TOPIC%
if "%SKIP_GIT%"=="1" (
    echo [Config] Git: Disabled
) else (
    echo [Config] Git: Auto commit/push enabled
)
if "%SKIP_VALIDATION%"=="1" echo [Config] Validation: Disabled
echo.

:: Build the command
set "CMD=python "%GENERATOR_DIR%\%PYTHON_SCRIPT%" --use-claude-cli --strategy "%STRATEGY%""

if defined TOPIC (
    set "CMD=%CMD% --topic "%TOPIC%""
)

if "%SKIP_GIT%"=="0" (
    set "CMD=%CMD% --auto-git"
)

if "%SKIP_VALIDATION%"=="1" (
    set "CMD=%CMD% --skip-validation"
)

:: Run the generator
echo [Run] Executing skill generator...
echo.
%CMD%

set "EXIT_CODE=%errorlevel%"

if %EXIT_CODE% neq 0 (
    echo.
    echo [ERROR] Generator failed with exit code %EXIT_CODE%
    exit /b %EXIT_CODE%
)

echo.
echo ============================================
echo Generation complete!
echo ============================================

:: Monitor GitHub Actions if gh CLI is available and git was used
if "%SKIP_GIT%"=="1" goto :done

:: Find gh CLI (check PATH first, then common install location)
set "GH_CMD=gh"
where gh >nul 2>&1
if errorlevel 1 (
    if exist "C:\Program Files\GitHub CLI\gh.exe" (
        set "GH_CMD=C:\Program Files\GitHub CLI\gh.exe"
    ) else (
        echo.
        echo [Info] gh CLI not installed. Skipping Actions monitoring.
        echo        Install with: winget install GitHub.cli
        goto :done
    )
)

"%GH_CMD%" auth status >nul 2>&1
if errorlevel 1 (
    echo.
    echo [Info] gh CLI not authenticated. Skipping Actions monitoring.
    echo        Run: gh auth login
    goto :done
)

echo.
echo [Actions] Monitoring GitHub Actions workflow...
echo [Actions] Waiting for workflow to start...

:: Wait for workflow to start (max 30 seconds)
set "WAIT_COUNT=0"
:wait_for_workflow
timeout /t 5 /nobreak >nul
set /a WAIT_COUNT+=1

for /f "tokens=1,2" %%a in ('"%GH_CMD%" run list --limit 1 --json status^,conclusion -q ".[0] | \"\(.status) \(.conclusion // \"none\")\"" 2^>nul') do (
    set "RUN_STATUS=%%a"
    set "RUN_CONCLUSION=%%b"
)

if "%RUN_STATUS%"=="in_progress" (
    echo [Actions] Workflow in progress...
    if %WAIT_COUNT% lss 24 goto :wait_for_workflow
    echo [Actions] Timeout waiting for workflow. Check manually.
    goto :done
)

if "%RUN_STATUS%"=="queued" (
    echo [Actions] Workflow queued...
    if %WAIT_COUNT% lss 24 goto :wait_for_workflow
)

if "%RUN_STATUS%"=="completed" (
    if "%RUN_CONCLUSION%"=="success" (
        echo [Actions] Workflow completed successfully!
        echo [Actions] Blog deployed to https://rs1017.github.io/
    ) else (
        echo [Actions] Workflow FAILED!
        echo.
        echo [Actions] Fetching error logs...
        for /f %%i in ('"%GH_CMD%" run list --limit 1 --json databaseId -q ".[0].databaseId"') do set "RUN_ID=%%i"
        "%GH_CMD%" run view !RUN_ID! --log-failed 2>nul || "%GH_CMD%" run view !RUN_ID! --log 2>nul | findstr /i "error fail"
        echo.
        echo [Actions] View full logs: "%GH_CMD%" run view !RUN_ID! --log
        exit /b 1
    )
)

:done
endlocal
exit /b 0

:show_help
echo.
echo Usage: generate_skill.bat [options]
echo.
echo Options:
echo   --strategy ^<type^>   Topic selection strategy
echo                        (auto, keyword, trend, request, extend)
echo                        Default: auto
echo.
echo   --topic ^<text^>      Specific topic to generate
echo                        Example: --topic "Git 커밋 분석 스킬"
echo.
echo   --skip-git           Skip automatic git commit/push
echo.
echo   --skip-validation    Skip content validation
echo.
echo   --help               Show this help message
echo.
echo Examples:
echo   generate_skill.bat
echo   generate_skill.bat --strategy keyword
echo   generate_skill.bat --topic "API 통합 스킬"
echo   generate_skill.bat --skip-git
echo   generate_skill.bat --skip-validation
echo.
echo GitHub Actions Monitoring:
echo   If gh CLI is installed, the script will automatically monitor
echo   the deployment workflow and report success/failure.
echo   Install gh CLI: winget install GitHub.cli
echo   Authenticate: gh auth login
echo.
exit /b 0
