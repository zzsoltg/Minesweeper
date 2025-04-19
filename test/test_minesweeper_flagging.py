import pytest
import src.minesweeper as minesweeper

def test_display_uncovered_field(capsys):
    """
    Egy egyszerű 4*4-es aknakereső játéktáblával teszteli a display_uncovered_field() működését.

    A capsys fixture segítségével megnézi a függvény kiírt értékét, majd azt elmenti.
    Ezután összehasonlítja az elvárt értékkel, amit soronként adunk meg, majd azt listába rendezzük.
    """
    field = [
        ["0", "0", "0", "0"],
        ["0", "1", "1", "1"],
        ["1", "2", "X", "1"],
        ["X", "2", "1", "1"]
    ]

    uncovered = [
        ["R", "U", "U", "U"],
        ["U", "R", "U", "U"],
        ["R", "R", "F", "U"],
        ["U", "R", "U", "U"]
    ]

    minesweeper.display_uncovered_field(field, uncovered)
    captured = capsys.readouterr().out.splitlines()

    header_expected = "   " + "  ".join(str(j) for j in range(len(field[0])))
    row0_expected = "0".ljust(3) + "0".ljust(3) + "   " + "   " + "   "
    row1_expected = "1".ljust(3) + "   " + "1".ljust(3) + "   " + "   "
    row2_expected = "2".ljust(3) + "1".ljust(3) + "2".ljust(3) + "F".ljust(3) + "   "
    row3_expected = "3".ljust(3) + "   " + "2".ljust(3) + "   " + "   "

    expected_output = [header_expected, row0_expected, row1_expected, row2_expected, row3_expected]

    assert captured == expected_output


def test_flag_addition(monkeypatch):
    """
    Egy egyszerű 4*4-es aknakereső játéktáblával teszteli a get_user_move() működését.

    A monkeypatch fixture segítségével a 3 inputra egy flag hozzáadásához szükséges parancsokat ad.
    Majd teszteli, hogy a függvény az ezekre elvárt kimenetet adja-e meg.
    """
    inputs = iter([
        "flag",
        "1",
        "2 3"
    ])

    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    result = minesweeper.get_user_move(4, 4)

    assert result == (1, 2, 3)


def test_flag_removal(monkeypatch):
    """
    Egy egyszerű 4*4-es aknakereső játéktáblával teszteli a get_user_move() működését.

    A monkeypatch fixture segítségével a 3 inputra egy flag eltávolításához szükséges parancsokat ad.
    Majd teszteli, hogy a függvény az ezekre elvárt kimenetet adja-e meg.
    """
    inputs = iter([
        "flag",
        "2",
        "0 1"
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    result = minesweeper.get_user_move(4, 4)
    assert result == (2, 0, 1)


def test_flag_invalid_then_valid(monkeypatch):
    """
    Egy egyszerű 4*4-es aknakereső játéktáblával teszteli a get_user_move() működését.

    A monkeypatch fixture segítségével a 3 inputra egy flag eltávolításához szükséges parancsokat ad.
    Előtte hibás parancsot ad a flag commandra.
    Majd teszteli, hogy a függvény az ezekre elvárt kimenetet adja-e meg.
    """
    inputs = iter([
        "flag",
        "3",
        "2",
        "1 2"
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    result = minesweeper.get_user_move(4, 4)
    assert result == (2, 1, 2)

def test_check_win_condition_false():
    """
    Egy egyszerű 4*4-es aknakereső játéktáblával teszteli a check_win_condition() működését.

    A tesztesetben nem minden mező került felfedésre, ami nem tartalmaz aknát, tehát a függvénynek
    false értékkel kell visszatérnie.
    """
    field = [
        ["0", "0", "0", "0"],
        ["0", "1", "1", "1"],
        ["1", "2", "X", "1"],
        ["X", "2", "1", "1"]
    ]

    uncovered = [
        ["R", "U", "U", "U"],
        ["U", "R", "U", "U"],
        ["R", "R", "F", "U"],
        ["U", "R", "U", "U"]
    ]

    assert minesweeper.check_win_condition(field, uncovered) == False

def test_check_win_condition_true():
    """
    Egy egyszerű 4*4-es aknakereső játéktáblával teszteli a check_win_condition() működését.

    A tesztesetben nem minden mező került felfedésre, ami nem tartalmaz aknát, tehát a függvénynek
    false értékkel kell visszatérnie.

    Felfedezett hibák: a kódban egy feltétel hibásan volt megadva (188. sor)
    """
    field = [
        ["0", "0", "0", "0"],
        ["0", "1", "1", "1"],
        ["1", "2", "X", "1"],
        ["X", "2", "1", "1"]
    ]

    uncovered = [
        ["R", "R", "R", "R"],
        ["R", "R", "R", "R"],
        ["R", "R", "U", "R"],
        ["U", "R", "R", "R"]
    ]

    assert minesweeper.check_win_condition(field, uncovered) == True


def test_reveal_all():
    uncovered = [
        ["R", "U", "U", "U"],
        ["U", "R", "U", "U"],
        ["R", "R", "F", "U"],
        ["U", "R", "U", "U"]
    ]

    expected = [
        ["R", "R", "R", "R"],
        ["R", "R", "R", "R"],
        ["R", "R", "R", "R"],
        ["R", "R", "R", "R"]
    ]

    minesweeper.reveal_all(uncovered)

    assert uncovered == expected