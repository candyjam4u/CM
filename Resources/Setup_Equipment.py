import sqlite3

# Define weapon data including the new categories
melee_weapon_data = {
    'Žádná': [
        {'name': 'Bez zbraně', 'ÚČ': 0, 'Útočnost': 0, 'OČ': -3, 'type': 'Jednoruční', 'Rodová_zbraň': None},
    ],
    'Ostré zbraně': [
        {'name': 'Krátký meč', 'ÚČ': 4, 'Útočnost': -1, 'OČ': -1, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Dlouhý meč', 'ÚČ': 7, 'Útočnost': -1, 'OČ': 0, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Obouruční meč', 'ÚČ': 7, 'Útočnost': 1, 'OČ': -1, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Široký meč', 'ÚČ': 5, 'Útočnost': 0, 'OČ': 0, 'type': 'Jednoruční',  'Rodová_zbraň': 'Člověk'},
        {'name': 'Šavle', 'ÚČ': 4, 'Útočnost': 2, 'OČ': 1, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Bastard', 'ÚČ': 6, 'Útočnost': 0, 'OČ': 1, 'type': 'Jednoruční',  'Rodová_zbraň': 'Barbar'},
        {'name': 'Katana', 'ÚČ': 6, 'Útočnost': 1, 'OČ': -1, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Rapír', 'ÚČ': 8, 'Útočnost': -1, 'OČ': -1, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Tesák', 'ÚČ': 3, 'Útočnost': -1, 'OČ': -2, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Dýka', 'ÚČ': 2, 'Útočnost': -2, 'OČ': -2, 'type': 'Jednoruční',  'Rodová_zbraň': None},
    ],
    'Tupé zbraně': [
        {'name': 'Válečné kladivo', 'ÚČ': 5, 'Útočnost': 2, 'OČ': -1, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Cep', 'ÚČ': 5, 'Útočnost': 4, 'OČ': -1, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Řemdih', 'ÚČ': 4, 'Útočnost': 3, 'OČ': -2, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Kyj', 'ÚČ': 3, 'Útočnost': 2, 'OČ': -1, 'type': 'Jednoruční',  'Rodová_zbraň': 'Kroll'},
        {'name': 'Obušek', 'ÚČ': 3, 'Útočnost': -2, 'OČ': -2, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Palcát', 'ÚČ': 5, 'Útočnost': 1, 'OČ': 0, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Bič', 'ÚČ': 3, 'Útočnost': 3, 'OČ': -2, 'type': 'Jednoruční',  'Rodová_zbraň': None},
    ],
    'Sekyry': [
        {'name': 'Jednoruční sekera', 'ÚČ': 3, 'Útočnost': 1, 'OČ': -1, 'type': 'Jednoruční',  'Rodová_zbraň': 'Kudůk'},
        {'name': 'Obouruční sekera', 'ÚČ': 4, 'Útočnost': 3, 'OČ': -1, 'type': 'Obouruční',  'Rodová_zbraň': 'Trpaslík'},
        {'name': 'Dvoubřitá sekera', 'ÚČ': 4, 'Útočnost': 6, 'OČ': -3, 'type': 'Obouruční',  'Rodová_zbraň': None},
    ],
    'Hole': [
        {'name': 'Okovaná hůl', 'ÚČ': 5, 'Útočnost': -1, 'OČ': 1, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Halapartna', 'ÚČ': 4, 'Útočnost': 6, 'OČ': 2, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Píka', 'ÚČ': 5, 'Útočnost': 2, 'OČ': 1, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Trojzubec/vidle', 'ÚČ': 6, 'Útočnost': 2, 'OČ': 2, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Kopí', 'ÚČ': 5, 'Útočnost': 0, 'OČ': 1, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Dřevec', 'ÚČ': 12, 'Útočnost': 3, 'OČ': 0, 'type': 'Obouruční',  'Rodová_zbraň': None},
    ],
}
ranged_weapon_data = {
    'Žádná': [
        {'name': 'Bez zbraně', 'ÚČ': 0, 'Útočnost': 0, 'OČ': -3, 'type': 'Jednoruční', 'Rodová_zbraň': None},
    ],
    'Střelné zbraně': [
        {'name': 'Krátký luk', 'ÚČ': 4, 'Útočnost': 0, 'OČ': -3, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Dlouhý luk', 'ÚČ': 5, 'Útočnost': 1, 'OČ': -3, 'type': 'Obouruční',  'Rodová_zbraň': 'Elf'},
        {'name': 'Lehká kuše', 'ÚČ': 4, 'Útočnost': 1, 'OČ': -3, 'type': 'Obouruční',  'Rodová_zbraň': 'Hobit'},
        {'name': 'Těžká kuše', 'ÚČ': 6, 'Útočnost': 2, 'OČ': -3, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Prak', 'ÚČ': 4, 'Útočnost': -1, 'OČ': -3, 'type': 'Obouruční', 'range':'Ranged', 'Rodová_zbraň': None},
    ],
    'Vrhací zbraně': [
        {'name': 'Dýka (vrhací)', 'ÚČ': 2, 'Útočnost': 0, 'OČ': -2, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Sekera (vrhací)', 'ÚČ': 3, 'Útočnost': 1, 'OČ': -1, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Oštěp', 'ÚČ': 5, 'Útočnost': 1, 'OČ': -1, 'type': 'Obouruční',  'Rodová_zbraň': None},
        {'name': 'Kámen', 'ÚČ': 0, 'Útočnost': 1, 'OČ': -3, 'type': 'Jednoruční',  'Rodová_zbraň': None},
        {'name': 'Hvězdice', 'ÚČ': 1, 'Útočnost': 1, 'OČ': -3, 'type': 'Jednoruční',  'Rodová_zbraň': None},
    ],
}

armor_data = [
    {'category': 'Žádné', 'OČ': 1},
    {'category': 'Vycpávané', 'OČ': 2},
    {'category': 'Kožené', 'OČ': 3},
    {'category': 'Šupinové', 'OČ': 4},
    {'category': 'Kroužkové', 'OČ': 5},
    {'category': 'Plátové', 'OČ': 6},
    {'category': 'Rytířské', 'OČ': 7},
]

shield_data = [
    {'category': 'Žádný', 'OČ': 0},
    {'category': 'Kulatý', 'OČ': 1},
    {'category': 'Rytířský', 'OČ': 1},
    {'category': 'Tarče', 'OČ': 2},
    {'category': 'Mandlový', 'OČ': 2},
    {'category': 'Legionářský', 'OČ': 2},
    {'category': 'Pavéza', 'OČ': 4},
]

# SQLite database filename
db_filename = 'equipment.db'

def create_or_connect_db():
    """ Create or connect to the SQLite database """
    conn = sqlite3.connect(db_filename)
    return conn

def create_tables(conn):
    """ Create tables for weapon, armor, and shield if they don't exist """
    cursor = conn.cursor()
    
    # Create melee weapon table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS melee_weapon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            ÚČ INTEGER,
            Útočnost INTEGER,
            OČ INTEGER,
            type TEXT,
            Rodová_zbraň TEXT
        )
    ''')

    # Create ranged weapon table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ranged_weapon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            ÚČ INTEGER,
            Útočnost INTEGER,
            OČ INTEGER,
            type TEXT,
            Rodová_zbraň TEXT
        )
    ''')
    
    # Create armor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS armor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            OČ INTEGER
        )
    ''')
    
    # Create shield table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shield (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            OČ INTEGER
        )
    ''')
    
    conn.commit()

def insert_or_update_melee_weapon(conn):
    """ Insert or update melle_weapon in the database """
    cursor = conn.cursor()
    
    for category, melee_weapon in melee_weapon_data.items():
        for melee_weapon in melee_weapon:
            name = melee_weapon['name']
            ÚČ = melee_weapon.get('ÚČ', None)
            Útočnost = melee_weapon.get('Útočnost', None)
            OČ = melee_weapon.get('OČ', None)
            type = melee_weapon.get('type', None)
            Rodová_zbraň = melee_weapon.get('Rodová_zbraň', None)
            
            # Check if the weapon already exists in the database
            cursor.execute('''
                SELECT id FROM melee_weapon WHERE category=? AND name=?
            ''', (category, name))
            row = cursor.fetchone()
            
            if row:
                # Weapon exists, update it
                cursor.execute('''
                    UPDATE melee_weapon SET ÚČ=?, Útočnost=?, OČ=?, type=?, Rodová_zbraň=?
                    WHERE category=? AND name=?
                ''', (ÚČ, Útočnost, OČ, type, Rodová_zbraň, category, name))
            else:
                # Weapon does not exist, insert it
                cursor.execute('''
                    INSERT INTO melee_weapon (category, name, ÚČ, Útočnost, OČ, type, Rodová_zbraň)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (category, name, ÚČ, Útočnost, OČ, type, Rodová_zbraň))
    
    # Commit changes
    conn.commit()

def insert_or_update_ranged_weapon(conn):
    """ Insert or update ranged_weapon in the database """
    cursor = conn.cursor()
    
    for category, ranged_weapon in ranged_weapon_data.items():
        for ranged_weapon in ranged_weapon:
            name = ranged_weapon['name']
            ÚČ = ranged_weapon.get('ÚČ', None)
            Útočnost = ranged_weapon.get('Útočnost', None)
            OČ = ranged_weapon.get('OČ', None)
            type = ranged_weapon.get('type', None)
            Rodová_zbraň = ranged_weapon.get('Rodová_zbraň', None)
            
            # Check if the weapon already exists in the database
            cursor.execute('''
                SELECT id FROM ranged_weapon WHERE category=? AND name=?
            ''', (category, name))
            row = cursor.fetchone()
            
            if row:
                # Weapon exists, update it
                cursor.execute('''
                    UPDATE ranged_weapon SET ÚČ=?, Útočnost=?, OČ=?, type=?, Rodová_zbraň=?
                    WHERE category=? AND name=?
                ''', (ÚČ, Útočnost, OČ, type, Rodová_zbraň, category, name))
            else:
                # Weapon does not exist, insert it
                cursor.execute('''
                    INSERT INTO ranged_weapon (category, name, ÚČ, Útočnost, OČ, type, Rodová_zbraň)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (category, name, ÚČ, Útočnost, OČ, type, Rodová_zbraň))
    
    # Commit changes
    conn.commit()

def insert_or_update_armor(conn):
    """ Insert or update armor in the database """
    cursor = conn.cursor()
    
    for armor in armor_data:
        category = armor['category']
        OČ = armor['OČ']
        
        # Check if the armor category already exists in the database
        cursor.execute('''
            SELECT id FROM armor WHERE category=?
        ''', (category,))
        row = cursor.fetchone()
        
        if row:
            # Armor category exists, update it
            cursor.execute('''
                UPDATE armor SET OČ=?
                WHERE category=?
            ''', (OČ, category))
        else:
            # Armor category does not exist, insert it
            cursor.execute('''
                INSERT INTO armor (category, OČ)
                VALUES (?, ?)
            ''', (category, OČ))
    
    # Commit changes
    conn.commit()

def insert_or_update_shield(conn):
    """ Insert or update shield in the database """
    cursor = conn.cursor()
    
    for shield in shield_data:
        category = shield['category']
        OČ = shield['OČ']
        
        # Check if the shield category already exists in the database
        cursor.execute('''
            SELECT id FROM shield WHERE category=?
        ''', (category,))
        row = cursor.fetchone()
        
        if row:
            # Shield category exists, update it
            cursor.execute('''
                UPDATE shield SET OČ=?
                WHERE category=?
            ''', (OČ, category))
        else:
            # Shield category does not exist, insert it
            cursor.execute('''
                INSERT INTO shield (category, OČ)
                VALUES (?, ?)
            ''', (category, OČ))
    
    # Commit changes
    conn.commit()

def main():
    # Create or connect to the SQLite database
    conn = create_or_connect_db()
    
    # Create tables if they don't exist
    create_tables(conn)
    
    # Insert or update data in each table
    insert_or_update_melee_weapon(conn)
    insert_or_update_ranged_weapon(conn)
    insert_or_update_armor(conn)
    insert_or_update_shield(conn)
    
    # Close connection
    conn.close()
    
    print("Database operations completed successfully.")

if __name__ == '__main__':
    main()
