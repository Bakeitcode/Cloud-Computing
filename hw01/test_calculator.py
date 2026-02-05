import builtins

from hw01.calculator import main


def run_main_with_inputs(monkeypatch, inputs):
    """Helper to feed inputs to main() in order."""
    it = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda _: next(it))


def test_addition(monkeypatch, capsys):
    run_main_with_inputs(monkeypatch, ["2", "+", "3"])
    main()
    out = capsys.readouterr().out
    assert "Result:" in out
    assert "5.0" in out


def test_subtraction(monkeypatch, capsys):
    run_main_with_inputs(monkeypatch, ["10", "-", "4"])
    main()
    out = capsys.readouterr().out
    assert "6.0" in out


def test_multiplication(monkeypatch, capsys):
    run_main_with_inputs(monkeypatch, ["3", "*", "4"])
    main()
    out = capsys.readouterr().out
    assert "12.0" in out


def test_division(monkeypatch, capsys):
    run_main_with_inputs(monkeypatch, ["8", "/", "2"])
    main()
    out = capsys.readouterr().out
    assert "4.0" in out


def test_division_by_zero(monkeypatch, capsys):
    run_main_with_inputs(monkeypatch, ["8", "/", "0"])
    main()
    out = capsys.readouterr().out
    assert "Error: division by zero" in out
    assert "Result:" not in out


def test_invalid_operator(monkeypatch, capsys):
    run_main_with_inputs(monkeypatch, ["1", "%", "2"])
    main()
    out = capsys.readouterr().out
    assert "Invalid operator" in out
    assert "Result:" not in out
