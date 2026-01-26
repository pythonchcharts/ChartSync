import sv_ttk
import os
import shutil
import stat
import hashlib
import threading
from tkinter import messagebox, Tk, HORIZONTAL
from tkinter import *
from tkinter import ttk

class FilterApp(Tk):

    def __init__(self):
        super().__init__()

        self.title("ChartSync")

        self.total_charts = 0
        self.processed_charts = 0

        self.mainframe = ttk.Frame(self, padding=(3, 3, 12, 12))
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Label(self.mainframe, text="Local Library:").grid(column=1, row=1, sticky=W)
        self.local_library = StringVar()
        local_entry = ttk.Entry(self.mainframe, width=28, textvariable=self.local_library)
        local_entry.grid(column=2, row=1, columnspan=6, sticky=(W, E))

        ttk.Label(self.mainframe, text="Destination:").grid(column=1, row=2, sticky=W)
        self.destination = StringVar()
        dest_entry = ttk.Entry(self.mainframe, width=28, textvariable=self.destination)
        dest_entry.grid(column=2, row=2, columnspan=6, sticky=(W, E))

        ttk.Label(self.mainframe, text="Filter by instrument:").grid(column=1, row=3, sticky=(W, E))
        ttk.Label(self.mainframe, text="Filter by difficulty:").grid(column=1, row=4, sticky=(W, E))

        # INSTRUMENT CHECKBOXES
        self.lead = BooleanVar()
        lead_check = ttk.Checkbutton(
            self.mainframe, text='Lead', variable=self.lead, onvalue=True, offvalue=False
        )
        lead_check.grid(column=2, row=3, sticky=(W, E))

        self.rhythm = BooleanVar()
        rhythm_check = ttk.Checkbutton(
            self.mainframe, text='Rhythm', variable=self.rhythm, onvalue=True, offvalue=False
        )
        rhythm_check.grid(column=3, row=3, sticky=(W, E))

        self.bass = BooleanVar()
        bass_check = ttk.Checkbutton(
            self.mainframe, text='Bass', variable=self.bass, onvalue=True, offvalue=False
        )
        bass_check.grid(column=4, row=3, sticky=(W, E))

        self.drums = BooleanVar()
        drums_check = ttk.Checkbutton(
            self.mainframe, text='Drums', variable=self.drums, onvalue=True, offvalue=False
        )
        drums_check.grid(column=5, row=3, sticky=(W, E))

        self.sixfret = BooleanVar()
        sixfret_check = ttk.Checkbutton(
            self.mainframe, text='6-Fret', variable=self.sixfret, onvalue=True, offvalue=False
        )
        sixfret_check.grid(column=6, row=3, sticky=(W, E))

        # DIFFICULTY CHECKBOXES
        self.expert = BooleanVar()
        expert_check = ttk.Checkbutton(
            self.mainframe, text='Expert', variable=self.expert, onvalue=True, offvalue=False
        )
        expert_check.grid(column=2, row=4, sticky=(W, E))

        self.hard = BooleanVar()
        hard_check = ttk.Checkbutton(
            self.mainframe, text='Hard', variable=self.hard, onvalue=True, offvalue=False
        )
        hard_check.grid(column=3, row=4, sticky=(W, E))

        self.medium = BooleanVar()
        medium_check = ttk.Checkbutton(
            self.mainframe, text='Medium', variable=self.medium, onvalue=True, offvalue=False
        )
        medium_check.grid(column=4, row=4, sticky=(W, E))

        self.easy = BooleanVar()
        easy_check = ttk.Checkbutton(
            self.mainframe, text='Easy', variable=self.easy, onvalue=True, offvalue=False
        )
        easy_check.grid(column=5, row=4, sticky=(W, E))

        self.exact = BooleanVar()
        exact_check = ttk.Checkbutton(
            self.mainframe, text='Exact?', variable=self.exact, onvalue=True, offvalue=False
        )
        exact_check.grid(column=6, row=4, sticky=(W, E))

        # ADDITIONAL CHECKBOXES
        ttk.Label(
            self.mainframe,
            text="Note: .mid charts cannot be filtered by difficulty, so they may not match the specified difficulties.\n" +
            ".mid charts will be filtered out by default unless this box is checked."
        ).grid(column=1, row=5, columnspan=10, sticky=(W, E))
        self.include_mid = BooleanVar()
        mid_check = ttk.Checkbutton(
            self.mainframe, text='Include .mid?', variable=self.include_mid, onvalue=True, offvalue=False
        )
        mid_check.grid(column=2, row=6, sticky=(W, E))

        sync_button = ttk.Button(self.mainframe, text="Sync", command=lambda:threading.Thread(target=self.show_confirmation).start())
        sync_button.grid(column=3, row=7, sticky=(W, E))

        self.prog_label = ttk.Label(self.mainframe, text="")
        self.prog_label.grid(column=1, row=8, sticky=(W, E))

        self.chart_name_label = ttk.Label(self.mainframe, text="", wraplength=500)
        self.chart_name_label.grid(column=1, row=9, columnspan=10, sticky=(W, E))

        self.resizable(width=False, height=False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(2, weight=0)
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        local_entry.focus()
        self.bind("<Return>", self.filter_and_sync)

        sv_ttk.set_theme("dark")

    def filter_and_sync(self):
        total_files = 0
        total_files_copied = 0
        charts_copied = 0
        rootdir = self.local_library.get()
        destdir = self.destination.get()

        # count all chart dirs
        chart_dirs = []
        for root, dirs, files in os.walk(rootdir):
            if files and not dirs:
                chart_dirs.append(root)
                total_files += len(files)
        total_charts = len(chart_dirs)
        print('Total charts detected: ' + str(total_charts))

        for path, dirs, files in os.walk(rootdir):
            for file in files:
                copy_chart = False
                filename, ext = os.path.splitext(file)
                if ext == '.chart':
                    self.chart_name_label.configure(text=f"Current Chart: {path + '\\' + file}")
                    lead_flags = rhythm_flags = bass_flags = drums_flags = sixfret_flags = [False] * 4
                    with open(path + '\\' + file, encoding="latin-1") as lines:
                        # Search the .chart file for any notes on the given highway
                        for line in lines:
                            if 'Single' in line:
                                if 'Expert' in line:
                                    lead_flags[0] = True
                                if 'Hard' in line:
                                    lead_flags[1] = True
                                if 'Medium' in line:
                                    lead_flags[2] = True
                                if 'Easy' in line:
                                    lead_flags[3] = True
                            if 'DoubleRhythm' in line:
                                if 'Expert' in line:
                                    rhythm_flags[0] = True
                                if 'Hard' in line:
                                    rhythm_flags[1] = True
                                if 'Medium' in line:
                                    rhythm_flags[2] = True
                                if 'Easy' in line:
                                    rhythm_flags[3] = True
                            if 'DoubleBass' in line:
                                if 'Expert' in line:
                                    bass_flags[0] = True
                                if 'Hard' in line:
                                    bass_flags[1] = True
                                if 'Medium' in line:
                                    bass_flags[2] = True
                                if 'Easy' in line:
                                    bass_flags[3] = True
                            if 'Drums' in line:
                                if 'Expert' in line:
                                    drums_flags[0] = True
                                if 'Hard' in line:
                                    drums_flags[1] = True
                                if 'Medium' in line:
                                    drums_flags[2] = True
                                if 'Easy' in line:
                                    drums_flags[3] = True
                            if 'GHLGuitar' in line:
                                if 'Expert' in line:
                                    sixfret_flags[0] = True
                                if 'Hard' in line:
                                    sixfret_flags[1] = True
                                if 'Medium' in line:
                                    sixfret_flags[2] = True
                                if 'Easy' in line:
                                    sixfret_flags[3] = True
                        lines.close()
                    user_params = [self.expert.get(), self.hard.get(), self.medium.get(), self.easy.get()]
                    if self.lead.get() and \
                            ((self.exact.get() and lead_flags == user_params) or \
                            (not self.exact.get() and any((item1 and item2) for item1, item2 in zip(lead_flags, user_params)))):
                        copy_chart = True
                    elif self.rhythm.get() and \
                            ((self.exact.get() and rhythm_flags == user_params) or \
                            (not self.exact.get() and any((item1 and item2) for item1, item2 in zip(rhythm_flags, user_params)))):
                        copy_chart = True
                    elif self.bass.get() and \
                            ((self.exact.get() and bass_flags == user_params) or \
                            (not self.exact.get() and any((item1 and item2) for item1, item2 in zip(bass_flags, user_params)))):
                        copy_chart = True
                    elif self.drums.get() and \
                            ((self.exact.get() and drums_flags == user_params) or \
                            (not self.exact.get() and any((item1 and item2) for item1, item2 in zip(drums_flags, user_params)))):
                        copy_chart = True
                    elif self.sixfret.get() and \
                            ((self.exact.get() and sixfret_flags == user_params) or \
                            (not self.exact.get() and any((item1 and item2) for item1, item2 in zip(sixfret_flags, user_params)))):
                        copy_chart = True

                # .mid has no difficulty indicators in its text, so difficulty cannot be discerned
                # The user must explicitly indicate to include .mid files.
                if ext == '.mid' and self.include_mid.get():
                    self.chart_name_label.configure(text=f"Current Chart: {path + '\\' + file}")
                    with open(path + '\\' + file, encoding="latin-1") as lines:
                        # Search the .mid file for any notes on the given highway
                        for line in lines:
                            if 'PART GUITAR' in line and 'PART GUITAR GHL' not in line and self.lead.get():
                                copy_chart = True
                            elif 'PART RHYTHM' in line and self.rhythm.get():
                                copy_chart = True
                            elif 'PART BASS' in line and self.bass.get():
                                copy_chart = True
                            elif 'PART DRUMS' in line and self.drums.get():
                                copy_chart = True
                            elif 'PART GUITAR GHL' in line and self.sixfret.get():
                                copy_chart = True
                        lines.close()

                if copy_chart:
                    copy_chart = False
                    charts_copied += 1
                    for file in files:
                        full_path_root = path + '\\' + file
                        path_suffix = path.replace(rootdir, "")
                        dest_path = destdir + path_suffix
                        full_path_dest = dest_path + '\\' + file
                        if os.path.exists(full_path_dest):
                            if self.file_hash(full_path_root) != self.file_hash(full_path_dest):
                                shutil.copy(full_path_root, dest_path)
                                total_files_copied += 1
                            else:
                                print(full_path_root + " is identical to the file at destination, not copying")
                        else:
                            os.makedirs(dest_path, exist_ok=True)
                            shutil.copy(full_path_root, dest_path)
                            total_files_copied += 1
                    self.prog_label.configure(text=f"Charts copied: {charts_copied}/{total_charts}")
        print("Total Files Copied: " + str(total_files_copied))

        self.prog_label.configure(text="Cleaning up destination folder...")
        total_files_deleted = 0
        # First clean up files
        for path, dirs, files in os.walk(destdir):
            for file in files:
                full_path_dest = path + '\\' + file
                path_suffix = path.replace(destdir, "")
                root_path = rootdir + path_suffix
                full_path_root = root_path + '\\' + file
                if not os.path.exists(full_path_root) and os.path.exists(full_path_dest):
                    os.remove(full_path_dest)
                    total_files_deleted += 1
        print("Total files deleted: " + str(total_files_deleted))
        # Then clean up dirs
        for path, _, _ in os.walk(destdir):
            try:
                os.rmdir(path)
            except OSError:
                pass
        self.prog_label.configure(text=f"Complete! Charts processed: {total_files_copied}, Files Deleted: {total_files_deleted}")
        self.chart_name_label.configure(text="")

    def file_hash(self, filepath):
        """Calculates the SHA-256 hash of a file."""
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            # Read the file in chunks to be memory-efficient
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
            f.close()
        return hasher.hexdigest()

    def show_confirmation(self):
        result = messagebox.askyesno("Confirm Action", "Are you sure you want to proceed?")
        if result:
            all_instruments = [self.lead.get(), self.rhythm.get(), self.bass.get(), self.drums.get(), self.sixfret.get()]
            all_diffs = [self.expert.get(), self.hard.get(), self.medium.get(), self.easy.get()]
            if not any(all_instruments):
                messagebox.showinfo("Error!", "No instrument filters selected.")
                return
            if not any(all_diffs):
                messagebox.showinfo(
                    "Error!", "No difficulty filters selected.\n" +
                    "For syncing .mid charts, select any difficulty."
                )
                return
            self.filter_and_sync()
            messagebox.showinfo("Success!", "Charts processed succesfully.")


if __name__ == '__main__':
    root = FilterApp()
    root.mainloop()