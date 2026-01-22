A little script made by python :)

Enter your source and destination paths, select any desired instruments, and hit Sync. The program will run for a while and filter out any charts without any of the checked instruments. It will copy any valid charts to the destination and give you a confirmation box when complete. This tool only copies files that either don't exist in the destination or have been edited in the source directory.


The program could take quite a while to run, but will show progress.


===To Run===


To run the tool, all you need is ChartSync.exe, which can be found on the [releases page](https://github.com/pythonchcharts/ChartSync/releases/tag/release)


===To Make Changes===


Edit main.py and rebuild using PyInstaller with the following command:


pyinstaller ./ChartSync.spec


Your new exe will be found in dist






