import tkinter as tk
from tkinter import messagebox

from vision import plot_data

def fetch_and_plot():
    keyword = entry.get()
    plot_data(keyword)
    success = plot_data(keyword)
    if not success:
        messagebox.showinfo("Information", "Keine Daten gefunden. Bitte versuchen Sie einen anderen Begriff.")

root = tk.Tk()
root.title("Data Visualizer")

root.state('zoomed')

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Compare", command=fetch_and_plot)
button.pack()

root.mainloop()