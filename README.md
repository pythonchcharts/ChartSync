A little script made by python :)

Enter your source and destination paths, select any desired instruments, and hit Filter. The program will run for a while and filter out any charts without any of the checked instruments. It will copy any valid charts to the destination and give you a confirmation box when complete.


The program could take quite a while to run. I haven't implemented any sort of progress bar yet, sorry.


===To Run===


To run the tool, all you need is ChartFilter.exe, which can be found on the [releases page](https://github.com/pythonchcharts/ChartFilter/releases)


===To Make Changes===


Edit main.py and rebuild using PyInstaller with the following command:


pyinstaller ./ChartFilter.spec


Your new exe will be found in dist




