# Windows Scripts

This is a collection of random scripts that have come in handy for Microsoft Windows machines.

## dirsize.py

This Python script actually works for both Windows and MacOS environments. It displays the total size of each main directory at the given path. The purpose is to determine which directory consumes the most disk space. The user can then run the script against that directory to drill down further.

I first created this script because I was running out of disk space and found it very difficult to determine which of the 30+ directories at `%AppData%` was the culprit.

No special libraries are required. A progress bar is displayed while calculating directory sizes.

### How to run

The script only has one argument: the directory name.
```
python dirsize.py C:\Windows
```
When running the script from a PowerShell window (rather than cmd.exe), you can use PowerShell shortcuts for path.
```
python dirsize.py $HOME\Documents
```
When running the script in MacOS, you can use inputs like `..\` or `~`.
```
python dirsize.py ~/Documents
```

## Get-DirectorySize.ps1

This is the PowerShell equivalent of the dirsize.py Python script in this directory. No special libraries are required. A progress bar is displayed during the calculation using the PowerShell `Write-Progress` cmdlet.

### How to run

The script only has one parameter: the directory path. This parameter is OPTIONAL and will default to the path where the script is located if not specified.

```
Get-DirectorySize.ps1 $HOME\Documents
```
or
```
Get-DirectorySize.ps1 -Path $HOME\Documents
```
## Authors

* **Doron Chosnek** - *Initial work* - [GitHub](https://github.com/dchosnek)

## Acknowledgments

* https://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
* https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
