# ChartSync

A little script made by python :)

Enter your source and destination paths, select any desired instruments and difficulties, and hit Sync. The program will begin copying any qualifying charts to the destination directory, mirroring the directory structure present in the source, and excluding any charts that do not meet the filters set by the user.


## How to Run


To run the tool, all you need is ChartSync.exe, which can be found on the [releases page](https://github.com/pythonchcharts/ChartSync/releases)

The instrument filters are non-exact, any chart with any of the selected instruments will be copied to the new library. The difficulty filters can be exact by enabling the "Exact?" flag, but otherwise are not and behave the same as instruments. Here is an example of a filter that will search only for full difficulty charts:

<img width="631" height="369" alt="image" src="https://github.com/user-attachments/assets/dd103f2d-bc85-4a88-88cd-fadcf06db7b7" />

For a less restrictive filter, here is an example of a filter that searches for any charts with drums and an expert chart, without caring what else the charts have:

<img width="630" height="371" alt="image" src="https://github.com/user-attachments/assets/59b26a82-51da-483c-99f4-d5e563c21963" />

As noted on the UI, .mid files cannot be filtered by difficulty. This is because the program reads the file as text and .mid does not have any discernable way to determine what difficulties are available on the chart in text format. You must select at least one difficulty for the program to run but it will have no effect on .mid charts. If you want to include .mid charts in your output anyway, check the "Include .mid" option.



## To Make Changes to the Source


Edit main.py and rebuild using PyInstaller with the following command:


pyinstaller ./ChartSync.spec


Your new exe will be found in dist


## Planned Features

- Destination cleanup: removing files in the destination directory that do not exist in the source. This means deleted charts in the source will also be deleted on the next sync.
- Exact modifier for instruments: Instruments should also have an exact modifier like difficulty does so that they behave the same way







