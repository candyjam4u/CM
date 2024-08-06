import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import random
import sqlite3
from PIL import Image
import os
import threading
import numpy as np
import subprocess
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')

IMAGE_PATH = os.path.join(RESOURCES_DIR, 'pictures', 'DesignerGray.png')
character_db_path = os.path.join(RESOURCES_DIR, 'character_information.db')
equipment_db_path = os.path.join(RESOURCES_DIR, 'Equipment.db')

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600
IMAGE_PATH = 'resources/pictures/DesignerGray.png'

resources_dir = 'resources'
character_db_path = os.path.join(resources_dir, 'character_information.db')
equipment_db_path = os.path.join(resources_dir, 'Equipment.db')

def run_setup_script(script_name):
    original_cwd = os.getcwd()
    try:
        os.chdir(resources_dir)
        subprocess.run(['python', script_name], check=True)
    finally:
        os.chdir(original_cwd)

if not os.path.exists(character_db_path):
    print(f"{character_db_path} not found. Running Setup_Character_Logic.py...")
    run_setup_script(os.path.join(RESOURCES_DIR, 'Setup_Character_Logic.py'))

if not os.path.exists(equipment_db_path):
    print(f"{equipment_db_path} not found. Running Setup_Equipment.py...")
    run_setup_script(os.path.join(RESOURCES_DIR, 'Setup_Equipment.py'))

conn_equipment = sqlite3.connect(equipment_db_path)
cursor_equipment = conn_equipment.cursor()

conn_info = sqlite3.connect(character_db_path)
cursor_info = conn_info.cursor()

conn_characters = sqlite3.connect(character_db_path)
cursor_characters = conn_characters.cursor()

print("Starting the main script...")

cursor_info.execute('SELECT id, name FROM races')
races = cursor_info.fetchall()

cursor_info.execute('SELECT id, name FROM classes')
classes = cursor_info.fetchall()

conn_characters = sqlite3.connect('resources/Characters.db')
cursor_characters = conn_characters.cursor()

cursor_characters.execute('''CREATE TABLE IF NOT EXISTS characters (
                                id INTEGER PRIMARY KEY,
                                Jméno TEXT,
                                Rasa TEXT,
                                Povolání TEXT,
                                Pohlaví TEXT,
                                Síla TEXT,
                                Obratnost TEXT,
                                Odolnost TEXT,
                                Inteligence TEXT,
                                Charisma TEXT,
                                HP INTEGER,
                                MaxHP INTEGER,
                                Mana INTEGER,
                                MaxMana INTEGER,
                                StatusEffect TEXT,
                                MeleeWeapon TEXT,
                                RangedWeapon TEXT,
                                Armor TEXT,
                                Shield TEXT,
                                Notes TEXT,
                                Lv INTEGER
                            )''')
conn_characters.commit()

