import csv
import sys
import time
import tkinter as tk
from tkinter import messagebox, Label
import threading

from Data.Trie import Trie
from vision import plot_data

def load_trie(max_titles):
    global trie_loaded
    start_time = time.time()

    try:
        trie_loaded = Trie()
        with open('wiki_titles.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            sys.setrecursionlimit(max_titles *1000000 + 1000)
            for i, row in enumerate(reader):
                if i >= max_titles*1000000:
                    break
                trie_loaded.insert(row[0])
                if i % 10000 == 0:
                    print(i)

        update_label("Trie geladen!")
        update_Lable_label("Geben Sie ein Keyword ein:")
        load_button.config(state="disabled")

    except Exception as e:
        update_label(f"Fehler beim Laden: {e}")

    end_time = time.time()
    duration = end_time - start_time
    print(f"Die Operation hat {duration} Sekunden gedauert.")

def on_listbox_select(event):
    widget = event.widget
    if widget.curselection():
        index = int(widget.curselection()[0])
        value = widget.get(index)
        entry.delete(0, tk.END)
        entry.insert(0, value)

def update_Lable_label(text):
    label.config(text=text)
    label.update()

def update_label(text):
    status_label.config(text=text)
    status_label.update()

def fetch_and_plot():
    keyword = entry.get().strip()
    if not keyword:
        messagebox.showwarning("Warnung", "Bitte geben Sie ein gültiges Keyword ein.")
        return
    success = plot_data(keyword)
    if success == True:
        print("Diagramm geladen!")
    elif success == -1:
        messagebox.showinfo("Information", "Keine Daten gefunden. Bitte versuchen Sie einen anderen Begriff.")
    elif success == -2:
        messagebox.showinfo("Warnung", "Google verweigert wieder den Zugriff auf diesen Begriff! Versuchen Sie einen anderen.")
    else:
        messagebox.showinfo("Warnung", "Hm...Schwierig!")


def autocomplete(event):
    text = entry.get()
    if text == '':
        listbox.delete(0, tk.END)
        return
    matches = [word for word in trie_loaded.search(text)]
    listbox.delete(0, tk.END)
    for match in matches:
        listbox.insert(tk.END, match)

def start_loading():
    max_titles = int(entry_load.get())
    if 1 <= max_titles <= 16:
        update_label("Lade Trie...")
        threading.Thread(target=lambda: load_trie(max_titles), daemon=True).start()
    else:
        messagebox.showwarning("Warnung", "Bitte geben Sie eine Zahl zwischen 1 und 16 ein.")


root = tk.Tk()
root.title("Data Visualizer")
root.state('zoomed')

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(padx=10, pady=10)

status_label = Label(main_frame, text="", font=("Arial", 12))
status_label.pack(pady=(0, 10))

label_load = tk.Label(main_frame, text="Anzahl der zu ladenden Titel (1-16) in Millionen:", font=("Arial", 14))
label_load.pack(pady=(0, 10))

entry_load = tk.Entry(main_frame, font=("Helvetica", 14), width=20, bg="#f0f0f0", fg="black")
entry_load.pack()

load_button = tk.Button(main_frame, text="Laden", command=start_loading)
load_button.pack(pady=(0, 10))

threading.Thread(target=load_trie, daemon=True).start()

label = tk.Label(main_frame, text="", font=("Arial", 14))
label.pack(pady=(0, 10))

entry = tk.Entry(main_frame, font=("Helvetica", 14), width=50, bg="#f0f0f0", fg="black")
entry.pack()

frame_for_listbox = tk.Frame(main_frame, bg="#dddddd", padx=5, pady=5)
frame_for_listbox.pack(padx=5, pady=5)

listbox = tk.Listbox(frame_for_listbox, width=50, bg="#ffffff", fg="black", selectbackground="#a0a0a0", font=("Helvetica", 12))
listbox.pack()

entry.bind('<KeyRelease>', autocomplete)

listbox.bind('<<ListboxSelect>>', lambda event: [on_listbox_select(event), fetch_and_plot()])


root.mainloop()
