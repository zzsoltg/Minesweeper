import random
import copy


def create_playing_field():
    """
    Létrehozza az aknakereső játék játéktábláját.

    Ez a függvény egy 21x12-es rácsot hoz létre, melynek minden cellája "0" (sztringként) van inicializálva,
    majd véletlenszerűen elhelyez 40 aknát (amelyeket "X" jelöl).

    Visszatérési érték:
        list: A játéktáblát reprezentáló kétdimenziós lista.
    """
    mines = 40
    playing_field = []

    # Hozzunk létre egy üres 21x12-es rácsot, melynek minden eleme "0"
    for i in range(21):
        field_line = ["0"] * 12  # Lista szorzással egy sor 12 "0"-ból
        playing_field.append(field_line)

    # Véletlenszerűen helyezzünk el 40 aknát ("X") a rácsban
    for _ in range(mines):
        while True:
            rand_i = random.randint(0, 20)  # Véletlenszerű sorindex 0 és 20 között
            rand_j = random.randint(0, 11)  # Véletlenszerű oszlopindex 0 és 11 között
            if playing_field[rand_i][rand_j] == "0":
                playing_field[rand_i][rand_j] = "X"
                break

    return playing_field


def calculate_numbers(field):
    """
    Kiszámolja az aknák számát minden nem-akna cella esetében a játéktáblán.

    Minden olyan cella esetében, amely nem tartalmaz aknát ("X"), a függvény megszámolja,
    hogy a cella nyolc szomszédos cellájában (átlós, függőleges és vízszintes irányban) hány akna található,
    és a "0" helyére a számlálás eredményét (sztringként) írja.

    Paraméter:
        field (list): Egy kétdimenziós lista, amely a játéktáblát ábrázolja; az üres cellákat "0", az aknákat "X" jelöli.

    Visszatérési érték:
        list: Egy új kétdimenziós lista, ahol a nem-akna cellákat a hozzájuk tartozó aknaszámokkal (sztringként)
              helyettesítjük, míg az aknákat tartalmazó cellák változatlanok maradnak.
    """
    rows = len(field)
    cols = len(field[0])
    new_field = []

    for i in range(rows):
        new_row = []
        for j in range(cols):
            # Ha az aktuális cella akna, marad "X"
            if field[i][j] == "X":
                new_row.append("X")
            else:
                count = 0
                # Vizsgáljuk meg a 8 szomszédos cellát
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di == 0 and dj == 0:
                            continue  # Kihagyjuk a cellát maga
                        ni, nj = i + di, j + dj
                        # Ellenőrizzük, hogy a szomszédos indexek a rács határain belül vannak-e
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if field[ni][nj] == "X":
                                count += 1
                new_row.append(str(count))
        new_field.append(new_row)
    return new_field


def display_playing_field_all(field):
    """
    Megjeleníti a teljes játéktáblát formázott módon.

    A függvény az oszlopok számait a tetején, a sorok számait pedig a bal oldalon jeleníti meg,
    és minden cellát mutat, függetlenül attól, hogy azokat felfedték-e már.

    Paraméter:
        field (list): A játéktáblát reprezentáló kétdimenziós lista.
    """
    header = "   " + "  ".join(str(j) for j in range(len(field[0])))
    print(header)
    for i in range(len(field)):
        # A sor számát bal oldalon jelenítjük meg, majd a cellák értékeit
        print(str(i).ljust(3) + "  ".join(field[i]))


def display_uncovered_field(field, uncovered):
    """
    Megjeleníti a játéktáblát úgy, hogy csak a felfedett cellák láthatóak.

    Minden cella esetében, ha az 'uncovered' rács szerint felfedett (R),
    annak értéke jelenik meg; ha flaggelt (F), akkor F,
    ha nem felfedett (U), akkor üres helyet mutat.

    Paraméterek:
        field (list): A játéktáblát reprezentáló kétdimenziós lista (aknák és számok).
        uncovered (list): Egy kétdimenziós lista, mely U, R, F betűkkel jelzi, hogy a mező milyen állapotban van.
    """
    header = "   " + "  ".join(str(j) for j in range(len(field[0])))
    print(header)
    for i in range(len(field)):
        row_str = str(i).ljust(3)
        for j in range(len(field[0])):
            if uncovered[i][j] == "R":
                row_str += field[i][j].ljust(3)
            elif uncovered[i][j] == "F":
                row_str += "F".ljust(3)
            else:
                row_str += "   "  # Három szóköz a fedett cellák helyére
        print(row_str)


