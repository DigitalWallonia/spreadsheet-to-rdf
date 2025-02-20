@echo off 
REM Change directory to the location of your script  
cd /d C:\Users\138\Documents\GitHub\spreadsheet-to-rdf

REM Run the Python script with command-line arguments  
"C:\Users\138\Documents\GitHub\spreadsheet-to-rdf\.venv\Scripts\python.exe" app.py -c config.yaml  

REM Optionally pause to see the output  
pause   