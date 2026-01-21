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
exit /b 0
