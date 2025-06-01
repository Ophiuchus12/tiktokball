import tkinter as tk
from tkinter import filedialog, colorchooser
import json
import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def choisir_couleur(entry):
    couleur = colorchooser.askcolor()[0]
    if couleur:
        entry.delete(0, tk.END)
        entry.insert(0, str(tuple(map(int, couleur))))

def choisir_image(entry):
    fichier = filedialog.askopenfilename(filetypes=[("Images", "*.png")])
    if fichier:
        entry.delete(0, tk.END)
        entry.insert(0, fichier)

def on_theme_change(event):
    if cerclesTheme.get() == "unicolor":
        label_cercles_color.pack()
        cerclesColor_entry.pack()
        bouton_couleur_cercles.pack()
    else:
        label_cercles_color.pack_forget()
        cerclesColor_entry.pack_forget()
        bouton_couleur_cercles.pack_forget()

def lancer_jeu():
    config = {
        "color1": eval(couleur1_entry.get()),
        "color2": eval(couleur2_entry.get()),
        "logo1": logo1_entry.get(),
        "logo2": logo2_entry.get(),
        "cerclesTheme": cerclesTheme.get(),
        "cerclesColor": eval(cerclesColor_entry.get()) if cerclesTheme.get() == "unicolor" else None,
        "timer": int(timer_entry.get()),
        "modeJeu": modeJeu_combo.get()
    }
    with open("config.json", "w") as f:
        json.dump(config, f)
    subprocess.run(["python3", "jeu.py"])

# Fenêtre
fenetre = ttk.Window(themename="cosmo")
fenetre.title("Paramètres du jeu")
fenetre.geometry("400x700")

# Couleur balle 1
ttk.Label(fenetre, text="Couleur balle 1 :").pack()
couleur1_entry = ttk.Entry(fenetre)
couleur1_entry.pack()
ttk.Button(fenetre, text="Choisir", command=lambda: choisir_couleur(couleur1_entry)).pack()

# Couleur balle 2
ttk.Label(fenetre, text="Couleur balle 2 :").pack()
couleur2_entry = ttk.Entry(fenetre)
couleur2_entry.pack()
ttk.Button(fenetre, text="Choisir", command=lambda: choisir_couleur(couleur2_entry)).pack()

# Logo balle 1
ttk.Label(fenetre, text="Logo balle 1 :").pack()
logo1_entry = ttk.Entry(fenetre)
logo1_entry.pack()
ttk.Button(fenetre, text="Parcourir", command=lambda: choisir_image(logo1_entry)).pack()

# Logo balle 2
ttk.Label(fenetre, text="Logo balle 2 :").pack()
logo2_entry = ttk.Entry(fenetre)
logo2_entry.pack()
ttk.Button(fenetre, text="Parcourir", command=lambda: choisir_image(logo2_entry)).pack()

# Thème des cercles + Couleur (groupe dans un Frame)
cercles_frame = ttk.Frame(fenetre)
cercles_frame.pack(pady=10, fill="x")

ttk.Label(cercles_frame, text="Thème des cercles :").pack()
cerclesTheme = ttk.Combobox(cercles_frame, values=["unicolor", "multicolor"], state="readonly")
cerclesTheme.pack()

label_cercles_color = ttk.Label(cercles_frame, text="Couleur des cercles :")
cerclesColor_entry = ttk.Entry(cercles_frame)
bouton_couleur_cercles = ttk.Button(cercles_frame, text="Choisir", command=lambda: choisir_couleur(cerclesColor_entry))
cerclesTheme.bind("<<ComboboxSelected>>", on_theme_change)

# Timer
ttk.Label(fenetre, text="Durée du timer (sec) :").pack()
timer_entry = ttk.Entry(fenetre)
timer_entry.insert(0, "60")
timer_entry.pack()

# Mode de jeu
ttk.Label(fenetre, text="Mode de jeu :").pack(pady=10)
modeJeu_combo = ttk.Combobox(fenetre, values=["Classique", "Multicolore", "Double Balle", "Challenge Timer"], state="readonly")
modeJeu_combo.pack()

# Lancer
ttk.Button(fenetre, text="Lancer le jeu", command=lancer_jeu, bootstyle="success").pack(pady=20)

fenetre.mainloop()
