@echo off
chcp 65001 >nul
echo ============================================
echo AI Skill Factory - 스케줄러 등록
echo ============================================
echo.

:: 관리자 권한 확인
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 관리자 권한이 필요합니다.
    echo         이 파일을 우클릭하고 "관리자 권한으로 실행"을 선택하세요.
    pause
    exit /b 1
)

set "SCRIPT_DIR=%~dp0"

echo [1/2] 평일 스케줄 등록 (월-금 12:30)...
schtasks /create /xml "%SCRIPT_DIR%weekday_task.xml" /tn "AI Skill Factory - Weekday" /f
if errorlevel 1 (
    echo [ERROR] 평일 스케줄 등록 실패
) else (
    echo [OK] 평일 스케줄 등록 완료
)

echo.
echo [2/2] 주말 스케줄 등록 (토-일 12:30~21:30, 1시간 간격)...
schtasks /create /xml "%SCRIPT_DIR%weekend_task.xml" /tn "AI Skill Factory - Weekend" /f
if errorlevel 1 (
    echo [ERROR] 주말 스케줄 등록 실패
) else (
    echo [OK] 주말 스케줄 등록 완료
)

echo.
echo ============================================
echo 등록된 작업 확인:
echo ============================================
schtasks /query /tn "AI Skill Factory - Weekday" /fo list | findstr /i "TaskName Status"
schtasks /query /tn "AI Skill Factory - Weekend" /fo list | findstr /i "TaskName Status"

echo.
echo 완료! 작업 스케줄러에서 확인하세요.
pause
