import tkinter as tk
from tkinter import filedialog, colorchooser
import json
import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

balle_params_list = []


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
    theme = cerclesTheme.get()
    
    if theme == "triple":
        modeJeu_combo.set("tripleCercle")
        modeJeu_combo.config(state="disabled")
        ajouter_balle_btn.config(state="disabled")
    else:
        modeJeu_combo.config(state="readonly")
        ajouter_balle_btn.config(state="normal")

    # Affichage/masquage couleur cercle selon thème
    if theme not in ["multicolor", "cageCercle", "cageCercle4"]:
        label_cercles_color.pack()
        cerclesColor_entry.pack()
        bouton_couleur_cercles.pack()
    else:
        label_cercles_color.pack_forget()
        cerclesColor_entry.pack_forget()
        bouton_couleur_cercles.pack_forget()



def ouvrir_modal_balle(parent):
    modal = tk.Toplevel(parent)
    modal.title("Configurer une balle")
    modal.geometry("300x300")
    modal.grab_set()

    ttk.Label(modal, text="Rayon :").pack()
    rayon_entry = ttk.Entry(modal)
    rayon_entry.pack()

    ttk.Label(modal, text="Couleur :").pack()
    couleur_entry = ttk.Entry(modal)
    couleur_entry.pack()
    ttk.Button(modal, text="Choisir la couleur Interieur", command=lambda: choisir_couleur(couleur_entry)).pack(pady=10)

    ttk.Label(modal, text="Couleur2 :").pack()
    couleur_entry2 = ttk.Entry(modal)
    couleur_entry2.pack()
    ttk.Button(modal, text="Choisir la couleur du bord", command=lambda: choisir_couleur(couleur_entry2)).pack(pady=10)


    ttk.Label(modal, text="Logo :").pack()
    logo_entry = ttk.Entry(modal)
    logo_entry.pack()
    ttk.Button(modal, text="Parcourir", command=lambda: choisir_image(logo_entry)).pack(pady=10)

    
    ttk.Button(modal, text="Ajouter", command=lambda: valider()).pack(pady=10)

    def valider():
        params = {
            "radius": int(rayon_entry.get()) if rayon_entry.get() else 60,
            "colorIn": eval(couleur_entry.get()) if couleur_entry.get() else (255,255,255),
            "colorBord": eval(couleur_entry2.get()) if couleur_entry2.get() else (255,255,255),
            "logo": logo_entry.get() or None
        }
        balle_params_list.append(params)

        # Affichage dans la liste
        info_balle = f"Balle {len(balle_params_list)} - Rayon {params['radius']} - Couleur {params['colorIn']}"
        liste_balles.insert(tk.END, info_balle)

        modal.grab_release()
        modal.destroy()


def lancer_jeu():
    if cerclesTheme.get() != "triple" and len(balle_params_list) == 0:
        tk.messagebox.showwarning("Avertissement", "Veuillez ajouter au moins une balle.")
        return
    config = {
        "cerclesTheme": cerclesTheme.get(),
        "cerclesColor": eval(cerclesColor_entry.get()) if cerclesTheme.get() == "unicolor" else None,
        "timer": int(timer_entry.get()),
        "modeJeu": modeJeu_combo.get(),
        "balles_custom": balle_params_list  # Liste des balles ajoutées
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f)
    subprocess.run(["python3", "jeu.py"])

# Fenêtre
fenetre = ttk.Window(themename="cosmo")
fenetre.title("Paramètres du jeu")
fenetre.geometry("400x700")


# Thème des cercles + Couleur (groupe dans un Frame)
cercles_frame = ttk.Frame(fenetre)
cercles_frame.pack(pady=10, fill="x")

ttk.Label(cercles_frame, text="Thème des cercles :").pack()
cerclesTheme = ttk.Combobox(cercles_frame, values=["unicolor", "multicolor", "simpleCercle", "simpleCercleferme", "cageCercle", "cageCercle4", "triple"], state="readonly")
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
modeJeu_combo = ttk.Combobox(fenetre, values=["classique", "simpleCercleferme", "rebondInfini", "simpleCercle", "cageCercle", "tripleCercle"], state="readonly")
modeJeu_combo.pack()

#create Ball
ajouter_balle_btn = ttk.Button(fenetre, text="Ajouter une balle personnalisée", command=lambda: ouvrir_modal_balle(fenetre))
ajouter_balle_btn.pack(pady=10)

#Liste des balles add
ttk.Label(fenetre, text="Balles ajoutées :").pack()
liste_balles = tk.Listbox(fenetre, height=5)
liste_balles.pack(fill="x", padx=10, pady=5)

# Lancer
ttk.Button(fenetre, text="Lancer le jeu", command=lancer_jeu, bootstyle="success").pack(pady=20)

fenetre.mainloop()
