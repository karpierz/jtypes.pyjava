@echo off
setlocal
set JAVA_HOME=C:\Program Files\Zulu\zulu-11
set javac="%JAVA_HOME%\bin\javac" -encoding UTF-8 -g:none ^
          -deprecation -Xlint:unchecked --release 8

pushd "%~dp0"\tests
rmdir /Q/S java-tests\classes 2> nul & mkdir java-tests\classes
dir /S/B/O:N ^
    java-tests\pyjavatest\*.java ^
    2> nul > build.fil
%javac% -d java-tests/classes -classpath java-tests/lib/* @build.fil
del /F/Q build.fil
popd

:exit
endlocal
