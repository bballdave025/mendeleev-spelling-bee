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
        CLI + ["-d", "cool,cook,bacon", "-s", "H,He,B,C,N,O,Ac,Na,Cl,U,Co,K"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "cool" in result.stdout or "cook" in result.stdout
    print("✅ test_raw_latin_symbols passed")

def test_raw_cyrillic_symbols():
    result = subprocess.run(
        CLI + ["-d", "бор,кислород,углерод", "-s", "Бо,Ки,Уг"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "бор" in result.stdout or "кислород" in result.stdout
    print("✅ test_raw_cyrillic_symbols passed")

def test_builtin_latin_symbols_with_latin_dict():
    result = subprocess.run(
        CLI + ["-d", "/usr/share/dict/words", "-s", "latin"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "neon" in result.stdout or "argon" in result.stdout
    print("✅ test_builtin_latin_symbols_with_latin_dict passed")

def test_builtin_cyrillic_symbols_with_russian_dict():
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
        f.write("бор\nкислород\nуглерод\n")
        f.flush()
        path = f.name

    result = subprocess.run(
        CLI + ["-d", path, "-s", "cyrillic"],
        capture_output=True, text=True
    )
    os.unlink(path)
    assert result.returncode == 0
    assert "бор" in result.stdout or "кислород" in result.stdout
    print("✅ test_builtin_cyrillic_symbols_with_russian_dict passed")

def test_mismatch_latin_symbols_with_russian_dict():
    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f:
        f.write("бор\nкислород\nуглерод\n")
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


