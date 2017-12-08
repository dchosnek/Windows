<#
.SYNOPSIS
  Clear RDP client history in Windows
.DESCRIPTION
  Clear RDP client history in Windows. Script has no inputs or outputs.
.INPUTS
  None
.OUTPUTS
  None
.NOTES
  Version:        1.0
  Author:         Doron Chosnek
  Creation Date:  February 2017
  Purpose/Change: Initial script development
#>

# This line is optional and simply shows a history of all RDP sessions ever made from this computer.
# Comment it out if you don't want to see that information.

Get-ChildItem -Path 'HKCU:\Software\Microsoft\Terminal Server Client\Servers'

# First remove the history of the last 10 RDP connections, which will be named MRU0 through MRU9.
# This is a fast operation, so we just delete all 10 without checking first to see if they exist.

0..9 | % { Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Terminal Server Client\Default' -Name MRU$_ -ErrorAction SilentlyContinue }

# The 'Servers' directory holds the list of all connections ever made from this computer. This
# operation simply retrieves each one and deletes it.

Get-ChildItem -Path 'HKCU:\Software\Microsoft\Terminal Server Client\Servers' | % { Remove-Item -Path Registry::$_ }

# There is a hidden file in the user's Documents folder that contains the most recent

Remove-Item $HOME\Documents\Default.rdp -Force