def fetch_characters():
    try:
        with sqlite3.connect('resources/characters.db') as conn:
            cursor_characters = conn.cursor()
            cursor_characters.execute('SELECT * FROM characters')
            characters = cursor_characters.fetchall()
        return characters
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def fetch_equipment(category):
    try:
        with sqlite3.connect('resources/equipment.db') as conn:
            cursor_equipment = conn.cursor()
            if category == 'melee_weapon':
                cursor_equipment.execute(f'SELECT name, ÚČ, Útočnost, OČ FROM {category}')
            elif category == 'ranged_weapon':
                cursor_equipment.execute(f'SELECT name, ÚČ, Útočnost, OČ FROM {category}')
            else:
                cursor_equipment.execute(f'SELECT category, OČ FROM {category}')
            return [row[0] for row in cursor_equipment.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def update_stats(character_id, updates):
    set_clause = ', '.join([f"{stat} = ?" for stat in updates.keys()])
    values = list(updates.values()) + [character_id]
    cursor_characters.execute(f'''
        UPDATE characters 
        SET {set_clause}
        WHERE id = ?
    ''', values)
    conn_characters.commit()

def fetch_melee_weapon_details(selected_melee_weapon):
    with sqlite3.connect('resources/equipment.db') as conn:
        cursor_equipment = conn.cursor()
        cursor_equipment.execute("SELECT ÚČ, Útočnost, OČ, Rodová_zbraň FROM melee_weapon WHERE name = ?", (selected_melee_weapon,))
        return cursor_equipment.fetchone()

def fetch_ranged_weapon_details(selected_ranged_weapon):
    with sqlite3.connect('resources/equipment.db') as conn:
        cursor_equipment = conn.cursor()
        cursor_equipment.execute("SELECT ÚČ, Útočnost, OČ, Rodová_zbraň FROM ranged_weapon WHERE name = ?", (selected_ranged_weapon,))
        return cursor_equipment.fetchone()

def fetch_armor_details(selected_armor):
    with sqlite3.connect('resources/equipment.db') as conn:
        cursor_equipment = conn.cursor()
        cursor_equipment.execute("SELECT OČ FROM armor WHERE category = ?", (selected_armor,))
        return cursor_equipment.fetchone()

def fetch_shield_details(selected_shield):
    with sqlite3.connect('resources/equipment.db') as conn:
        cursor_equipment = conn.cursor()
        cursor_equipment.execute("SELECT OČ FROM shield WHERE category = ?", (selected_shield,))
        return cursor_equipment.fetchone()

def fetch_random_melee_weapon(character_class=None):
    with sqlite3.connect('resources/equipment.db') as conn:
        cursor_equipment = conn.cursor()
        if character_class == "Kouzelník":
            valid_ids = (1, 2, 10, 11, 16, 22)
        elif character_class == "Alchymista":
            valid_ids = (1, 2, 10, 11, 16, 22)
        elif character_class == "Hraničář":
            valid_ids = (1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 16, 18, 19, 22)
        elif character_class == "Zloděj":
            valid_ids = (1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 16, 18, 19, 22)
        else:
            valid_ids = None
        
        if valid_ids:
            cursor_equipment.execute(f'SELECT name FROM melee_weapon WHERE id IN {valid_ids} ORDER BY RANDOM() LIMIT 1')
        else:
            cursor_equipment.execute('SELECT name FROM melee_weapon ORDER BY RANDOM() LIMIT 1')
        
        row = cursor_equipment.fetchone()
        if row:
            return row[0]
        return None

def fetch_random_ranged_weapon(character_class=None):
    with sqlite3.connect('resources/equipment.db') as conn:
        cursor_equipment = conn.cursor()
        if character_class == "Kouzelník":
            valid_ids = (1, 7, 8, 9, 10, 11)
        elif character_class == "Alchymista":
            valid_ids = (1, 2, 3, 4, 6, 7, 8, 9, 10, 11)
        elif character_class == "Hraničář":
            valid_ids = (1, 2, 3, 4, 6, 7, 8, 9, 10, 11)
        elif character_class == "Zloděj":
            valid_ids = (1, 2, 3, 4, 6, 7, 8, 9, 10, 11)
        else:
            valid_ids = None
        
        if valid_ids:
            cursor_equipment.execute(f'SELECT name FROM ranged_weapon WHERE id IN {valid_ids} ORDER BY RANDOM() LIMIT 1')
        else:
            cursor_equipment.execute('SELECT name FROM ranged_weapon ORDER BY RANDOM() LIMIT 1')
        
        row = cursor_equipment.fetchone()
        if row:
            return row[0]
        return None

def fetch_random_armor(character_class=None):
    with sqlite3.connect('resources/equipment.db') as conn:
        cursor_equipment = conn.cursor()
        if character_class == "Kouzelník":
            valid_ids = (1, 1)
        elif character_class == "Alchymista":
            valid_ids = (1, 2, 3, 4)
        elif character_class == "Hraničář":
            valid_ids = (1, 2, 3, 4, 5)
        elif character_class == "Zloděj":
            valid_ids = (1, 2, 3)
        else:
            cursor_equipment.execute('SELECT id, category FROM armor ORDER BY RANDOM()')
            rows = cursor_equipment.fetchall()
            weighted_choices = [(row[1], 1 / row[0]) for row in rows]
            chosen_armor = random.choices(
                [armor for armor, weight in weighted_choices],
                [weight for armor, weight in weighted_choices]
            )[0]
            return chosen_armor

        cursor_equipment.execute(f'SELECT category FROM armor WHERE id IN {valid_ids} ORDER BY RANDOM() LIMIT 1')
        row = cursor_equipment.fetchone()
        if row:
            return row[0]
        return None

def fetch_random_shield(character_class=None, weapon_type=None):
    with sqlite3.connect('resources/equipment.db') as conn:
        cursor_equipment = conn.cursor()
        if character_class in ["Kouzelník", "Alchymista", "Zloděj"] or weapon_type == "Obouruční":
            cursor_equipment.execute('SELECT category FROM shield WHERE id = 1 ORDER BY RANDOM() LIMIT 1')
        else:
            cursor_equipment.execute('SELECT id, category FROM shield ORDER BY RANDOM()')
            rows = cursor_equipment.fetchall()
            weighted_choices = [(row[1], 1 / row[0]) for row in rows]
            chosen_shield = random.choices(
                [shield for shield, weight in weighted_choices],
                [weight for shield, weight in weighted_choices]
            )[0]
            return chosen_shield
        row = cursor_equipment.fetchone()
        if row:
            return row[0]
        return None

def fetch_character_by_id(character_id):
    try:
        with sqlite3.connect('resources/characters.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters WHERE id=?", (character_id,))
            character = cursor.fetchone()
        return character
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def calculate_stats(character_id, updates):
    with sqlite3.connect('resources/characters.db') as conn:
        cursor_characters = conn.cursor()
        set_clause = ', '.join([f"{stat} = ?" for stat in updates.keys()])
        values = list(updates.values()) + [character_id]
        cursor_characters.execute(f'''
            UPDATE characters 
            SET {set_clause}
            WHERE id = ?
        ''', values)
        conn.commit()

def close_db_connections():
    pass

def get_stat_ranges(race_id, class_id):
    cursor_info.execute('SELECT stat, min_value, max_value FROM stat_ranges WHERE race_id = ? AND class_id = ?',
                    (race_id, class_id))
    return cursor_info.fetchall()

def get_names_for_race_and_gender(race_id, gender):
    cursor_info.execute('SELECT name FROM names WHERE race_id = ? AND gender = ?', (race_id, gender))
    names = [row[0] for row in cursor_info.fetchall()]
    return names

def update_ids(*args):
    selected_race = race_name_var.get()
    selected_class = class_name_var.get()

    for race in races:
        if race[1] == selected_race:
            race_var.set(race[0])

    for cls in classes:
        if cls[1] == selected_class:
            class_var.set(cls[0])

def calculate_modifier(value):
    try:
        if '/' in value:
            value = value.split('/')[1].strip()
        return int(value)

    except ValueError:
        return 0
def run_in_thread(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.start()
    return thread

class ConfirmationPopup(ctk.CTkFrame):
    def __init__(self, parent, message, on_confirm, on_cancel):
        self.overlay = ctk.CTkFrame(parent, fg_color="transparent")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.tkraise()
        self.overlay.bind("<Button-1>", lambda e: None)

        super().__init__(self.overlay, corner_radius=10)
        self.place(relx=0.5, rely=0.5, anchor="center")
        self.configure(width=300, height=150)

        self.label = ctk.CTkLabel(self, text=message, wraplength=250, justify="center")
        self.label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10, fill="x")

        self.confirm_button = ctk.CTkButton(self.button_frame, text="Yes", command=lambda: self.confirm(on_confirm), fg_color='#676767', hover_color='#818181')
        self.confirm_button.pack(side="left", padx=20, pady=10, expand=True)

        self.cancel_button = ctk.CTkButton(self.button_frame, text="No", command=lambda: self.cancel(on_cancel), fg_color='#676767', hover_color='#818181')
        self.cancel_button.pack(side="right", padx=20, pady=10, expand=True)
        
        self.tkraise()

    def confirm(self, on_confirm):
        on_confirm()
        self.overlay.destroy()

    def cancel(self, on_cancel):
        on_cancel()
        self.overlay.destroy()

class CharacterManagerApp:
    def __init__(self, root):
        self.root = root or ctk.CTk()
        self.root.title("")
        self.root.geometry("810x620")
        self.all_races = ['Hobit', 'Kudůk', 'Trpaslík', 'Elf', 'Člověk', 'Barbar', 'Kroll']
        self.character_entries = {}
        self.notebook = None
        self.race_frames = {}
        self.race_content_frame = None
        self.current_race = None
        self.apply_dark_theme()
        self.characters_tabs()
        self.edit_mode = {}
        self.is_generating = False
        self.characters_by_race = {r: [] for r in self.all_races}
        self.font_color = "#2B2B2B"

        # Update paths for icons and images
        self.root.iconbitmap(os.path.join(RESOURCES_DIR, 'pictures', 'castergray.ico'))
        self.melee_image = ctk.CTkImage(light_image=Image.open(os.path.join(RESOURCES_DIR, 'pictures', 'melee.png')), size=(25, 25))
        self.ranged_image = ctk.CTkImage(light_image=Image.open(os.path.join(RESOURCES_DIR, 'pictures', 'ranged.png')), size=(25, 25))
        self.armor_image = ctk.CTkImage(light_image=Image.open(os.path.join(RESOURCES_DIR, 'pictures', 'armor.png')), size=(25, 25))
        self.shield_image = ctk.CTkImage(light_image=Image.open(os.path.join(RESOURCES_DIR, 'pictures', 'shield.png')), size=(25, 25))
        self.swordsb_image = ctk.CTkImage(light_image=Image.open(os.path.join(RESOURCES_DIR, 'pictures', 'swordsb.png')), size=(35, 35))
        self.arrowsb_image = ctk.CTkImage(light_image=Image.open(os.path.join(RESOURCES_DIR, 'pictures', 'arrowsb.png')), size=(35, 35))

    def apply_dark_theme(self):
        style = ttk.Style(self.root)
        self.root.tk.call("source", "resources/azure.tcl")
        ctk.set_appearance_mode("dark")
        style.configure("CTkButton", foreground="#676767")
        style.theme_use('azure-dark')
        style.configure("TLabel", foreground="#aeaeae", background="#2B2B2B")
        style.configure("TButton", foreground="#aeaeae")
        style.configure("TLabel", foreground= "#aeaeae")
        style.configure("TNotebook", background="#242424")
        style.configure("TEntry", foreground="#aeaeae")
        style.configure("TCombobox", foreground="#aeaeae")
        style.configure("CTkLabel", bg_color="#000000")

    def characters_tabs(self):
        def show_race_frame(race):
            characters = fetch_characters()
            characters_by_race = {r: [] for r in self.all_races}

            for character in characters:
                characters_by_race[character[2]].append(character)

            for r, frame in self.race_frames.items():
                if r == race:
                    if frame.winfo_ismapped():
                        frame.pack_forget()
                        your_image = ctk.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH)), size=(IMAGE_WIDTH, IMAGE_HEIGHT))
                        label = ctk.CTkLabel(self.race_content_frame, image=your_image, text='')
                        label.pack(fill="both", expand=True)
                        label.configure(anchor="center")
                    else:
                        self.hide_generate_widget()
                        frame.pack(expand=True, fill='both')
                        for widget in frame.winfo_children():
                            widget.destroy()
                        self.update_race_frame(frame, characters_by_race[race])
                else:
                    frame.pack_forget()

        race_buttons_frame = ctk.CTkFrame(self.root, fg_color='transparent')
        race_buttons_frame.pack(side='left', fill='y', padx=10, pady=30)

        self.race_frames = {}
        self.race_content_frame = ctk.CTkFrame(self.root, fg_color="#242424")
        self.race_content_frame.pack(side='left', expand=True, fill='both', padx=10, pady=10)

        your_image = ctk.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH)), size=(IMAGE_WIDTH, IMAGE_HEIGHT))
        label = ctk.CTkLabel(self.race_content_frame, image=your_image, text='')
        label.pack(fill="x")

        self.create_character_button = ctk.CTkButton(race_buttons_frame, text="GENERATE NEW", command=self.toggle_generate_widget, height=35, font=('Comfortaa', 18, 'bold'), corner_radius=8, fg_color='#676767', text_color='#242424', hover_color='#818181')
        self.create_character_button.pack(fill='x', pady=2, side='bottom')

        self.generate_widget_visible = False

        for col in range(5):
            self.race_content_frame.grid_columnconfigure(col, weight=5, minsize=100)

        for race in self.all_races:
            race_button = ctk.CTkButton(
                race_buttons_frame,
                command=lambda r=race: show_race_frame(r),
                height=35,
                text=race.upper(),
                font=('Comfortaa', 18, 'bold'),
                corner_radius=8,
                fg_color='#676767',
                text_color='#242424',
                hover_color="#818181"
            )
            race_button.pack(fill='x', pady=5)

            race_frame = ctk.CTkFrame(self.race_content_frame)
            self.race_frames[race] = race_frame

    def update_race_frame(self, frame, characters):
        global update_feedback
        race_notebook = ttk.Notebook(frame)
        race_notebook.pack(expand=True, fill='both')
        race_characters = characters

        for character in race_characters:
            character_id = character[0]
            character_tab = ctk.CTkFrame(race_notebook)
            race_notebook.add(character_tab, text=character[1])
            self.character_entries[character_id] = {}
            labels = ["Jméno", "Rasa", "Povolání", "Lv","Síla", "Obratnost", "Odolnost", "Inteligence", "Charisma"]
            values = character[1:4] + character[20:21] + character[5:11]

            # Configure columns for fixed sizes
            character_tab.grid_columnconfigure(0, minsize=120, weight=1)
            character_tab.grid_columnconfigure(1, minsize=80, weight=1, uniform="col")
            character_tab.grid_columnconfigure(2, minsize=20, weight=1, uniform="col")
            character_tab.grid_columnconfigure(3, minsize=120, weight=1, uniform="col")
            character_tab.grid_columnconfigure(4, minsize=50, weight=1)
            character_tab.grid_columnconfigure(5, minsize=50, weight=1, uniform="col")


            for i, (label, value) in enumerate(zip(labels, values)):
                ttk.Label(character_tab, text=label, font=('Comfortaa', 11, 'bold')).grid(row=i, column=0, padx=10, pady=7, sticky='w')
                label_widget = ttk.Label(character_tab, text=value)
                label_widget.grid(row=i, column=1, padx=10, pady=2, sticky='w')
                self.character_entries[character_id][label.lower()] = {"label": label_widget, "value": value}

            ttk.Label(character_tab, text="").grid(row=len(labels), column=0, padx=10, pady=2)

            additional_labels = ["HP", "Mana", "Status"]
            additional_values = [character[10] or character[11], character[12] or character[13], character[14] or '']
            stat_names = ["hp", "mana", "statuseffect"]

            for j, (label, value, stat_name) in enumerate(zip(additional_labels, additional_values, stat_names), start=len(labels) + 1):
                ctk.CTkLabel(character_tab, text_color='#aeaeae', text=label, font=('Comfortaa', 14, 'bold')).grid(row=j, column=0, padx=10, pady=0, sticky='w')

                if label == "Status":
                    entry_widget = ctk.CTkEntry(character_tab, text_color='#aeaeae', width=190)
                    entry_widget.grid(row=j, column=1, columnspan=2, padx=0, pady=2, sticky='w')
                else:
                    entry_widget = ctk.CTkEntry(character_tab, text_color='#aeaeae', width=35)
                    entry_widget.grid(row=j, column=1, padx=0, pady=2, sticky='w')

                entry_widget.insert(0, str(value))
                self.character_entries[character_id][stat_name] = {"entry": entry_widget, "value": value}

            text_box_frame = ctk.CTkFrame(character_tab, fg_color="#676767", corner_radius=10)
            text_box_frame.grid(row=14, rowspan=5, column=0, columnspan=6, padx=10, pady=10, sticky='nsew')

            character_tab.grid_rowconfigure(14, weight=1)

            notes_entry = ctk.CTkTextbox(text_box_frame, text_color='#aeaeae', fg_color="#2B2B2B", height=5)
            notes_entry.insert("1.0", str(character[19] or ""))
            notes_entry.pack(expand=True, fill='both', padx=2, pady=2)

            self.character_entries[character_id]["notes"] = {"entry": notes_entry, "value": character[19]}

            ctk.CTkLabel(character_tab, text="/").grid(row=len(labels) + 1, column=1, padx=10, pady=0)
            hp_maxhp_label = ctk.CTkLabel(character_tab, text=str(character[11] or 0), text_color='#aeaeae', width=35)
            hp_maxhp_label.grid(row=len(labels) + 1, column=1, padx=0, pady=0, sticky='e')
            self.character_entries[character_id]["maxhp"] = {"label": hp_maxhp_label, "value": character[11]}

            ctk.CTkLabel(character_tab, text="/").grid(row=len(labels) + 2, column=1, padx=10, pady=0)
            mana_maxmana_label = ctk.CTkLabel(character_tab, text=str(character[13] or 0), text_color='#aeaeae', width=35)
            mana_maxmana_label.grid(row=len(labels) + 2, column=1, padx=0, pady=1, sticky='e')
            self.character_entries[character_id]["maxmana"] = {"label": mana_maxmana_label, "value": character[13]}

            ctk.CTkLabel(character_tab, text="", image=self.melee_image).grid(row=0, column=2, padx=10, pady=1, sticky='e')
            ctk.CTkLabel(character_tab, text="", image=self.ranged_image).grid(row=1, column=2, padx=10, pady=1, sticky='e')
            ctk.CTkLabel(character_tab, text="", image=self.armor_image).grid(row=0, column=4, padx=0, pady=1, sticky='w')
            ctk.CTkLabel(character_tab, text="", image=self.shield_image).grid(row=1, column=4, padx=0, pady=1, sticky='w')

            meleeweapon_label_text = character[15] if len(character) > 15 and character[15] else ""
            rangedweapon_label_text = character[16] if len(character) > 16 and character[16] else ""
            armor_label_text = character[17] if len(character) > 17 and character[17] else ""
            shield_label_text = character[18] if len(character) > 18 and character[18] else ""

            meleeweapon_label = ttk.Label(character_tab, text=meleeweapon_label_text)
            rangedweapon_label = ttk.Label(character_tab, text=rangedweapon_label_text)
            armor_label = ttk.Label(character_tab, text=armor_label_text)
            shield_label = ttk.Label(character_tab, text=shield_label_text)

            self.character_entries[character_id]["meleeweapon_label"] = meleeweapon_label
            self.character_entries[character_id]["rangedweapon_label"] = rangedweapon_label
            self.character_entries[character_id]["armor_label"] = armor_label
            self.character_entries[character_id]["shield_label"] = shield_label

            self.character_entries[character_id]["selected_melee_weapon"] = meleeweapon_label_text
            self.character_entries[character_id]["selected_ranged_weapon"] = rangedweapon_label_text
            self.character_entries[character_id]["selected_armor"] = armor_label_text
            self.character_entries[character_id]["selected_shield"] = shield_label_text

            meleeweapon_dropdown = ttk.Combobox(character_tab, values=fetch_equipment('melee_weapon'), width=100)
            rangedweapon_dropdown = ttk.Combobox(character_tab, values=fetch_equipment('ranged_weapon'), width=100)
            armor_dropdown = ttk.Combobox(character_tab, values=fetch_equipment('armor'), width=100)
            shield_dropdown = ttk.Combobox(character_tab, values=fetch_equipment('shield'), width=100)

            self.character_entries[character_id]["meleeweapon_dropdown"] = meleeweapon_dropdown
            self.character_entries[character_id]["rangedweapon_dropdown"] = rangedweapon_dropdown
            self.character_entries[character_id]["armor_dropdown"] = armor_dropdown
            self.character_entries[character_id]["shield_dropdown"] = shield_dropdown

            meleeweapon_dropdown.bind("<<ComboboxSelected>>", lambda event, cid=character_id: self.on_equipment_selected("meleeweapon", cid))
            rangedweapon_dropdown.bind("<<ComboboxSelected>>", lambda event, cid=character_id: self.on_equipment_selected("rangedweapon", cid))
            armor_dropdown.bind("<<ComboboxSelected>>", lambda event, cid=character_id: self.on_equipment_selected("armor", cid))
            shield_dropdown.bind("<<ComboboxSelected>>", lambda event, cid=character_id: self.on_equipment_selected("shield", cid))

            self.character_entries[character_id]["selected_melee_weapon"] = meleeweapon_label_text
            self.character_entries[character_id]["selected_ranged_weapon"] = rangedweapon_label_text
            self.character_entries[character_id]["selected_armor"] = armor_label_text
            self.character_entries[character_id]["selected_shield"] = shield_label_text

            meleeweapon_label.grid(row=0, column=3, padx=10, pady=2, sticky='w')
            rangedweapon_label.grid(row=1, column=3, padx=10, pady=2, sticky='w')
            armor_label.grid(row=0, column=5, padx=10, pady=2, sticky='w')
            shield_label.grid(row=1, column=5, padx=10, pady=2, sticky='w')

            ctk.CTkLabel(character_tab, image= self.swordsb_image, text="").grid(row=4, column=2, padx=25)
            ctk.CTkLabel(character_tab, text="ÚČ:", text_color='#aeaeae', bg_color= "transparent", font=('Comfortaa', 14, 'bold')).grid(row=4, column=2, padx=10, pady=2, sticky='e')
            uc_melee_label = ctk.CTkLabel(character_tab, text=str(character[18] if len(character) > 15 else ""))
            uc_melee_label.grid(row=4, column=3, padx=10, pady=2, sticky='w')
            self.character_entries[character_id]["uc_melee_label"] = uc_melee_label

            ctk.CTkLabel(character_tab, text="Útočnost:", text_color='#aeaeae', font=('Comfortaa', 14, 'bold')).grid(row=4, column=3, padx=10, pady=2, sticky='e')
            utocnost_melee_label = ctk.CTkLabel(character_tab, text=str(character[20] if len(character) > 20 else ""))
            utocnost_melee_label.grid(row=4, column=4, padx=10, pady=2, sticky='w')
            self.character_entries[character_id]["utocnost_melee_label"] = utocnost_melee_label

            ctk.CTkLabel(character_tab, text="OČ:", text_color='#aeaeae', font=('Comfortaa', 14, 'bold')).grid(row=5, column=2, padx=10, pady=2, sticky='e')
            oc_melee_label = ctk.CTkLabel(character_tab, text=str(character[19] if len(character) > 19 else ""))
            oc_melee_label.grid(row=5, column=3, padx=10, pady=2, sticky='w')
            self.character_entries[character_id]["oc_melee_label"] = oc_melee_label

            ctk.CTkLabel(character_tab, image= self.arrowsb_image, text="").grid(row=7, column=2,  padx=2)
            ctk.CTkLabel(character_tab, text="ÚČ:", text_color='#aeaeae', font=('Comfortaa', 14, 'bold')).grid(row=7, column=2, padx=10, pady=2, sticky='e')
            uc_ranged_label = ctk.CTkLabel(character_tab, text=str(character[18] if len(character) > 18 else ""))
            uc_ranged_label.grid(row=7, column=3, padx=10, pady=2, sticky='w')
            self.character_entries[character_id]["uc_ranged_label"] = uc_ranged_label

            ctk.CTkLabel(character_tab, text="Útočnost:", text_color='#aeaeae', font=('Comfortaa', 14, 'bold')).grid(row=7, column=3, padx=10, pady=2, sticky='e')
            utocnost_ranged_label = ctk.CTkLabel(character_tab, text=str(character[20] if len(character) > 20 else ""))
            utocnost_ranged_label.grid(row=7, column=4, padx=10, pady=2, sticky='w')
            self.character_entries[character_id]["utocnost_ranged_label"] = utocnost_ranged_label

            ctk.CTkLabel(character_tab, text="OČ:", text_color='#aeaeae', font=('Comfortaa', 14, 'bold')).grid(row=8, column=2, padx=10, pady=2, sticky='e')
            oc_ranged_label = ctk.CTkLabel(character_tab, text=str(character[19] if len(character) > 19 else ""))
            oc_ranged_label.grid(row=8, column=3, padx=10, pady=2, sticky='w')
            self.character_entries[character_id]["oc_ranged_label"] = oc_ranged_label
            
            edit_button = ctk.CTkButton(character_tab, text="EDIT CHARACTER", command=lambda cid=character_id: self.toggle_edit_mode(cid), width=135, font=('Comfortaa', 12, 'bold'), corner_radius=8, fg_color='#676767', text_color='#242424', hover_color='#818181')
            edit_button.grid(row=11, column=4, columnspan=3, padx=10, sticky='e')
            self.character_entries[character_id]["edit_button"] = edit_button

            save_button = ctk.CTkButton(character_tab, text="SAVE CHARACTER", command=lambda cid=character_id: self.save_edit(cid), width=135, font=('Comfortaa', 12, 'bold'), corner_radius=8, fg_color='#676767', text_color='#242424', hover_color='#818181')
            save_button.grid(row=11, column=4, columnspan=3, padx=10, sticky='e')
            save_button.grid_remove()
            self.character_entries[character_id]["save_button"] = save_button

            update_button = ctk.CTkButton(character_tab, text="UPDATE", command=lambda cid=character_id: self.update_additional_stats(cid), width=80, font=('Comfortaa', 12, 'bold'), corner_radius=8, fg_color='#676767', text_color='#242424', hover_color='#818181')
            update_button.grid(row=11, column=2, padx=0)
            self.character_entries[character_id]["update_button"] = update_button

            update_feedback = ctk.StringVar()
            update_feedback_label = ctk.CTkLabel(character_tab, textvariable=update_feedback, text_color='#aeaeae')
            update_feedback_label.grid(row=10, column=2)

            self.character_entries[character_id]["update_feedback"] = update_feedback

            self.character_entries[character_id]["update_feedback_label"] = update_feedback_label

            delete_button = ctk.CTkButton(character_tab, text="DELETE CHARACTER", command=lambda cid=character_id: self.delete_character(cid), width=135, font=('Comfortaa', 12, 'bold'), corner_radius=8, fg_color='#676767', text_color='#242424', hover_color='#818181')
            delete_button.grid(row=12, column=4, columnspan=3, pady=5, padx=10, sticky='e')
            self.character_entries[character_id]["delete_button"] = delete_button

            self.calculate_stats(character_id)


    def delete_character(self, character_id):
        def confirm_deletion():
            cursor_characters.execute('DELETE FROM characters WHERE id = ?', (character_id,))
            conn_characters.commit()
            self.refresh_character_tabs()

        def cancel_deletion():
            pass

        ConfirmationPopup(self.root, "Are you sure you want to delete this character?", confirm_deletion, cancel_deletion)

    def refresh_character_tabs(self):
        characters = fetch_characters()
        self.characters_by_race = {r: [] for r in self.all_races}

        for character in characters:
            self.characters_by_race[character[2]].append(character)

        for race, frame in self.race_frames.items():
            if frame.winfo_ismapped():
                for widget in frame.winfo_children():
                    widget.destroy()
                self.update_race_frame(frame, self.characters_by_race[race])

    def toggle_generate_widget(self):
        if self.generate_widget_visible:
            self.hide_generate_widget()
            your_image = ctk.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH)), size=(IMAGE_WIDTH, IMAGE_HEIGHT))
            label = ctk.CTkLabel(self.race_content_frame, image=your_image, text='')
            label.pack(fill="x")
        else:
            self.show_generate_widget()

    def show_generate_widget(self):
        self.generate_widget(self.race_content_frame)
        self.generate_widget_visible = True

    def hide_generate_widget(self):
        for widget in self.race_content_frame.winfo_children():
            widget.pack_forget()
        self.generate_widget_visible = False

    def toggle_edit_mode(self, character_id):
        for stat in ["jméno", "lv", "síla", "obratnost", "odolnost", "inteligence", "charisma"]:
            entry_widget = ctk.CTkEntry(self.character_entries[character_id][stat]["label"].master , width=70, text_color='#aeaeae')
            entry_widget.insert(0, str(self.character_entries[character_id][stat]["value"]))
            entry_widget.grid(row=self.character_entries[character_id][stat]["label"].grid_info()["row"], column=1, padx=10, pady=2, sticky='w')
            self.character_entries[character_id][stat]["label"].grid_remove()
            self.character_entries[character_id][stat]["label"] = entry_widget

        for stat in ["maxhp", "maxmana"]:
            entry_widget = ctk.CTkEntry(self.character_entries[character_id][stat]["label"].master , width=35, text_color='#aeaeae')
            entry_widget.insert(0, str(self.character_entries[character_id][stat]["value"]))
            entry_widget.grid(row=self.character_entries[character_id][stat]["label"].grid_info()["row"], column=1, padx=0, pady=2, sticky='e')
            self.character_entries[character_id][stat]["label"].grid_remove()
            self.character_entries[character_id][stat]["label"] = entry_widget

        self.character_entries[character_id]["edit_button"].grid_remove()
        self.character_entries[character_id]["save_button"].grid()

        equipment_positions = {
            "meleeweapon": (0, 3),
            "rangedweapon": (1, 3),
            "armor": (0, 5),
            "shield": (1, 5)
        }

        for equipment_type in ["meleeweapon", "rangedweapon", "armor", "shield"]:
            equipment_label = self.character_entries[character_id][f"{equipment_type}_label"]
            equipment_dropdown = self.character_entries[character_id][f"{equipment_type}_dropdown"]

            if equipment_label and equipment_dropdown:
                equipment_dropdown.set(equipment_label.cget("text"))
                equipment_dropdown.grid(row=equipment_positions[equipment_type][0], column=equipment_positions[equipment_type][1], padx=10, pady=2, sticky='w')
                equipment_label.grid_remove()

    def save_edit(self, character_id):
        updates = {}
        for stat in ["jméno","lv", "síla", "obratnost", "odolnost", "inteligence", "charisma"]:
            updated_value = self.character_entries[character_id][stat]["label"].get()
            updates[stat] = updated_value

            label_widget = ctk.CTkLabel(self.character_entries[character_id][stat]["label"].master, text=updated_value, text_color='#aeaeae')
            label_widget.grid(row=self.character_entries[character_id][stat]["label"].grid_info()["row"], column=1, padx=10, pady=2, sticky='w')
            self.character_entries[character_id][stat]["label"].grid_remove()
            self.character_entries[character_id][stat]["label"] = label_widget
            self.character_entries[character_id][stat]["value"] = updated_value

        for stat in ["maxhp", "maxmana"]:
            updated_value = self.character_entries[character_id][stat]["label"].get()
            updates[stat] = updated_value

            label_widget = ctk.CTkLabel(self.character_entries[character_id][stat]["label"].master, text=updated_value, text_color='#aeaeae')
            label_widget.grid(row=self.character_entries[character_id][stat]["label"].grid_info()["row"], column=1, padx=10, pady=2, sticky='e')
            self.character_entries[character_id][stat]["label"].grid_remove()
            self.character_entries[character_id][stat]["label"] = label_widget
            self.character_entries[character_id][stat]["value"] = updated_value

        for equipment_type in ["meleeweapon", "rangedweapon", "armor", "shield"]:
            equipment_dropdown = self.character_entries[character_id][f"{equipment_type}_dropdown"]
            selected_equipment = equipment_dropdown.get()
            updates[equipment_type] = selected_equipment

            original_row = equipment_dropdown.grid_info()["row"]
            original_column = equipment_dropdown.grid_info()["column"]

            label_widget = ctk.CTkLabel(equipment_dropdown.master, text=selected_equipment, text_color='#aeaeae')
            label_widget.grid(row=original_row, column=original_column, padx=10, pady=2, sticky='w')
            equipment_dropdown.grid_remove()
            self.character_entries[character_id][f"{equipment_type}_label"] = label_widget
            self.character_entries[character_id][f"{equipment_type}_value"] = selected_equipment

        calculate_stats(character_id, updates)

        self.character_entries[character_id]["edit_button"].grid()
        self.character_entries[character_id]["save_button"].grid_remove()

    def calculate_stats(self, character_id):
        try:
            selected_melee_weapon = self.character_entries[character_id].get("selected_melee_weapon", "")
            selected_ranged_weapon = self.character_entries[character_id].get("selected_ranged_weapon", "")
            selected_armor = self.character_entries[character_id].get("selected_armor", "")
            selected_shield = self.character_entries[character_id].get("selected_shield", "")

            character = fetch_character_by_id(character_id)
            character_race = character[2]
            str_modifier = calculate_modifier(character[5]) 
            dex_modifier = calculate_modifier(character[6]) 

            uc_melee = 0
            utocnost_melee = 0
            oc_melee = 0

            uc_ranged = 0
            utocnost_ranged = 0
            oc_ranged = 0

            melee_weapon_details = fetch_melee_weapon_details(selected_melee_weapon) if selected_melee_weapon else ("Error in equipment.db")
            ranged_weapon_details = fetch_ranged_weapon_details(selected_ranged_weapon) if selected_ranged_weapon else ("Error in equipment.db")
            armor_details = fetch_armor_details(selected_armor) if selected_armor else ("Error in equipment.db")
            shield_details = fetch_shield_details(selected_shield) if selected_shield else ("Error in equipment.db")

            if melee_weapon_details[3] == character_race:
                uc_melee_bonus = 1
            else:
                uc_melee_bonus = 0

            if ranged_weapon_details[3] == character_race:
                uc_ranged_bonus = 1
            else:
                uc_ranged_bonus = 0

            uc_melee = (melee_weapon_details[0] or 0) + str_modifier + uc_melee_bonus
            utocnost_melee = melee_weapon_details[1] or 0
            oc_melee = (armor_details[0] or 0) + (melee_weapon_details[2] or 0) + (shield_details[0] or 0) + dex_modifier

            uc_ranged = (ranged_weapon_details[0] or 0) + dex_modifier + uc_ranged_bonus
            utocnost_ranged = ranged_weapon_details[1] or 0
            oc_ranged = (armor_details[0] or 0) + (ranged_weapon_details[2] or 0) + (shield_details[0] or 0) + dex_modifier

            uc_melee_label = self.character_entries[character_id]["uc_melee_label"]
            oc_melee_label = self.character_entries[character_id]["oc_melee_label"]
            utocnost_melee_label = self.character_entries[character_id]["utocnost_melee_label"]

            uc_melee_label.configure(text=str(uc_melee))
            oc_melee_label.configure(text=str(oc_melee))
            utocnost_melee_label.configure(text=str(utocnost_melee))

            uc_ranged_label = self.character_entries[character_id]["uc_ranged_label"]
            oc_ranged_label = self.character_entries[character_id]["oc_ranged_label"]
            utocnost_ranged_label = self.character_entries[character_id]["utocnost_ranged_label"]

            uc_ranged_label.configure(text=str(uc_ranged))
            oc_ranged_label.configure(text=str(oc_ranged))
            utocnost_ranged_label.configure(text=str(utocnost_ranged))

        except (ValueError, IndexError) as e:
            uc_melee_label = self.character_entries[character_id]["uc_melee_label"]
            oc_melee_label = self.character_entries[character_id]["oc_melee_label"]
            utocnost_melee_label = self.character_entries[character_id]["utocnost_melee_label"]

            uc_melee_label.configure(text="0")
            oc_melee_label.configure(text="0")
            utocnost_melee_label.configure(text="0")

            uc_ranged_label = self.character_entries[character_id]["uc_ranged_label"]
            oc_ranged_label = self.character_entries[character_id]["oc_ranged_label"]
            utocnost_ranged_label = self.character_entries[character_id]["utocnost_ranged_label"]

            uc_ranged_label.configure(text="0")
            oc_ranged_label.configure(text="0")
            utocnost_ranged_label.configure(text="0")

            print(f"Error occurred during calculation: {e}")

    def on_equipment_selected(self, equipment_type, character_id):
        try:
            print(f"Selecting {equipment_type} for character ID: {character_id}")
            if equipment_type == "meleeweapon":
                meleeweapon_dropdown = self.character_entries[character_id]["meleeweapon_dropdown"]
                selected_melee_weapon = meleeweapon_dropdown.get()
                self.character_entries[character_id]["selected_melee_weapon"] = selected_melee_weapon

            elif equipment_type == "rangedweapon":
                rangedweapon_dropdown = self.character_entries[character_id]["rangedweapon_dropdown"]
                selected_ranged_weapon = rangedweapon_dropdown.get()
                self.character_entries[character_id]["selected_ranged_weapon"] = selected_ranged_weapon
            
            elif equipment_type == "armor":
                armor_dropdown = self.character_entries[character_id]["armor_dropdown"]
                selected_armor = armor_dropdown.get()
                self.character_entries[character_id]["selected_armor"] = selected_armor
            
            elif equipment_type == "shield":
                shield_dropdown = self.character_entries[character_id]["shield_dropdown"]
                selected_shield = shield_dropdown.get()
                self.character_entries[character_id]["selected_shield"] = selected_shield
            
            self.calculate_stats(character_id)
            print(f"Equipment selection updated for {equipment_type}")

        except (ValueError, IndexError) as e:
            print(f"Error occurred during {equipment_type} selection: {e}")

    def update_additional_stats(self, character_id):
        updates = {}
        for stat in ["hp", "mana", "statuseffect"]:
            updated_value = self.character_entries[character_id][stat]["entry"].get()
            updates[stat] = updated_value
            self.character_entries[character_id][stat]["value"] = updated_value

        notes_widget = self.character_entries[character_id]["notes"]["entry"]
        updated_notes = notes_widget.get("1.0", "end").strip()
        updates["notes"] = updated_notes
        self.character_entries[character_id]["notes"]["value"] = updated_notes

        update_stats(character_id, updates)

        update_feedback = self.character_entries[character_id]["update_feedback"]
        update_feedback.set("Updated")
        self.root.after(1800, lambda: update_feedback.set(""))

    def generate_widget(self, frame):
        global race_var, class_var, gender_var, name_var, race_name_var, class_name_var, result_text, save_feedback, result_label, lv_var
        self.is_generating = True

        for widget in self.race_content_frame.winfo_children():
            widget.pack_forget()

        generate_frame = ctk.CTkFrame(self.race_content_frame)
        generate_frame.pack(side='top', anchor='n')

        race_frame = ctk.CTkFrame(generate_frame, fg_color="#242424", bg_color="#242424")
        race_frame.pack(side='left', anchor='w')

        race_var = ctk.IntVar(value=races[0][0])
        race_name_var = ctk.StringVar(value=races[0][1])
        race_name_var.trace('w', update_ids)
        race_label = ctk.CTkLabel(race_frame, text="Race")
        race_label.pack(side='top', anchor='n')
        race_dropdown = ctk.CTkComboBox(race_frame, variable=race_name_var, values=[race[1] for race in races])
        race_dropdown.pack(side='top', anchor='w', padx='2', pady='3')

        class_frame = ctk.CTkFrame(generate_frame, fg_color="#242424", bg_color="#242424")
        class_frame.pack(side='left', anchor='w')

        class_var = ctk.IntVar(value=classes[0][0])
        class_name_var = ctk.StringVar(value=classes[0][1])
        class_name_var.trace('w', update_ids)
        class_label = ctk.CTkLabel(class_frame, text="Class")
        class_label.pack(side='top', anchor='n')
        class_dropdown = ctk.CTkComboBox(class_frame, variable=class_name_var, values=[cls[1] for cls in classes])
        class_dropdown.pack(side='top', anchor='w', padx='2', pady='3')

        lv_frame = ctk.CTkFrame(generate_frame, fg_color="#242424", bg_color="#242424")
        lv_frame.pack(side='left', anchor='w')

        lv_var = ctk.StringVar()
        lv_label = ctk.CTkLabel(lv_frame, text="Lv")
        lv_label.pack(side='top', anchor='n')
        lv_entry = ctk.CTkEntry(lv_frame, textvariable=lv_var)
        lv_entry.pack(side='top', anchor='w', padx='2', pady='3')

        details_frame = ctk.CTkFrame(frame)
        details_frame.pack(side='top', anchor='n', padx='5', pady='10')

        name_frame = ctk.CTkFrame(details_frame, fg_color="#242424", bg_color="#242424")
        name_frame.pack(side='left', anchor='w')

        name_var = ctk.StringVar()
        name_label = ctk.CTkLabel(name_frame, text="Name")
        name_label.pack(side='top', anchor='n')
        name_entry = ctk.CTkEntry(name_frame, textvariable=name_var)
        name_entry.pack(side='top', anchor='w', padx='20', pady='0')

        gender_frame = ctk.CTkFrame(details_frame, fg_color="#242424", bg_color="#242424")
        gender_frame.pack(side='left', anchor='w', padx='0', pady='0', expand=True, fill='both')

        gender_var = ctk.StringVar()
        male_radio = ctk.CTkRadioButton(gender_frame, text="Male", variable=gender_var, value="Muž", height=5)
        male_radio.pack(side='left', padx='10', pady='0')
        female_radio = ctk.CTkRadioButton(gender_frame, text="Female", variable=gender_var, value="Žena", height=5)
        female_radio.pack(side='left', padx='0', pady='0')

        buttons_frame = ctk.CTkFrame(frame, fg_color="#242424", bg_color="#242424")
        buttons_frame.pack(side='top', anchor='n')

        weak_button = ctk.CTkButton(buttons_frame, text="Weak", command=lambda: self.generate_stats(race_var.get(), class_var.get(), gender_var.get(), 'weak'))
        weak_button.pack(side='left', padx='2', pady='3')

        normal_button = ctk.CTkButton(buttons_frame, text="Normal", command=lambda: self.generate_stats(race_var.get(), class_var.get(), gender_var.get(), 'normal'))
        normal_button.pack(side='left', padx='2', pady='3')

        strong_button = ctk.CTkButton(buttons_frame, text="Strong", command=lambda: self.generate_stats(race_var.get(), class_var.get(), gender_var.get(), 'strong'))
        strong_button.pack(side='left', padx='2', pady='3')

        result_text = ctk.StringVar()
        result_label = ctk.CTkLabel(frame, textvariable=result_text, font=("<Roboto>", 18))
        result_label.pack(side='top', anchor='n', padx=2, pady=3, ipadx=10, ipady=10)

        save_button = ctk.CTkButton(frame, text="Uložit", command=self.save_character_to_db)
        save_button.pack(side='bottom', anchor='s', padx='2', pady='3')

        save_feedback = ctk.StringVar()
        save_feedback_label = ctk.CTkLabel(frame, textvariable=save_feedback)
        save_feedback_label.pack(side='bottom', anchor='s')

        self.is_generating = False

    def save_character_to_db(self):
        try:
            details = result_text.get().split("\n")
            jméno = details[0].split(": ")[1]  
            rasa = race_name_var.get()
            povolání = class_name_var.get()
            pohlaví = gender_var.get()
            lv = details[4].split(": ")[1]
            síla = details[5].split(": ")[1]
            obratnost = details[6].split(": ")[1]
            odolnost = details[7].split(": ")[1]
            inteligence = details[8].split(": ")[1]
            charisma = details[9].split(": ")[1]
            max_hp = details[10].split(": ")[1]
            max_mana = details[11].split(": ")[1]

            self.save_character(jméno, rasa, povolání, pohlaví, lv, síla, obratnost, odolnost, inteligence, charisma, max_hp, max_mana)
            save_feedback.set(f"{jméno} Uložen/a")
            self.root.after(3000, self.hide_feedback)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save character: {str(e)}")

    def hide_feedback(self):
        save_feedback.set("")

    def save_character(self, name, race, character_class, gender, level, strength, dexterity, constitution, intelligence, charisma, max_hp, max_mana):
        random_melee_weapon = fetch_random_melee_weapon(character_class)
        random_ranged_weapon = fetch_random_ranged_weapon(character_class)

        print(f"Generated random weapons - Melee: {random_melee_weapon}, Ranged: {random_ranged_weapon}")

        random_armor = fetch_random_armor(character_class)
        print(f"Generated random armor: {random_armor}")

        random_shield = fetch_random_shield(character_class)
        print(f"Generated random shield: {random_shield}")

        cursor_characters.execute('''INSERT INTO characters (Jméno, Rasa, Povolání, Pohlaví, Lv, Síla, Obratnost, Odolnost, Inteligence, Charisma, MaxHP, MaxMana, MeleeWeapon, RangedWeapon, Armor, Shield)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (name, race, character_class, gender, level, strength, dexterity, constitution, intelligence, charisma, max_hp, max_mana, random_melee_weapon, random_ranged_weapon, random_armor, random_shield))
        conn_characters.commit()
        print(f"Character generated: {name}, {race} {character_class}, {gender}, Lv: {level}, Síla: {strength}, Obratnost: {dexterity}, Odolnost: {constitution}, Inteligence: {intelligence}, Charisma: {charisma}, Max HP: {max_hp}, Max Mana: {max_mana}")

    def get_modifier(self, value):
        if value == '':
            return ''
        value = int(value)
        if value == 1:
            return "/ -5"
        elif value in (2, 3):
            return "/ -4"
        elif value in (4, 5):
            return "/ -3"
        elif value in (6, 7):
            return "/ -2"
        elif value in (8, 9):
            return "/ -1"
        elif value in (10, 11, 12):
            return "/ +0"
        elif value in (13, 14):
            return "/ +1"
        elif value in (15, 16):
            return "/ +2"
        elif value in (17, 18):
            return "/ +3"
        elif value in (19, 20):
            return "/ +4"
        else:
            return "/ +5"

    def get_modifier_value(self, modifier_str):
        if '/' in modifier_str:
            return int(modifier_str.split('/')[1].strip())
        return 0

    def calculate_maxhp(self, level, constitution_modifier):
        if class_name_var.get() == "Válečník":
            base_hp = 10 + constitution_modifier
            hp = base_hp
            for _ in range(1, level):
                hp += random.randint(1, 10) + constitution_modifier
            return hp
        
        if class_name_var.get() == "Hraničář":
            base_hp = 8 + constitution_modifier
            hp = base_hp
            for _ in range(1, level):
                hp += random.randint(1, 6) +2 + constitution_modifier
            return hp
        if class_name_var.get() == "Alchymista":
            base_hp = 7 + constitution_modifier
            hp = base_hp
            for _ in range(1, level):
                hp += random.randint(1, 6) +1 + constitution_modifier
            return hp
        else:
            base_hp = 6 + constitution_modifier
            hp = base_hp
            for _ in range(1, level):
                hp += random.randint(1, 6) + constitution_modifier
            return hp

    def calculate_maxmana(self, level, intelligence, character_class):
        mana_table = {
            "Kouzelník": {
                1: {range(8, 10): 7, range(10, 12): 7, range(12, 14): 8, range(14, 16): 8, range(16, 18): 8, range(18, 20): 9, range(20, 22): 9},
                2: {range(8, 10): 10, range(10, 12): 11, range(12, 14): 12, range(14, 16): 12, range(16, 18): 12, range(18, 20): 13, range(20, 22): 14},
                3: {range(8, 10): 12, range(10, 12): 14, range(12, 14): 15, range(14, 16): 16, range(16, 18): 17, range(18, 20): 18, range(20, 22): 20},
                4: {range(8, 10): 14, range(10, 12): 17, range(12, 14): 19, range(14, 16): 20, range(16, 18): 21, range(18, 20): 23, range(20, 22): 26},
                5: {range(8, 10): 17, range(10, 12): 20, range(12, 14): 22, range(14, 16): 24, range(16, 18): 26, range(18, 20): 28, range(20, 22): 31},
                # Extend this pattern to level 10
            },
            "Hraničář": {
                1: {range(6, 8): 0, range(8, 10): 0, range(10, 12): 0, range(12, 14): 0, range(14, 16): 0, range(16, 18): 0, range(18, 20): 0},
                2: {range(6, 8): 3, range(8, 10): 3, range(10, 12): 3, range(12, 14): 3, range(14, 16): 3, range(16, 18): 3, range(18, 20): 3},
                3: {range(6, 8): 6, range(8, 10): 6, range(10, 12): 7, range(12, 14): 7, range(14, 16): 7, range(16, 18): 8, range(18, 20): 8},
                4: {range(6, 8): 10, range(8, 10): 10, range(10, 12): 11, range(12, 14): 11, range(14, 16): 11, range(16, 18): 12, range(18, 20): 13},
                5: {range(6, 8): 12, range(8, 10): 13, range(10, 12): 13, range(12, 14): 14, range(14, 16): 15, range(16, 18): 15, range(18, 20): 16},
                # Extend this pattern to level 10
            }
        }

        if character_class in mana_table:
            class_table = mana_table[character_class]
            if level in class_table:
                for int_range, mana in class_table[level].items():
                    if intelligence in int_range:
                        return mana
        return 0

    def generate_random_level(self):
        levels = np.arange(1, 11)
        probabilities = [0.16, 0.23, 0.23, 0.16, 0.15, 0.04, 0.01, 0.01, 0.005, 0.005]
        return np.random.choice(levels, p=probabilities)

    def generate_stats(self, race_id, class_id, gender, type):
        race_id = race_var.get()
        class_id = class_var.get()
        gender = gender_var.get() 
        
        if not gender:
            gender = self.get_random_gender()

        gender_code = 'M' if gender == 'Muž' else 'F'
        

        stat_ranges = get_stat_ranges(race_id, class_id)
        names = get_names_for_race_and_gender(race_id, gender_code)
        generated_stats = {}

        print(f"Generating stats for: {race_name_var.get()} {class_name_var.get()}, {gender} - {type}")


        for stat, min_val, max_val in stat_ranges:
            if type == 'weak':
                value = random.randint(min_val, (min_val + max_val) // 2)
            elif type == 'normal':
                value = random.randint(min_val, max_val)
            elif type == 'strong':
                value = random.randint((min_val + max_val) // 2, max_val)

            modifier = self.get_modifier(value)
            generated_stats[stat] = value

        selected_name = name_var.get() 
        if not selected_name:
            if names:
                selected_name = random.choice(names)
            else:
                selected_name = ""

        level = self.generate_random_level()
        lv_var.set(level)
        
        constitution_value = generated_stats.get('Odolnost', 10)
        constitution_modifier_str = self.get_modifier(constitution_value)
        constitution_modifier = self.get_modifier_value(constitution_modifier_str)
        
        max_hp = self.calculate_maxhp(level, constitution_modifier)
        
        intelligence_value = generated_stats.get('Inteligence', 10)
        max_mana = self.calculate_maxmana(level, intelligence_value, class_name_var.get())

        result_text.set(
            f"{'Jméno:'} {selected_name}\n"
            f"{'Rasa:'} {race_name_var.get()}\n"
            f"{'Povolání:'} {class_name_var.get()}\n"
            f"{'Pohlaví:'} {gender}\n"
            f"{'Úroveň:'} {level}\n"
            f"{'Síla:'} {generated_stats.get('Síla', '')} {self.get_modifier(generated_stats.get('Síla', ''))}\n"
            f"{'Obratnost:'} {generated_stats.get('Obratnost', '')} {self.get_modifier(generated_stats.get('Obratnost', ''))}\n"
            f"{'Odolnost:'} {generated_stats.get('Odolnost', '')} {self.get_modifier(generated_stats.get('Odolnost', ''))}\n"
            f"{'Inteligence:'} {generated_stats.get('Inteligence', '')} {self.get_modifier(generated_stats.get('Inteligence', ''))}\n"
            f"{'Charisma:'} {generated_stats.get('Charisma', '')} {self.get_modifier(generated_stats.get('Charisma', ''))}\n"
            f"{'Max HP:'} {max_hp}\n"
            f"{'Max Mana:'} {max_mana}"
        )

    def get_random_gender(self):
        return 'Muž' if random.random() < 0.75 else 'Žena'

if __name__ == "__main__":
    root = ctk.CTk()
    app = CharacterManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: [close_db_connections(), root.destroy()])
    root.mainloop()

print(f"EXITING CHARACTER MANAGER")
close_db_connections()
