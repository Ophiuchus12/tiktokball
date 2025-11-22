"""
Game launcher with GUI for configuring game settings.
Uses tkinter/ttkbootstrap for the interface.
"""

import sys
from pathlib import Path

# Ajoute sourceCode/ au PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))


import sys
from pathlib import Path

# Ajoute sourceCode/ au PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import subprocess
import ast
import os

try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    HAS_TTKBOOTSTRAP = True
except ImportError:
    import tkinter.ttk as ttk
    HAS_TTKBOOTSTRAP = False
    print("Warning: ttkbootstrap not installed, using standard tkinter")

from config.config_manager import ConfigManager
from config.constants import DEFAULT_TIMER, DEFAULT_MIN_RADIUS


class GameLauncher:
    """Main launcher window for game configuration."""
    
    def __init__(self):
        """Initialize the launcher window."""
        self.config = ConfigManager()
        self.balle_params_list = []
        self.balleOptionAvanced = {}
        
        # Create main window
        if HAS_TTKBOOTSTRAP:
            self.root = ttk.Window(themename="cosmo")
        else:
            self.root = tk.Tk()
        
        self.root.title("TikTok Ball Game - Launcher")
        self.root.geometry("500x850")
        
        self._create_widgets()
        self._load_existing_config()
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Title
        title_label = ttk.Label(
            self.root, 
            text="🎮 TikTok Ball Game Configuration",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Background selection
        self._create_background_section()
        
        # Circle theme selection
        self._create_circle_theme_section()
        
        # Timer duration
        self._create_timer_section()
        
        # Game mode selection
        self._create_game_mode_section()
        
        # Min radius (conditional)
        self._create_min_radius_section()
        
        # Ball configuration
        self._create_ball_section()
        
        # Launch button
        self._create_launch_button()
    
    def _create_background_section(self):
        """Create background image selection widgets."""
        frame = ttk.LabelFrame(self.root, text="Background Image", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        self.bg_entry = ttk.Entry(frame, width=40)
        self.bg_entry.pack(side="left", padx=5)
        
        browse_btn = ttk.Button(
            frame, 
            text="Browse", 
            command=lambda: self._choose_image(self.bg_entry)
        )
        browse_btn.pack(side="left", padx=5)
    
    def _create_circle_theme_section(self):
        """Create circle theme selection widgets."""
        frame = ttk.LabelFrame(self.root, text="Circle Theme", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame, text="Theme:").pack(anchor="w")
        self.cerclesTheme = ttk.Combobox(
            frame,
            values=[
                "unicolor", "multicolor", "simpleCercle", 
                "simpleCercleferme", "cageCercle", "cageCercle4", "triple"
            ],
            state="readonly",
            width=37
        )
        self.cerclesTheme.pack(fill="x", pady=5)
        self.cerclesTheme.bind("<<ComboboxSelected>>", self._on_theme_change)
        
        # Color selection (shown conditionally)
        self.color_frame = ttk.Frame(frame)
        self.color_frame.pack(fill="x", pady=5)
        
        ttk.Label(self.color_frame, text="Color:").pack(side="left")
        self.cerclesColor_entry = ttk.Entry(self.color_frame, width=20)
        self.cerclesColor_entry.pack(side="left", padx=5)
        
        self.bouton_couleur_cercles = ttk.Button(
            self.color_frame,
            text="Choose Color",
            command=lambda: self._choose_color(self.cerclesColor_entry)
        )
        self.bouton_couleur_cercles.pack(side="left", padx=5)
    
    def _create_timer_section(self):
        """Create timer duration widgets."""
        frame = ttk.LabelFrame(self.root, text="Game Timer", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame, text="Duration (seconds):").pack(side="left")
        self.timer_entry = ttk.Entry(frame, width=10)
        self.timer_entry.insert(0, str(DEFAULT_TIMER))
        self.timer_entry.pack(side="left", padx=5)
    
    def _create_game_mode_section(self):
        """Create game mode selection widgets."""
        frame = ttk.LabelFrame(self.root, text="Game Mode", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        self.modeJeu_combo = ttk.Combobox(
            frame,
            values=[
                "classique", "simpleCercleferme", "rebondInfini",
                "simpleCercle", "cageCercle", "tripleCercle"
            ],
            state="readonly",
            width=37
        )
        self.modeJeu_combo.pack(fill="x", pady=5)
        self.modeJeu_combo.bind("<<ComboboxSelected>>", self._on_mode_jeu_change)
    
    def _create_min_radius_section(self):
        """Create minimum radius configuration (conditional)."""
        self.min_radius_frame = ttk.LabelFrame(
            self.root, 
            text="Circle Settings", 
            padding=10
        )
        
        ttk.Label(self.min_radius_frame, text="Minimum Radius:").pack(side="left")
        self.min_radius_entry = ttk.Entry(self.min_radius_frame, width=10)
        self.min_radius_entry.insert(0, str(DEFAULT_MIN_RADIUS))
        self.min_radius_entry.pack(side="left", padx=5)
    
    def _create_ball_section(self):
        """Create ball configuration widgets."""
        frame = ttk.LabelFrame(self.root, text="Ball Configuration", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        # Add ball button
        self.ajouter_balle_btn = ttk.Button(
            frame,
            text="➕ Add Custom Ball",
            command=self._open_ball_modal
        )
        if HAS_TTKBOOTSTRAP:
            self.ajouter_balle_btn.config(bootstyle="info")
        self.ajouter_balle_btn.pack(pady=5)
        
        # Advanced options button
        advanced_btn = ttk.Button(
            frame,
            text="⚙️ Advanced Ball Options",
            command=self._open_advanced_options_modal
        )
        if HAS_TTKBOOTSTRAP:
            advanced_btn.config(bootstyle="secondary")
        advanced_btn.pack(pady=5)
        
        # Ball list
        ttk.Label(frame, text="Configured Balls:").pack(anchor="w", pady=(10, 0))
        self.liste_balles = tk.Listbox(frame, height=5)
        self.liste_balles.pack(fill="x", pady=5)
        
        # Remove ball button
        remove_btn = ttk.Button(
            frame,
            text="❌ Remove Selected Ball",
            command=self._remove_selected_ball
        )
        if HAS_TTKBOOTSTRAP:
            remove_btn.config(bootstyle="danger")
        remove_btn.pack(pady=5)
    
    def _create_launch_button(self):
        """Create launch game button."""
        launch_btn = ttk.Button(
            self.root,
            text="🚀 Launch Game",
            command=self._launch_game
        )
        if HAS_TTKBOOTSTRAP:
            launch_btn.config(bootstyle="success")
        launch_btn.pack(pady=20)
    
    def _choose_color(self, entry):
        """Open color chooser dialog."""
        color = colorchooser.askcolor()[0]
        if color:
            entry.delete(0, tk.END)
            entry.insert(0, str(tuple(map(int, color))))
    
    def _choose_image(self, entry):
        """Open file chooser for images."""
        fichier = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.JPG *.JPEG")]
        )
        if fichier:
            entry.delete(0, tk.END)
            entry.insert(0, fichier)
    
    def _on_theme_change(self, event=None):
        """Handle circle theme change."""
        theme = self.cerclesTheme.get()
        
        # Update game mode based on theme
        if theme == "triple":
            self.modeJeu_combo.set("tripleCercle")
            self.modeJeu_combo.config(state="disabled")
            self.ajouter_balle_btn.config(state="disabled")
        else:
            self.modeJeu_combo.config(state="readonly")
            self.ajouter_balle_btn.config(state="normal")
        
        # Show/hide color selection
        if theme in ["multicolor", "cageCercle", "cageCercle4", "triple"]:
            self.color_frame.pack_forget()
        else:
            self.color_frame.pack(fill="x", pady=5)
    
    def _on_mode_jeu_change(self, event=None):
        """Handle game mode change."""
        mode = self.modeJeu_combo.get()
        
        # Show/hide min_radius based on mode
        if mode == "classique":
            self.min_radius_frame.pack(fill="x", padx=10, pady=5)
        else:
            self.min_radius_frame.pack_forget()
    
    def _open_ball_modal(self):
        """Open modal for configuring a ball."""
        modal = tk.Toplevel(self.root)
        modal.title("Configure Ball")
        modal.geometry("350x450")
        modal.grab_set()
        
        # Radius
        ttk.Label(modal, text="Radius:").pack(pady=(10, 0))
        rayon_entry = ttk.Entry(modal)
        rayon_entry.insert(0, "20")
        rayon_entry.pack(pady=5)
        
        # Inner color
        ttk.Label(modal, text="Inner Color:").pack(pady=(10, 0))
        couleur_entry = ttk.Entry(modal)
        couleur_entry.pack(pady=5)
        ttk.Button(
            modal,
            text="Choose Inner Color",
            command=lambda: self._choose_color(couleur_entry)
        ).pack(pady=5)
        
        # Border color
        ttk.Label(modal, text="Border Color:").pack(pady=(10, 0))
        couleur_entry2 = ttk.Entry(modal)
        couleur_entry2.pack(pady=5)
        ttk.Button(
            modal,
            text="Choose Border Color",
            command=lambda: self._choose_color(couleur_entry2)
        ).pack(pady=5)
        
        # Logo
        ttk.Label(modal, text="Logo (optional):").pack(pady=(10, 0))
        logo_entry = ttk.Entry(modal)
        logo_entry.pack(pady=5)
        ttk.Button(
            modal,
            text="Browse Logo",
            command=lambda: self._choose_image(logo_entry)
        ).pack(pady=5)
        
        # Add button
        def validate_ball():
            try:
                radius = int(rayon_entry.get()) if rayon_entry.get() else 20
            except ValueError:
                messagebox.showerror("Error", "Radius must be a number")
                return
            
            try:
                colorIn = eval(couleur_entry.get()) if couleur_entry.get() else (255, 255, 255)
                colorBord = eval(couleur_entry2.get()) if couleur_entry2.get() else (255, 255, 255)
            except:
                messagebox.showerror("Error", "Colors must be in format (R, G, B)")
                return
            
            params = {
                "radius": radius,
                "colorIn": colorIn,
                "colorBord": colorBord,
                "logo": logo_entry.get() or None
            }
            self.balle_params_list.append(params)
            
            info_balle = f"Ball {len(self.balle_params_list)} - Radius: {params['radius']}"
            self.liste_balles.insert(tk.END, info_balle)
            
            modal.grab_release()
            modal.destroy()
        
        add_btn = ttk.Button(modal, text="Add Ball", command=validate_ball)
        if HAS_TTKBOOTSTRAP:
            add_btn.config(bootstyle="success")
        add_btn.pack(pady=20)
    
    def _open_advanced_options_modal(self):
        """Open modal for advanced ball options."""
        modal = tk.Toplevel(self.root)
        modal.title("Advanced Ball Options")
        modal.geometry("350x300")
        modal.grab_set()
        
        # Mode selection
        ttk.Label(modal, text="Visual Mode:").pack(pady=(20, 5))
        mode_choice = ttk.Combobox(
            modal,
            values=["none", "invisible", "trainee", "trace"],
            state="readonly"
        )
        mode_choice.set("none")
        mode_choice.pack(pady=5)
        
        # OnBounce selection
        ttk.Label(modal, text="Bounce Effect:").pack(pady=(20, 5))
        onBounce_choice = ttk.Combobox(
            modal,
            values=["none", "linked", "cage"],
            state="readonly"
        )
        onBounce_choice.set("none")
        onBounce_choice.pack(pady=5)
        
        def validate_options():
            self.balleOptionAvanced = {
                "mode": mode_choice.get(),
                "onBounce": onBounce_choice.get(),
            }
            
            # Update list with new info
            info_option = f"✨ Effects: {self.balleOptionAvanced['mode']} / {self.balleOptionAvanced['onBounce']}"
            # Remove old effects info if exists
            for i in range(self.liste_balles.size()):
                if self.liste_balles.get(i).startswith("✨"):
                    self.liste_balles.delete(i)
                    break
            self.liste_balles.insert(tk.END, info_option)
            
            modal.grab_release()
            modal.destroy()
        
        save_btn = ttk.Button(modal, text="Save Options", command=validate_options)
        if HAS_TTKBOOTSTRAP:
            save_btn.config(bootstyle="primary")
        save_btn.pack(pady=30)
    
    def _remove_selected_ball(self):
        """Remove selected ball from list."""
        selection = self.liste_balles.curselection()
        if selection:
            index = selection[0]
            item_text = self.liste_balles.get(index)
            
            # Don't remove effects entry
            if not item_text.startswith("✨"):
                self.liste_balles.delete(index)
                # Remove from params list (accounting for effects entry)
                ball_index = index
                if any(self.liste_balles.get(i).startswith("✨") 
                       for i in range(self.liste_balles.size()) if i < index):
                    ball_index -= 1
                if 0 <= ball_index < len(self.balle_params_list):
                    self.balle_params_list.pop(ball_index)
    
    def _load_existing_config(self):
        """Load existing configuration if available."""
        self.bg_entry.insert(0, self.config.get("background", ""))
        
        theme = self.config.get_circle_theme()
        if theme in self.cerclesTheme['values']:
            self.cerclesTheme.set(theme)
            self._on_theme_change()
        
        color = self.config.get_circle_color()
        self.cerclesColor_entry.insert(0, str(color))
        
        mode = self.config.get_game_mode()
        if mode in self.modeJeu_combo['values']:
            self.modeJeu_combo.set(mode)
            self._on_mode_jeu_change()
        
        # Load balls
        custom_balls = self.config.get_custom_balls()
        for ball in custom_balls:
            self.balle_params_list.append(ball)
            info = f"Ball {len(self.balle_params_list)} - Radius: {ball.get('radius', 20)}"
            self.liste_balles.insert(tk.END, info)
        
        # Load advanced options
        advanced = self.config.get("balleOptionsAvanced", {})
        if advanced:
            self.balleOptionAvanced = advanced
            info = f"✨ Effects: {advanced.get('mode', 'none')} / {advanced.get('onBounce', 'none')}"
            self.liste_balles.insert(tk.END, info)
    
    def _launch_game(self):
        """Validate configuration and launch the game."""
        # Validation
        if self.cerclesTheme.get() != "triple" and len(self.balle_params_list) == 0:
            messagebox.showwarning(
                "Warning",
                "Please add at least one ball (or select 'triple' theme)."
            )
            return
        
        # Get circle color
        try:
            if self.cerclesTheme.get() in ["unicolor"]:
                cercles_color = ast.literal_eval(self.cerclesColor_entry.get())
            else:
                cercles_color = [255, 255, 255]
        except:
            messagebox.showerror(
                "Error",
                "Invalid circle color. Expected format: (R, G, B)"
            )
            return
        
        # Get timer
        try:
            timer = int(self.timer_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Timer must be a number")
            return
        
        # Get min_radius if visible
        try:
            min_radius = int(self.min_radius_entry.get())
        except ValueError:
            min_radius = DEFAULT_MIN_RADIUS
        
        # Build configuration
        config_data = {
            "background": self.bg_entry.get() or "images/noir.jpg",
            "cerclesTheme": self.cerclesTheme.get(),
            "cerclesColor": list(cercles_color) if isinstance(cercles_color, tuple) else cercles_color,
            "timer": timer,
            "modeJeu": self.modeJeu_combo.get(),
            "min_radius": min_radius,
            "balles_custom": self.balle_params_list,
            "balleOptionsAvanced": self.balleOptionAvanced
        }
        
        # Save configuration
        self.config.config = config_data
        if self.config.save():
            print("Configuration saved successfully!")
            
            # Launch game
            try:
                game_path = Path(__file__).resolve().parents[1] / "launchers/jeu.py"
                subprocess.run(["python3", str(game_path)])
            except FileNotFoundError:
                try:
                    game_path = Path(__file__).resolve().parents[1] / "launchers/jeu.py"
                    subprocess.run(["python3", str(game_path)])

                except Exception as e:
                    messagebox.showerror("Error", f"Could not launch game: {e}")
        else:
            messagebox.showerror("Error", "Could not save configuration")
    
    def run(self):
        """Start the launcher."""
        self.root.mainloop()


if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()