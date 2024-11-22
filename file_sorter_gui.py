import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox


def file_sorter(path, folder_names, file_types, keywords, status_label):
    try:
        file_names = os.listdir(path)

        # Create folders if they don't exist
        for folder in folder_names:
            if folder:
                folder_path = os.path.join(path, folder)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

        # Move files and folders into corresponding folders
        for file in file_names:
            src = os.path.join(path, file)

            # Move directories
            if os.path.isdir(src):
                for folder, keyword in zip(folder_names, keywords):
                    if folder and keyword and keyword.lower() in file.lower():
                        dst = os.path.join(path, folder, file)
                        if os.path.exists(dst):
                            shutil.rmtree(dst)  # Remove existing folder if it conflicts
                        shutil.move(src, dst)
                        break
                continue

            # Move files based on extension or keyword match
            for ext, folder, keyword in zip(file_types, folder_names, keywords):
                if not folder or (not ext and not keyword):
                    continue
                if (ext and file.lower().endswith(ext)) or (keyword and keyword.lower() in file.lower()):
                    dst = os.path.join(path, folder, file)
                    if os.path.exists(dst):
                        os.remove(dst)
                    shutil.move(src, dst)
                    break

        status_label.config(text="Sorting completed.")
    except Exception as e:
        status_label.config(text=f"Error: {e}")


def start_sorting():
    global running
    running = True

    path = path_entry.get()
    if not os.path.exists(path):
        messagebox.showerror("Error", "Invalid path provided.")
        return

    folder_names = [entry.get() for entry in folder_entries]
    file_types = [entry.get() for entry in file_type_entries]
    keywords = [entry.get() for entry in keyword_entries]

    if not any(folder_names):
        messagebox.showerror("Error", "At least one folder name is required.")
        return

    def run_sorting_cycle():
        if not running:
            return
        file_sorter(path, folder_names, file_types, keywords, status_label)
        countdown(30)

    def countdown(seconds):
        if not running:
            return
        if seconds > 0:
            countdown_label.config(text=f"Next run in {seconds} seconds...")
            root.after(1000, countdown, seconds - 1)  # Update countdown every second
        else:
            run_sorting_cycle()  # Restart sorting cycle after countdown

    status_label.config(text="Sorting started...")
    run_sorting_cycle()


def stop_sorting():
    global running
    running = False
    status_label.config(text="Sorting stopped.")
    countdown_label.config(text="Sorting halted.")
    root.after_cancel(root.after_id)


# Tkinter GUI Setup
root = tk.Tk()
root.title("File Sorter App")
root.geometry("500x700")

# Main Frame with Scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Path Entry
path_label = tk.Label(scrollable_frame, text="Enter the path to sort:")
path_label.pack(pady=5)
path_entry = tk.Entry(scrollable_frame, width=40)
path_entry.pack(pady=5)

# Folder, file type, and keyword entries
folder_entries = []
file_type_entries = []
keyword_entries = []

for i in range(5):
    folder_label = tk.Label(scrollable_frame, text=f"Folder {i+1} Name:")
    folder_label.pack(pady=5)
    folder_entry = tk.Entry(scrollable_frame, width=40)
    folder_entry.pack(pady=5)
    folder_entries.append(folder_entry)

    file_type_label = tk.Label(scrollable_frame, text=f"File Type {i+1} (e.g., .pdf):")
    file_type_label.pack(pady=5)
    file_type_entry = tk.Entry(scrollable_frame, width=40)
    file_type_entry.pack(pady=5)
    file_type_entries.append(file_type_entry)

    keyword_label = tk.Label(scrollable_frame, text=f"Keyword {i+1}:")
    keyword_label.pack(pady=5)
    keyword_entry = tk.Entry(scrollable_frame, width=40)
    keyword_entry.pack(pady=5)
    keyword_entries.append(keyword_entry)

# Buttons
start_button = tk.Button(scrollable_frame, text="Start Sorting", command=start_sorting)
start_button.pack(pady=10)

stop_button = tk.Button(scrollable_frame, text="Stop Sorting", command=stop_sorting)
stop_button.pack(pady=10)

# Status Labels
status_label = tk.Label(scrollable_frame, text="Status: Ready")
status_label.pack(pady=10)

countdown_label = tk.Label(scrollable_frame, text="")
countdown_label.pack(pady=10)

running = False  # Global flag to manage sorting cycle
root.mainloop()






# path name: /Users/dejwilli/Downloads













