import sqlite3

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('character_information.db')
cursor = conn.cursor()

# Create tables for races, classes, stat ranges, and names
cursor.execute('''
CREATE TABLE IF NOT EXISTS races (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS stat_ranges (
    race_id INTEGER,
    class_id INTEGER,
    stat TEXT,
    min_value INTEGER,
    max_value INTEGER,
    FOREIGN KEY (race_id) REFERENCES races(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS names (
    id INTEGER PRIMARY KEY,
    race_id INTEGER,
    name TEXT,
    gender TEXT,          
    FOREIGN KEY (race_id) REFERENCES races(id)
)
''')

# Insert data for races
races = [('Hobit',), ('Kudůk',), ('Trpaslík',), ('Elf',), ('Člověk',), ('Barbar',), ('Kroll',)]
cursor.executemany('INSERT INTO races (name) VALUES (?)', races)

# Insert data for classes
classes = [('Válečník',), ('Hraničář',), ('Alchymista',), ('Kouzelník',), ('Zloděj',)]
cursor.executemany('INSERT INTO classes (name) VALUES (?)', classes)

# Insert names for each race
names = [
    (1, 'Pipenda', 'M'), (1, 'Rubert', 'M'), (1, 'Fridibald', 'M'), (1, 'Sibylbert', 'M'), (1, 'Grifur', 'M'), (1, 'Florimund', 'M'), (1, 'Humbert', 'M'), (1, 'Plešič', 'M'), (1, 'Bungo', 'M'), (1, 'Šalvěj', 'M'), (1, 'Lavendel', 'M'), (1, 'Záboj', 'M'), (1, 'Eufémie', 'F'), (1, 'Melichar', 'M'), (1, 'Růžena', 'F'), (1, 'Hvězdoň', 'M'), (1, 'Berenikla', 'F'), (1, 'Ignať', 'M'), (1, 'Rozinka', 'F'), (1, 'Žofka', 'F'), (1, 'Slavoboj', 'M'), (1, 'Safír', 'M'), (1, 'Myrtil', 'M'), (1, 'Rubín', 'M'), (1, 'Smaragd', 'M'), (1, 'Perla', 'F'), (1, 'Jantar', 'M'), (1, 'Žulík', 'M'), (1, 'Ambrož', 'M'), (1, 'Bratša', 'M'), (1, 'Jasmína', 'F'), (1, 'Meluzína', 'F'), (1, 'Laluna', 'F'), (1, 'Věneč', 'M'), (1, 'Řepník', 'M'), (1, 'Papo', 'M'), (1, 'Olek', 'M'), (1, 'Velina', 'F'), (1, 'Maruška', 'F'), (1, 'Bazil', 'M'), (1, 'Mazanec', 'M'), (1, 'Šej', 'M'), (1, 'Řepníček', 'M'), (1, 'Zvonk', 'M'), (1, 'Bůvka', 'F'), (1, 'Ovčík', 'M'), (1, 'Bouba', 'M'), (1, 'Pískavec', 'M'), (1, 'Svatozář', 'M'), (1, 'Třešňa', 'F'), (1, 'Višněnka', 'F'), (1, 'Lískovec', 'M'), (1, 'Švestka', 'F'), (1, 'Hroznýš', 'M'), (1, 'Pěnivec', 'M'), (1, 'Babor', 'M'), (1, 'Papoušek', 'M'), (1, 'Lýkovec', 'M'), (1, 'Oříšek', 'M'), (1, 'Béďa', 'M'), (1, 'Myrtilka', 'F'), (1, 'Norek', 'M'), (1, 'Pavouk', 'M'), (1, 'Čmelík', 'M'), (1, 'Sýček', 'M'), (1, 'Drobínek', 'M'), (1, 'Pliška', 'F'), (1, 'Korbel', 'M'), (1, 'Manka', 'F'), (1, 'Zrzek', 'M'), (1, 'Vrbovka', 'F'),  (1, 'Vikýř', 'M'), (1, 'Béda', 'M'), (1, 'Bouba', 'M'), (1, 'Fik', 'M'), (1, 'Bobík', 'M'),  (1, 'Hájek', 'M'), (1, 'Brčál', 'M'), (1, 'Mlžek', 'M'), (1, 'Bílek', 'M'), (1, 'Vřešťan', 'M'),
    (2, 'Drozd', 'M'), (2, 'Rudobor', 'M'), (2, 'Hilda', 'F'), (2, 'Pivoj', 'M'), (2, 'Pip', 'M'), (2, 'Bronislav', 'M'),(2, 'Brunhilda', 'F'), (2, 'Gisla', 'F'), (2, 'Hervor', 'F'), (2, 'Ida', 'F'), (2, 'Bertha', 'F'), (2, 'Sigrid', 'F'), (2, 'Hrodga', 'F'), (2, 'Alva', 'F'), (2, 'Frida', 'F'), (2, 'Astrid', 'F'), (2, 'Freya', 'F'), (2, 'Ingrid', 'F'), (2, 'Thora', 'F'), (2, 'Dagmar', 'F'), (2, 'Runa', 'F'), (2, 'Solveig', 'F'), (2, 'Yrsa', 'F'), (2, 'Gertrude', 'F'), (2, 'Olga', 'F'), (2, 'Elsa', 'F'), (2, 'Borghild', 'F'), (2, 'Ragnhild', 'F'), (2, 'Helga', 'F'), (2, 'Gunnvor', 'F'), (2, 'Tove', 'F'), (2, 'Hildegard', 'F'), (2, 'Solveig', 'F'), (2, 'Margit', 'F'), (2, 'Astrud', 'F'), (2, 'Liv', 'F'), (2, 'Edda', 'F'), (2, 'Sif', 'F'), (2, 'Gudrun', 'F'), (2, 'Hilda', 'F'), (2, 'Lotta', 'F'), (2, 'Marta', 'F'), (2, 'Svanhild', 'F'), (2, 'Synnove', 'F'), (2, 'Mette', 'F'), (2, 'Rosa', 'F'), (2, 'Birgit', 'F'), (2, 'Disa', 'F'), (2, 'Gunilla', 'F'), (2, 'Jorunn', 'F'), (2, 'Kirsten', 'F'), (2, 'Tora', 'F'), (2, 'Vigdis', 'F'), (2, 'Yrla', 'F'), (2, 'Eir', 'F'), (2, 'Kamínek', 'M'), (2, 'Horin', 'M'), (2, 'Záboj', 'M'), (2, 'Břetislav', 'M'), (2, 'Hvozdník', 'M'), (2, 'Kameník', 'M'), (2, 'Polev', 'M'), (2, 'Hradník', 'M'), (2, 'Borivoj', 'M'), (2, 'Střelovec', 'M'), (2, 'Železník', 'M'), (2, 'Borovík', 'M'), (2, 'Medvědík', 'M'), (2, 'Hvězdník', 'M'), (2, 'Pádivoj', 'M'), (2, 'Hvězdomír', 'M'), (2, 'Střemhlav', 'M'), (2, 'Tvrzislav', 'M'), (2, 'Kvíček', 'M'), (2, 'Drahoň', 'M'), (2, 'Kameníček', 'M'), (2, 'Skáli', 'M'), (2, 'Kvíli', 'M'), (2, 'Tráli', 'M'), (2, 'Hórin', 'M'), (2, 'Hugin', 'M'), (2, 'Mundin', 'M'), (2, 'Zlatomír', 'M'), (2, 'Korund', 'M'), (2, 'Sardonyx', 'M'), (2, 'Garmund', 'M'), (2, 'Náli', 'M'), (2, 'Hjálmar', 'M'), (2, 'Gundri', 'M'), (2, 'Lofar', 'M'), (2, 'Svílin', 'M'), (2, 'Járin', 'M'), (2, 'Beri', 'M'), (2, 'Dreki', 'M'), (2, 'Einar', 'M'), (2, 'Falr', 'M'), (2, 'Folkar', 'M'), (2, 'Gim', 'M'), (2, 'Gulli', 'M'), (2, 'Haustl', 'M'), (2, 'Kinni', 'M'), (2, 'Náli', 'M'), (2, 'Pósi', 'M'), (2, 'Tíli', 'M'), (2, 'Unni', 'M'), (2, 'Vallar', 'M'), (2, 'Vorli', 'M'), (2, 'Yngvi', 'M'), (2, 'Glóli', 'M'), (2, 'Djákn', 'M'), (2, 'Hjálmarr', 'M'), (2, 'Mánir', 'M'), (2, 'Otti', 'M'), (2, 'Ratni', 'M'), (2, 'Sigdi', 'M'), (2, 'Sveri', 'M'), (2, 'Tjalli', 'M'), (2, 'Vigg', 'M'), (2, 'Hergi', 'M'), (2, 'Stáni', 'M'), (2, 'Vindarr', 'M'), (2, 'Yngvarr', 'M'), (2, 'Fáfnir', 'M'), (2, 'Svarri', 'M'), (2, 'Haki', 'M'), (2, 'Ginnarr', 'M'), (2, 'Rauri', 'M'), (2, 'Géir', 'M'), (2, 'Bergi', 'M'), (2, 'Derr', 'M'), (2, 'Énarr', 'M'), (2, 'Frási', 'M'), (2, 'Védharr', 'M'), (2, 'Varr', 'M'), (2, 'Bjorni', 'M'), (2, 'Eirik', 'M'), (2, 'Harri', 'M'), (2, 'Ívaldi', 'M'), (2, 'Súri', 'M'), (2, 'Tonnar', 'M'), (2, 'Áni', 'M'), (2, 'Audi', 'M'), (2, 'Brokki', 'M'), (2, 'Dverri', 'M'), (2, 'Egill', 'M'), (2, 'Flosi', 'M'), (2, 'Grani', 'M'), (2, 'Heimir', 'M'), (2, 'Hildir', 'M'), (2, 'Hilmarr', 'M'), (2, 'Konnar', 'M'), (2, 'Lói', 'M'), (2, 'Móri', 'M'), (2, 'Rónarr', 'M'), (2, 'Róni', 'M'), (2, 'Stálfr', 'M'), (2, 'Steini', 'M'), (2, 'Súri', 'M'), (2, 'Tanni', 'M'), (2, 'Þráinn', 'M'), (2, 'Torfi', 'M'), (2, 'Vetrliði', 'M'), (2, 'Vilmarr', 'M'), (2, 'Yngvi', 'M'), (2, 'Þríarr', 'M'), (2, 'Álfarr', 'M'), (2, 'Ásmundr', 'M'), (2, 'Ásvaldr', 'M'), (2, 'Ávaldr', 'M'), (2, 'Óli', 'M'), (2, 'Óni', 'M'), (2, 'Bjarni', 'M'), (2, 'Bragi', 'M'), (2, 'Búi', 'M'), (2, 'Buni', 'M'), (2, 'Dellingr', 'M'), (2, 'Einarr', 'M'), (2, 'Eskil', 'M'), (2, 'Fáfnir', 'M'), (2, 'Finni', 'M'), (2, 'Geri', 'M'), (2, 'Grani', 'M'), (2, 'Grímr', 'M'), (2, 'Haddi', 'M'), (2, 'Hakon', 'M'), (2, 'Hanni', 'M'), (2, 'Helgi', 'M'), (2, 'Hilmarr', 'M'), (2, 'Hroarr', 'M'), (2, 'Illugi', 'M'), (2, 'Jöfur', 'M'), (2, 'Jói', 'M'), (2, 'Kári', 'M'), (2, 'Koli', 'M'), (2, 'Lambi', 'M'), (2, 'Leifr', 'M'), (2, 'Magni', 'M'), (2, 'Máni', 'M'), (2, 'Nari', 'M'), (2, 'Nóri', 'M'), (2, 'Oddi', 'M'), (2, 'Orrar', 'M'), (2, 'Rakki', 'M'), (2, 'Rikki', 'M'), (2, 'Rói', 'M'), (2, 'Rögnarr', 'M'), (2, 'Sindri', 'M'), (2, 'Skeggi', 'M'), (2, 'Sveinn', 'M'), (2, 'Talli', 'M'), (2, 'Tanni', 'M'), (2, 'Tóki', 'M'), (2, 'Tummi', 'M'), (2, 'Unni', 'M'), (2, 'Vali', 'M'), (2, 'Valli', 'M'), (2, 'Vani', 'M'), (2, 'Váli', 'M'), (2, 'Vigi', 'M'), (2, 'Vili', 'M'), (2, 'Vígi', 'M'), (2, 'Vári', 'M'),
    (3, 'Drobov', 'M'), (3, 'Hilda', 'F'), (3, 'Brumbur', 'M'), (3, 'Pipstein', 'M'), (3, 'Balinno', 'M'), (3, 'Pípon', 'M'), (3, 'Hrabišek', 'M'), (3, 'Droběna', 'F'), (3, 'Rudi', 'M'), (3, 'Lílina', 'F'), (3, 'Fritzi', 'F'), (3, 'Tobi', 'M'), (3, 'Cipísek', 'M'), (3, 'Bětuška', 'F'), (3, 'Vendelín', 'M'), (3, 'Bělka', 'F'), (3, 'Žaneta', 'F'), (3, 'Fíb', 'M'), (3, 'Gilda', 'F'), (3, 'Nela', 'F'), (3, 'Kvído', 'M'), (3, 'Aldina', 'F'), (3, 'Tynka', 'F'), (3, 'Lena', 'F'), (3, 'Milada', 'F'), (3, 'Sera', 'F'), (3, 'Tříska', 'M'), (3, 'Liána', 'F'), (3, 'Melina', 'F'), (3, 'Nina', 'F'), (3, 'Ludek', 'M'), (3, 'Kubi', 'M'), (3, 'Lela', 'F'), (3, 'Vilma', 'F'), (3, 'Šárka', 'F'), (3, 'Rosi', 'F'), (3, 'Arni', 'M'), (3, 'Gita', 'F'), (3, 'Ela', 'F'), (3, 'Kvido', 'M'), (3, 'Bora', 'F'), (3, 'Oto', 'M'), (3, 'Dora', 'F'), (3, 'Erik', 'M'), (3, 'Leo', 'M'), (3, 'Kori', 'F'), (3, 'Jura', 'M'), (3, 'Fany', 'F'), (3, 'Zeta', 'F'), (3, 'Bobo', 'M'), (3, 'Drobíš', 'M'), (3, 'Bramir', 'M'), (3, 'Hobran', 'M'), (3, 'Rúmik', 'M'), (3, 'Piposlav', 'M'), (3, 'Borohobit', 'M'), (3, 'Kuloslav', 'M'), (3, 'Drobpír', 'M'), (3, 'Hobír', 'M'), (3, 'Boromír', 'M'), (3, 'Pipomír', 'M'), (3, 'Korúnd', 'M'), (3, 'Kudrak', 'M'), (3, 'Boropír', 'M'), (3, 'Pipobor', 'M'), (3, 'Kudrobor', 'M'), (3, 'Droboš', 'M'), (3, 'Pipolín', 'M'), (3, 'Hobrad', 'M'), (3, 'Branomír', 'M'), (3, 'Dropip', 'M'), (3, 'Kudrán', 'M'), (3, 'Hobran', 'M'), (3, 'Pipír', 'M'), (3, 'Borobír', 'M'), (3, 'Drobík', 'M'), (3, 'Pipran', 'M'), (3, 'Hobrok', 'M'), (3, 'Borobík', 'M'), (3, 'Kudrán', 'M'), (3, 'Drobík', 'M'), (3, 'Pipřík', 'M'), (3, 'Hobroš', 'M'), (3, 'Borodrán', 'M'),(3, 'Drobov', 'M'), (3, 'Pipol', 'M'),
    (4, 'Aelarion', 'M'), (4, 'Elorian', 'M'), (4, 'Thalassion', 'M'), (4, 'Amarael', 'M'), (4, 'Caladwen', 'F'), (4, 'Thalendir', 'M'), (4, 'Elarian', 'M'), (4, 'Liriel', 'F'), (4, 'Eldamar', 'M'), (4, 'Nimrodel', 'F'), (4, 'Aralin', 'M'), (4, 'Eärlindë', 'F'), (4, 'Amarië', 'F'), (4, 'Finduilas', 'F'), (4, 'Galdor', 'M'), (4, 'Melian', 'F'), (4, 'Voronwë', 'M'), (4, 'Ecthelion', 'M'), (4, 'Glaurung', 'M'), (4, 'Ingwë', 'M'), (4, 'Nerdanel', 'F'), (4, 'Turgon', 'M'), (4, 'Varda', 'F'), (4, 'Lithiriel', 'F'), (4, 'Aranion', 'M'), (4, 'Eladan', 'M'), (4, 'Maeglin', 'M'), (4, 'Thalion', 'M'), (4, 'Ardalambion', 'M'), (4, 'Eärlas', 'M'), (4, 'Lindir', 'M'), (4, 'Nerwen', 'F'), (4, 'Aranion', 'M'), (4, 'Galathir', 'M'), (4, 'Melian', 'F'), (4, 'Tharandil', 'M'), (4, 'Aldaron', 'M'), (4, 'Tári', 'F'), (4, 'Eärendur', 'M'), (4, 'Melian', 'F'), (4, 'Alqualondë', 'M'), (4, 'Eldor', 'M'), (4, 'Noldorin', 'M'), (4, 'Telmarin', 'M'), (4, 'Aegnor', 'M'),
    (5, 'Rupert', 'M'), (5, 'Fosir', 'M'), (5, 'Lezar', 'M'), (5, 'Olga', 'F'), (5, 'Dalimír', 'M'), (5, 'Jasna', 'F'), (5, 'Ruměna', 'F'), (5, 'Tarlon', 'M'), (5, 'Živana', 'F'), (5, 'Míroš', 'M'), (5, 'Velena', 'F'), (5, 'Milora', 'F'), (5, 'Staniš', 'M'), (5, 'Zlatana', 'F'), (5, 'Jasan', 'M'), (5, 'Lumíra', 'F'), (5, 'Borimir', 'M'), (5, 'Radmila', 'F'), (5, 'Davor', 'M'), (5, 'Slavena', 'F'), (5, 'Lesmir', 'M'), (5, 'Plamenor', 'M'), (5, 'Duboslav', 'M'), (5, 'Jitroslav', 'M'), (5, 'Hvězdor', 'M'), (5, 'Vlnislav', 'M'), (5, 'Kamínek', 'M'), (5, 'Vítrvan', 'M'), (5, 'Skalomír', 'M'), (5, 'Láskorad', 'M'), (5, 'Zemomír', 'M'), (5, 'Tichomil', 'M'), (5, 'Drakoslav', 'M'), (5, 'Vodomil', 'M'), (5, 'Dobrovoj', 'M'), (5, 'Kamenor', 'M'), (5, 'Srdan', 'M'), (5, 'Stromír', 'M'), (5, 'Hvozdomir', 'M'), (5, 'Tichomír', 'M'), (5, 'Zlatomil', 'M'), (5, 'Lísteček', 'M'), (5, 'Zlatovoj', 'M'), (5, 'Čaroslav', 'M'), (5, 'Jitromir', 'M'), (5, 'Jasohled', 'M'), (5, 'Bystrík', 'M'), (5, 'Dobromir', 'M'), (5, 'Radoslav', 'M'), (5, 'Štítoslav', 'M'), (5, 'Čestmír', 'M'), (5, 'Blahoslav', 'M'), (5, 'Pravoslav', 'M'), (5, 'Ladislav', 'M'), (5, 'Přemysl', 'M'), (5, 'Radomír', 'M'), (5, 'Želmír', 'M'), (5, 'Ludivoj', 'M'), (5, 'Vojan', 'M'), (5, 'Jarohled', 'M'), (5, 'Jarovoj', 'M'), (5, 'Světoslav', 'M'), (5, 'Bohdan', 'M'), (5, 'Slavoš', 'M'), (5, 'Pravomil', 'M'), (5, 'Mračislav', 'M'), (5, 'Tajemir', 'M'), (5, 'Krasomír', 'M'),
    (6, 'Conan', 'M'), (6, 'Kull', 'M'), (6, 'Sonja', 'F'), (6, 'Bran Mak Morn', 'M'), (6, 'Lišaj', 'M'),  (6, 'Sár Buh Salak', 'F'), (6, 'Thorgal', 'M'), (6, 'Freydis', 'F'), (6, 'Hagen', 'M'), (6, 'Brynhild', 'F'), (6, 'Ragnar', 'M'), (6, 'Sif', 'F'), (6, 'Eirik', 'M'), (6, 'Gudrun', 'F'), (6, 'Hrolf', 'M'), (6, 'Astrid', 'F'), (6, 'Vigdis', 'F'), (6, 'Bjorn', 'M'), (6, 'Helga', 'F'), (6, 'Skadi', 'F'), (6, 'Gorm', 'M'), (6, 'Runa', 'F'), (6, 'Thorvald', 'M'), (6, 'Inga', 'F'), (6, 'Baldur', 'M'), (6, 'Freya', 'F'), (6, 'Olaf', 'M'), (6, 'Kara', 'F'), (6, 'Sigurd', 'M'), (6, 'Ylva', 'F'), (6, 'Ulf', 'M'), (6, 'Sigrun', 'F'), (6, 'Rolf', 'M'), (6, 'Thora', 'F'), (6, 'Ivar', 'M'), (6, 'Saga', 'F'), (6, 'Starkad', 'M'), (6, 'Ragnhild', 'F'), (6, 'Hakon', 'M'), (6, 'Ingeborg', 'F'), (6, 'Asmund', 'M'), (6, 'Ragnvald', 'M'), (6, 'Torstein', 'M'), (6, 'Skogul', 'F'), (6, 'Haldor', 'M'), (6, 'Viggo', 'M'), (6, 'Hertha', 'F'), (6, 'Styr', 'M'), (6, 'Birna', 'F'), (6, 'Arne', 'M'), (6, 'Gunnar', 'M'),
    (7, 'Groo', 'M'), (7, 'Brom', 'M'), (7, 'Grok', 'M'), (7, 'Gragu', 'M'), (7, 'Kámen', 'M'), (7, 'Kamena', 'F'), (7, 'Thrak', 'M'), (7, 'Zog', 'M'), (7, 'Ursa', 'F'), (7, 'Drak', 'M'), (7, 'Krog', 'M'), (7, 'Vrog', 'M'), (7, 'Mog', 'M'), (7, 'Zara', 'F'), (7, 'Narg', 'M'), (7, 'Borg', 'M'), (7, 'Garn', 'M'), (7, 'Urg', 'M'), (7, 'Tharg', 'M'), (7, 'Orga', 'F'), (7, 'Rorg', 'M'), (7, 'Grog', 'M'), (7, 'Kragg', 'M'), (7, 'Draga', 'F'), (7, 'Krag', 'M'), (7, 'Zug', 'M'), (7, 'Org', 'M'), (7, 'Throg', 'M'), (7, 'Frog', 'M'), (7, 'Trog', 'M'), (7, 'Grim', 'M'), (7, 'Naga', 'F'), (7, 'Rug', 'M'), (7, 'Zog', 'M'), (7, 'Krog', 'M'), (7, 'Gnak', 'M'), (7, 'Dran', 'M'), (7, 'Urg', 'M'), (7, 'Zug', 'M'), (7, 'Thug', 'M'), (7, 'Mora', 'F'), (7, 'Trak', 'M'), (7, 'Urla', 'F'), (7, 'Grush', 'M'), (7, 'Murg', 'M'), (7, 'Brak', 'M'), (7, 'Goth', 'M'), (7, 'Fang', 'M'), (7, 'Krogath', 'M'), (7, 'Thrag', 'M'), (7, 'Brak', 'M'), (7, 'Zara', 'F')
]
cursor.executemany('INSERT INTO names (race_id, name, gender) VALUES (?, ?, ?)', names)