def get_user_move(rows, cols):
    """
    Kéri a felhasználótól egy érvényes lépés megadását (sor, oszlop), amely a tábla határain belül van.
    A flag parancs megadásával van lehetőség flagek megadására.
    Az undo parancs megadásával lehetőség van az utolsó lépés visszavonására

    A függvény kezeli a hibás bemeneteket, és biztosítja, hogy a megadott koordináták két egész szám,
    a megfelelő tartományban legyenek.

    Paraméterek:
        rows (int): A játéktábla sorainak száma.
        cols (int): A játéktábla oszlopainak száma.

    Visszatérési érték:
        tuple: Egy (flag, sor, oszlop) értéket tartalmazó tuple, amely a felhasználó által választott
        koordinátákat jelzi, illetve, hogy történt-e flagging vagy undo művelet.
    """
    while True:
        print("Parancsok: flag - flaggelés; undo - visszavonás")
        user_input = input("Add meg a felfedendő cella sorát és oszlopát (szóközzel elválasztva) vagy egy parancsot: ")
        flagging = 0
        if user_input == "flag":
            while True:
                flagging = input("Add meg, hogy új flaget szeretnél hozzáadni (1) vagy eltávolítani egy meglévőt (2)! ")
                if flagging != "1" and flagging != "2":
                    print("Kérlek 1-essel vagy 2-essel válaszolj!")
                    continue
                flagging = int(flagging)
                break
            user_input = input("Add meg a flaggelni kívánt cella sorát és oszlopát (szóközzel elválasztva): ")
        parts = user_input.split()
        if len(parts) != 2:
            print("Kérlek, pontosan két számot adj meg, szóközzel elválasztva, vagy egy megfelelő parancsot!")
            continue
        try:
            row = int(parts[0])
            col = int(parts[1])
        except ValueError:
            print("Hibás bemenet. Egész számokat adj meg.")
            continue
        if not (0 <= row < rows and 0 <= col < cols):
            print("A megadott koordináták kívül esnek a tábla határain. Próbáld újra.")
            continue
        if flagging == 1:
            return 1, row, col
        elif flagging == 2:
            return 2, row, col
        return 0, row, col


def check_win_condition(field, uncovered):
    """
    Ellenőrzi, hogy minden nem-akna cella felfedésre került-e.

    Paraméterek:
        field (list): A játéktáblát reprezentáló kétdimenziós lista.
        uncovered (list): uncovered (list): Egy kétdimenziós lista, mely U, R, F betűkkel jelzi,
        hogy a mező milyen állapotban van.

    Visszatérési érték:
        bool: Igaz, ha minden biztonságos (nem-akna) cella felfedésre került, egyébként Hamis.
    """
    rows = len(field)
    cols = len(field[0])
    for i in range(rows):
        for j in range(cols):
            if field[i][j] != "X" and (uncovered[i][j] == "U" or uncovered[i][j] != "F"):
                return False
    return True


def reveal_all(uncovered):
    """
    Felfedi az összes cellát.

    Ez a függvény módosítja az 'uncovered' rácsot úgy, hogy minden cella felfedettnek legyen jelölve.

    Paraméter:
        uncovered (list): uncovered (list): Egy kétdimenziós lista, mely U, R, F betűkkel jelzi,
        hogy a mező milyen állapotban van.
    """
    for i in range(len(uncovered)):
        for j in range(len(uncovered[0])):
            uncovered[i][j] = "R"


def game_loop(numbered_field):
    """
    A fő játékmeneti ciklus, amely kezeli a lépéseket, frissíti a játék állapotát,
    és megjeleníti a játéktáblát.

    A ciklus addig kéri a felhasználótól a lépéseket, amíg egy akna felfedésre nem kerül (veszteség),
    vagy az összes biztonságos cella felfedésre kerül (győzelem).

    Paraméter:
        numbered_field (list): A játéktáblát reprezentáló kétdimenziós lista, mely aknákat és számokat tartalmaz.
    """
    rows = len(numbered_field)
    columns = len(numbered_field[0])
    # Létrehozunk egy rácsot, amely jelzi, mely cellák lettek felfedve (kezdetben minden hamis)
    uncovered = [["U" for _ in range(columns)] for _ in range(rows)]

    while True:
        display_uncovered_field(numbered_field, uncovered)
        flagging, row, col = get_user_move(rows, columns)

        if uncovered[row][col] == "R":
            print("Ez a cella már fel van fedve. Válassz egy másikat!")
            continue

        if flagging == 1:
            if uncovered[row][col] == "F":
                print("Ez a cella már flaggelve van. Válassz másikat!")
                continue
            uncovered[row][col] = "F"
            continue

        if flagging == 2:
            if uncovered[row][col] != "F":
                print("Ez a cella nincs flaggelve. Válassz másikat!")
                continue
            else:
                uncovered[row][col] = "U"
                continue

        if uncovered[row][col] == "F":
            while True:
                sure = input("Ezt a mezőt korábban flaggelted. Biztosan fel akarod fedni? I/N ")
                if sure == "I":
                    break
                elif sure == "N":
                    break
                else:
                    print("Kérlek I-vel vagy N-nel válaszolj!")
            if sure == "N":
                continue

        # Felfedjük a kiválasztott cellát
        uncovered[row][col] = "R"

        # Ellenőrizzük, hogy a felfedett cella akna-e
        if numbered_field[row][col] == "X":
            print("Bumm! Aknára léptünk. Vége a játéknak!")
            reveal_all(uncovered)
            display_uncovered_field(numbered_field, uncovered)
            break

        # Ellenőrizzük, hogy minden biztonságos cella felfedésre került-e (győzelmi feltétel)
        if check_win_condition(numbered_field, uncovered):
            print("Gratulálok! Minden biztonságos cellát felfedtél!")
            display_uncovered_field(numbered_field, uncovered)
            break


def main():
    """
    Fő függvény, amely inicializálja a játéktáblát és elindítja a játékmenetet.
    """
    # Létrehozzuk a játéktáblát és kiszámoljuk az egyes cellák mellett lévő aknák számát
    playing_field = create_playing_field()
    numbered_field = calculate_numbers(playing_field)

    print("Üdvözlünk az Akna-kereső játékban!")
    game_loop(numbered_field)


if __name__ == "__main__":
    main()
