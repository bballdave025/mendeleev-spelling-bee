import subprocess
import tempfile
import os

CLI = ["python", "-m", "mendeleevspellingbee.core"]

def test_help_flag():
    result = subprocess.run(CLI + ["--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Decode words using chemical element symbols" in result.stdout
    print("✅ test_help_flag passed")

def test_raw_latin_symbols():
    result = subprocess.run(
        CLI + ["-d", "cook,cool,hi,bacon,car,flamingo,rain", "-s", "H,He,B,C,N,O,Ac,Na,Cl,U,Co,K"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "cook" in result.stdout and "cook" in result.stdout
    print("✅ test_raw_latin_symbols passed")

def test_raw_cyrillic_symbols():
    result = subprocess.run(
        CLI + ["-d", "урал,аккордион,аккордам,уг,акцепт", "-s", "Ур,Ал,Ки,Ак,Ко,Рд"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "урал" in result.stdout and "аккордам" in result.stdout
    print("✅ test_raw_cyrillic_symbols passed")

def test_builtin_latin_symbols_with_latin_dict():
    result = subprocess.run(
        CLI + ["-d", "/usr/share/dict/words", "-s", "latin"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "rain" in result.stdout and "close" in result.stdout
    print("✅ test_builtin_latin_symbols_with_latin_dict passed")

def test_builtin_cyrillic_symbols_with_russian_dict():
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
        f.write("урал\nуг\nаккордам\nаккордион\nакцепт\nтунисе\n")
        f.flush()
        path = f.name

    result = subprocess.run(
        CLI + ["-d", path, "-s", "cyrillic"],
        capture_output=True, text=True
    )
    os.unlink(path)
    assert result.returncode == 0
    assert "тунисе" in result.stdout and "аккордион" in result.stdout
    print("✅ test_builtin_cyrillic_symbols_with_russian_dict passed")

def test_mismatch_latin_symbols_with_russian_dict():
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
        f.write("урал\nуг\nаккордам\nаккордион\nакцепт\nтунисе\n")
        f.flush()
        path = f.name

    result = subprocess.run(
        CLI + ["-d", path, "-s", "latin"],
        capture_output=True, text=True
    )
    os.unlink(path)
    assert result.returncode == 0
    assert result.stdout.strip() == ""
    print("✅ test_mismatch_latin_symbols_with_russian_dict passed")

def test_mismatch_cyrillic_symbols_with_latin_dict():
    result = subprocess.run(
        CLI + ["-d", "/usr/share/dict/words", "-s", "cyrillic"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == ""
    print("✅ test_mismatch_cyrillic_symbols_with_latin_dict passed")