# Example stat ranges for different race/class combinations
stat_ranges = [
    # Hobit
    (1, 1, 'Síla', 8, 13), (1, 2, 'Síla', 6, 11), (1, 3, 'Síla', 3, 8), (1, 4, 'Síla', 3, 8), (1, 5, 'Síla', 3, 8),
    (1, 1, 'Obratnost', 11, 16), (1, 2, 'Obratnost', 11, 16), (1, 3, 'Obratnost', 15, 20), (1, 4, 'Obratnost', 11, 16), (1, 5, 'Obratnost', 16, 21),
    (1, 1, 'Odolnost', 13, 18), (1, 2, 'Odolnost', 8, 13), (1, 3, 'Odolnost', 12, 17), (1, 4, 'Odolnost', 8, 13), (1, 5, 'Odolnost', 8, 13),
    (1, 1, 'Inteligence', 10, 15), (1, 2, 'Inteligence', 10, 15), (1, 3, 'Inteligence', 10, 15), (1, 4, 'Inteligence', 12, 17), (1, 5, 'Inteligence', 10, 15),
    (1, 1, 'Charisma', 8, 18), (1, 2, 'Charisma', 8, 18), (1, 3, 'Charisma', 8, 18), (1, 4, 'Charisma', 16, 21), (1, 5, 'Charisma', 15, 20),

    # Kudůk
    (2, 1, 'Síla', 10, 15), (2, 2, 'Síla', 8, 13), (2, 3, 'Síla', 6, 16), (2, 4, 'Síla', 6, 16), (2, 5, 'Síla', 6, 16),
    (2, 1, 'Obratnost', 9, 14), (2, 2, 'Obratnost', 9, 14), (2, 3, 'Obratnost', 14, 19), (2, 4, 'Obratnost', 9, 14), (2, 5, 'Obratnost', 15, 20),
    (2, 1, 'Odolnost', 14, 19), (2, 2, 'Odolnost', 9, 14), (2, 3, 'Odolnost', 13, 18), (2, 4, 'Odolnost', 9, 14), (2, 5, 'Odolnost', 9, 14),
    (2, 1, 'Inteligence', 10, 15), (2, 2, 'Inteligence', 10, 15), (2, 3, 'Inteligence', 10, 15), (2, 4, 'Inteligence', 12, 17), (2, 5, 'Inteligence', 10, 15),
    (2, 1, 'Charisma', 2, 17), (2, 2, 'Charisma', 2, 17), (2, 3, 'Charisma', 2, 17), (2, 4, 'Charisma', 13, 18), (2, 5, 'Charisma', 12, 17),

    # Trpaslík
    (3, 1, 'Síla', 14, 19), (3, 2, 'Síla', 12, 17), (3, 3, 'Síla', 6, 16), (3, 4, 'Síla', 6, 16), (3, 5, 'Síla', 6, 16),
    (3, 1, 'Obratnost', 9, 14), (3, 2, 'Obratnost', 9, 14), (3, 3, 'Obratnost', 11, 16), (3, 4, 'Obratnost', 9, 14), (3, 5, 'Obratnost', 12, 17),
    (3, 1, 'Odolnost', 16, 21), (3, 2, 'Odolnost', 9, 14), (3, 3, 'Odolnost', 15, 20), (3, 4, 'Odolnost', 9, 14), (3, 5, 'Odolnost', 9, 14),
    (3, 1, 'Inteligence', 10, 15), (3, 2, 'Inteligence', 9, 14), (3, 3, 'Inteligence', 10, 15), (3, 4, 'Inteligence', 11, 16), (3, 5, 'Inteligence', 10, 15),
    (3, 1, 'Charisma', 2, 17), (3, 2, 'Charisma', 2, 17), (3, 3, 'Charisma', 2, 17), (3, 4, 'Charisma', 11, 16), (3, 5, 'Charisma', 10, 15),

    # Elf
    (4, 1, 'Síla', 13, 18), (4, 2, 'Síla', 11, 16), (4, 3, 'Síla', 6, 16), (4, 4, 'Síla', 6, 16), (4, 5, 'Síla', 6, 16),
    (4, 1, 'Obratnost', 9, 14), (4, 2, 'Obratnost', 9, 14), (4, 3, 'Obratnost', 14, 19), (4, 4, 'Obratnost', 9, 14), (4, 5, 'Obratnost', 15, 20),
    (4, 1, 'Odolnost', 9, 14), (4, 2, 'Odolnost', 9, 14), (4, 3, 'Odolnost', 8, 13), (4, 4, 'Odolnost', 9, 14), (4, 5, 'Odolnost', 9, 14),
    (4, 1, 'Inteligence', 10, 15), (4, 2, 'Inteligence', 14, 19), (4, 3, 'Inteligence', 10, 15), (4, 4, 'Inteligence', 16, 21), (4, 5, 'Inteligence', 10, 15),
    (4, 1, 'Charisma', 2, 17), (4, 2, 'Charisma', 2, 17), (4, 3, 'Charisma', 2, 17), (4, 4, 'Charisma', 15, 20), (4, 5, 'Charisma', 14, 19),

    # Člověk
    (5, 1, 'Síla', 13, 18), (5, 2, 'Síla', 11, 16), (5, 3, 'Síla', 6, 16), (5, 4, 'Síla', 6, 16), (5, 5, 'Síla', 6, 16),
    (5, 1, 'Obratnost', 9, 14), (5, 2, 'Obratnost', 9, 14), (5, 3, 'Obratnost', 3, 18), (5, 4, 'Obratnost', 9, 14), (5, 5, 'Obratnost', 14, 19),
    (5, 1, 'Odolnost', 13, 18), (5, 2, 'Odolnost', 9, 14), (5, 3, 'Odolnost', 12, 17), (5, 4, 'Odolnost', 9, 14), (5, 5, 'Odolnost', 9, 14),
    (5, 1, 'Inteligence', 10, 15), (5, 2, 'Inteligence', 12, 17), (5, 3, 'Inteligence', 10, 15), (5, 4, 'Inteligence', 10, 15), (5, 5, 'Inteligence', 10, 15),
    (5, 1, 'Charisma', 2, 17), (5, 2, 'Charisma', 2, 17), (5, 3, 'Charisma', 2, 17), (5, 4, 'Charisma', 13, 18), (5, 5, 'Charisma', 12, 17),

    # Barbar
    (6, 1, 'Síla', 14, 19), (6, 2, 'Síla', 12, 17), (6, 3, 'Síla', 6, 16), (6, 4, 'Síla', 6, 16), (6, 5, 'Síla', 6, 16),
    (6, 1, 'Obratnost', 9, 14), (6, 2, 'Obratnost', 9, 14), (6, 3, 'Obratnost', 12, 17), (6, 4, 'Obratnost', 9, 14), (6, 5, 'Obratnost', 13, 18),
    (6, 1, 'Odolnost', 14, 19), (6, 2, 'Odolnost', 9, 14), (6, 3, 'Odolnost', 13, 18), (6, 4, 'Odolnost', 9, 14), (6, 5, 'Odolnost', 9, 14),
    (6, 1, 'Inteligence', 10, 15), (6, 2, 'Inteligence', 12, 17), (6, 3, 'Inteligence', 10, 15), (6, 4, 'Inteligence', 14, 19), (6, 5, 'Inteligence', 10, 15),
    (6, 1, 'Charisma', 2, 17), (6, 2, 'Charisma', 2, 17), (6, 3, 'Charisma', 2, 17), (6, 4, 'Charisma', 11, 16), (6, 5, 'Charisma', 10, 15),

    # Kroll
    (7, 1, 'Síla', 16, 21), (7, 2, 'Síla', 14, 19), (7, 3, 'Síla', 6, 16), (7, 4, 'Síla', 6, 16), (7, 5, 'Síla', 6, 16),
    (7, 1, 'Obratnost', 9, 14), (7, 2, 'Obratnost', 9, 14), (7, 3, 'Obratnost', 9, 14), (7, 4, 'Obratnost', 9, 14), (7, 5, 'Obratnost', 10, 15),
    (7, 1, 'Odolnost', 16, 21), (7, 2, 'Odolnost', 9, 14), (7, 3, 'Odolnost', 15, 20), (7, 4, 'Odolnost', 9, 14), (7, 5, 'Odolnost', 9, 14),
    (7, 1, 'Inteligence', 10, 15), (7, 2, 'Inteligence', 6, 11), (7, 3, 'Inteligence', 10, 15), (7, 4, 'Inteligence', 8, 13), (7, 5, 'Inteligence', 10, 15),
    (7, 1, 'Charisma', 2, 17), (7, 2, 'Charisma', 2, 17), (7, 3, 'Charisma', 2, 17), (7, 4, 'Charisma', 8, 13), (7, 5, 'Charisma', 7, 12),
]

cursor.executemany('INSERT INTO stat_ranges (race_id, class_id, stat, min_value, max_value) VALUES (?, ?, ?, ?, ?)', stat_ranges)


print("Database operations completed successfully.")

# Commit changes and close the connection
conn.commit()
conn.close()
