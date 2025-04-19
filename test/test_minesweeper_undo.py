import pytest
import src.minesweeper as minesweeper

def test_get_user_move(monkeypatch):
    """
    Teszteli a get_user_move() függvényben, hogy felismeri-e az undo parancsot
    """
    monkeypatch.setattr("builtins.input", lambda prompt="": "undo")
    result = minesweeper.get_user_move(4, 4)
    assert result == (-1, -1, -1)


def test_get_user_move_undo_after_invalid_input(monkeypatch):
    """
    Teszteli, hogy a get_user_move() függvényben egy hibás bemenet után felismeri-e az undo parancsot.
    """
    inputs = iter(["asdf", "undo"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    result = minesweeper.get_user_move(4, 4)
    assert result == (-1, -1, -1)


def test_game_loop_undo(monkeypatch, capsys):
    """
    Teszteli, hogy a game_loop() függvényben működik-e az undo parancs.
    """

    numbered_field = [
        [1, "X"],
        [1, 1]
    ]

    inputs = iter(["0 0", "undo", "0 1"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    monkeypatch.setattr(minesweeper, "display_uncovered_field", lambda nf, uncovered: None)
    monkeypatch.setattr(minesweeper, "reveal_all", lambda uncovered: None)
    monkeypatch.setattr(minesweeper, "check_win_condition", lambda nf, uncovered: False)

    minesweeper.game_loop(numbered_field)

    captured = capsys.readouterr().out
    assert "Bumm! Aknára léptünk. Vége a játéknak!" in captured