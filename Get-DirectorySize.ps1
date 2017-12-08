<#
.SYNOPSIS
Calculates the size of each top level directory at the given path and displays a summary.
Author: Doron Chosnek, November 2017

.DESCRIPTION
This script will discover the directories that exist at a given path and then preform a recursive search for each.
It will calculate and display the total size of all files in each directory.

If you don't specify a path, the script will use the current working directory.

.PARAMETER Path
This optional parameter specifies the path to be examined.

.NOTES
  Version:        1.0
  Author:         Doron Chosnek
  Creation Date:  November 2017
  Purpose/Change: Initial script development

.EXAMPLE
 Get-DirectorySize.ps1
    Calculate the size of all the folders located in the current working directory.
.EXAMPLE
 Get-DirectorySize.ps1 -Path $HOME
    Calculate the size of all the folders located in the current user's home directory.
.EXAMPLE
 Get-DirectorySize.ps1 -Path 'c:\program files\'
    Calculate the size of all the folders in the Program Files directory.
#>


param(
    [Parameter(Mandatory=$False,ValueFromPipeline=$False)][string]$Path=$PSScriptRoot
)

# get the folders at the given path (just the top level)
$toplevel = Get-ChildItem -Path $Path | ? { $_ -is [System.IO.DirectoryInfo] }

$largest = 0
$counter = 0
$all_dirs = @()

# step through each folder and calculate the size of all files (recursively) within
foreach($f in $toplevel)
{
    $counter += 1
    Write-Progress -Activity "Calculating directory size" -Status $f.Name -PercentComplete ($counter*100/$toplevel.Count)

    # this single line calculates the total size of all files in all subfolders
    $bytes = (Get-ChildItem $f.FullName -Recurse -ErrorAction SilentlyContinue | ? { $_ -is [System.IO.FileInfo] } | Measure-Object -Sum Length).Sum

    # we use the size of the largest file to determine whether the output should be expressed in B, MB, GB, etc.
    $largest = if($bytes -gt $largest) { $bytes } else { $largest }

    $current_dir = "" | select Name, Bytes, Size
    $current_dir.Name = $f.Name
    $current_dir.Bytes = $bytes

    $all_dirs += $current_dir
}

# calculate which unit of measurement to use for file size
$abbreviations = @(' B ', ' KB', ' MB', ' GB', ' TB', ' PB')
$index = [math]::floor([math]::log( $largest ) / [math]::log( 1024 ))

$all_dirs | % { 
    $tmp = $_.Bytes / [math]::pow(1024, $index)
    $_.Size = ($tmp.ToString("0.0000")).PadLeft(9) + $abbreviations[$index]
}

$all_dirs | sort -Descending Bytes | ft Size, Name -AutoSize
