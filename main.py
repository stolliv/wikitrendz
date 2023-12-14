import tkinter as tk
from tkinter import messagebox, Label
import pickle
import threading
from vision import plot_data

def load_trie():
    global trie_loaded
    try:
        with open('Data/trie_data.pkl', 'rb') as input:
            trie_loaded = pickle.load(input)
        update_label("Trie geladen!")
    except Exception as e:
        update_label(f"Fehler beim Laden: {e}")

def on_listbox_select(event):
    widget = event.widget
    if widget.curselection():
        index = int(widget.curselection()[0])
        value = widget.get(index)
        entry.delete(0, tk.END)
        entry.insert(0, value)

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


# Auto-Vervollständigungsfunktion
def autocomplete(event):
    text = entry.get()
    if text == '':
        listbox.delete(0, tk.END)
        return
    matches = [word for word in trie_loaded.search(text)]
    listbox.delete(0, tk.END)
    for match in matches:
        listbox.insert(tk.END, match)

# Initialisieren des Tkinter-Fensters
root = tk.Tk()
root.title("Data Visualizer")
root.state('zoomed')

# Haupt-Frame
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(padx=10, pady=10)

# Status-Label für Ladeanzeige
status_label = Label(main_frame, text="Lade Trie...", font=("Arial", 12))
status_label.pack(pady=(0, 10))

# Starten des Ladevorgangs in einem separaten Thread
threading.Thread(target=load_trie, daemon=True).start()
# Beschriftung
label = tk.Label(main_frame, text="Geben Sie ein Keyword ein:", font=("Arial", 14))
label.pack(pady=(0, 10))

# Eingabefeld und Listbox
entry = tk.Entry(main_frame, font=("Helvetica", 14), width=50, bg="#f0f0f0", fg="black")
entry.pack()

frame_for_listbox = tk.Frame(main_frame, bg="#dddddd", padx=5, pady=5)
frame_for_listbox.pack(padx=5, pady=5)

listbox = tk.Listbox(frame_for_listbox, width=50, bg="#ffffff", fg="black", selectbackground="#a0a0a0", font=("Helvetica", 12))
listbox.pack()

# Event-Bindung für Auto-Vervollständigung
entry.bind('<KeyRelease>', autocomplete)

# Bindung der Listbox-Selektion an die on_listbox_select Funktion
listbox.bind('<<ListboxSelect>>', lambda event: [on_listbox_select(event), fetch_and_plot()])


# Tkinter-Schleife starten
root.mainloop()
