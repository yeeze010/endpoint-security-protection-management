@echo off
setlocal

set "MVN_CMD=mvn"
where mvn >nul 2>nul
if errorlevel 1 (
  set "MVN_CMD=%~dp0..\.tools\apache-maven-3.9.9\bin\mvn.cmd"
)

"%MVN_CMD%" -f "%~dp0..\backend\pom.xml" %*
