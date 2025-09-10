# mendeleev-spelling-bee

A little NLP fun: finding which words can be made using only the symbols of Mendeleev's Table, more commonly known as the period table (perhaps less justly also known as that). The trick here is that we will use multiple languages. We'll even try to use scripts - let's be specific, the [writing system](https://en.wikipedia.org/wiki/Writing_system) ([archived](https://web.archive.org/web/20240613141523/https://en.wikipedia.org/wiki/Writing_system)) type of scripts (to the degree that Periodic Tables can be found in other scripts) - starting with Cyrillic.

# Content of README

You definitely want to go see [The Basics](), as there's a lot of fun down there. However, I want to look at the test-driven development used to make this think work with Latin and Cyrillic script versions of the periodic table. How did I get a Cyrillic version of the periodic table? Well, that will be discussed in the Chain of Though (CoT) propmting section. I must say that it's more

## Test-driven development.

The first set of tests had been set up before the code was completely written. As soon as I had a backbone, I set up the following, from the root of this repo

```bash
 <=> conda environment, blank means none activated
[feature/cli-tokenizer] <=> git branch, blank means not in a git repo
bballdave025@MY-MACHINE ~/my_repos_dwb/mendeleev-spelling-bee
$ cat tests/test_core.py 
import subprocess
import tempfile
import os

CLI = ["python", "-m", "mendeleevspellingbee.core"]

def test_help_flag():
    result = subprocess.run(CLI + ["--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Decode words using chemical element symbols" in result.stdout
    print("[checks] test_help_flag passed")

def test_raw_latin_symbols():
    result = subprocess.run(
        CLI + ["-d", "cook,cool,hi,bacon,car,flamingo,rain", "-s", "H,He,B,C,N,O,Ac,Na,Cl,U,Co,K"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "cook" in result.stdout and "cook" in result.stdout
    print("[checks] test_raw_latin_symbols passed")

def test_raw_cyrillic_symbols():
    result = subprocess.run(
        CLI + ["-d", "урал,аккордион,аккордам,уг,акцепт", "-s", "Ур,Ал,Ки,Ак,Ко,Рд,Ам"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "урал" in result.stdout and "аккордам" in result.stdout
    print("[checks] test_raw_cyrillic_symbols passed")

def test_builtin_latin_symbols_with_latin_dict():
    result = subprocess.run(
        CLI + ["-d", "/usr/share/dict/words", "-s", "latin"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "rain" in result.stdout and "close" in result.stdout
    print("[checks] test_builtin_latin_symbols_with_latin_dict passed")

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
    assert "тунисе" in result.stdout and "аккордам" in result.stdout
    print("[checks] test_builtin_cyrillic_symbols_with_russian_dict passed")

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
    print("[checks] test_mismatch_latin_symbols_with_russian_dict passed")

def test_mismatch_cyrillic_symbols_with_latin_dict():
    result = subprocess.run(
        CLI + ["-d", "/usr/share/dict/words", "-s", "cyrillic"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == ""
    print("[checks] test_mismatch_cyrillic_symbols_with_latin_dict passed")


=====..........................................................retval=0.........
```

This has passed, as you'll see in the next code snippet, and after it did, I
committed and pushed it as the `v0.1.1`, the release following the basic development
in `v0.1.1`. The branch that got released as `v0.1.1` was `feature/cli-tokenizer`. The
next branch, to be committed as `v0.1.2` has the goal of adding a `--contains` flag,
so the user can enter a word or list of words (we'll want to enter a list of the
elements, to see which elements can be spelled using only the chemical-element
symbols).

Here are the test results:

```bash
 <=> conda environment, blank means none activated
[feature/cli-tokenizer] <=> git branch, blank means not in a git repo
bballdave025@MY-MACHINE ~/my_repos_dwb/mendeleev-spelling-bee
$ pytest -v -s
============================= test session starts ==============================
platform linux -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0 -- /home/bballdave025/miniforge3/bin/python3.12
cachedir: .pytest_cache
rootdir: /home/bballdave025/my_repos_dwb/mendeleev-spelling-bee
configfile: pyproject.toml
collected 7 items                                                              

tests/test_core.py::test_help_flag [checks] test_help_flag passed
PASSED
tests/test_core.py::test_raw_latin_symbols [checks] test_raw_latin_symbols passed
PASSED
tests/test_core.py::test_raw_cyrillic_symbols [checks] test_raw_cyrillic_symbols passed
PASSED
tests/test_core.py::test_builtin_latin_symbols_with_latin_dict [checks] test_builtin_latin_symbols_with_latin_dict passed
PASSED
tests/test_core.py::test_builtin_cyrillic_symbols_with_russian_dict [checks] test_builtin_cyrillic_symbols_with_russian_dict passed
PASSED
tests/test_core.py::test_mismatch_latin_symbols_with_russian_dict [checks] test_mismatch_latin_symbols_with_russian_dict passed
PASSED
tests/test_core.py::test_mismatch_cyrillic_symbols_with_latin_dict [checks] test_mismatch_cyrillic_symbols_with_latin_dict passed
PASSED

============================== 7 passed in 18.77s ==============================
=====..........................................................retval=0.........
```

So, what am I testing?

# The Basics

Basic - find words and phrases that can be created by using the symbols from the Mendeleev chart (Periodic Table). Examples would be:

`Radium` `Iodine` `Nitrogen` = <kbd>Ra</kbd><kbd>I</kbd><kbd>N</kbd> , which is liquid precipitation, of course.

`Francium` `Silver` = <kbd>Fr</kbd><kbd>Ag</kbd> , which is an adjective for a type of grenade or a verb that has come into normal English usage due to video games.

The work below (in the section, _Let's see if we can quickly find some examples that are more fun_), gives me a quick fun one,

`Thorium` `Iodine` `Sulfur` &nbsp;&nbsp; `Flerovium` `Americium` `Gallium` &nbsp;&nbsp;&nbsp;&nbsp; is &nbsp;&nbsp;&nbsp;&nbsp;
<kbd>Th</kbd><kbd>I</kbd><kbd>S</kbd> &nbsp;&nbsp; <kbd>Fl</kbd><kbd>Am</kbd><kbd>In</kbd><kbd>Ga</kbd>

Well, &nbsp;&nbsp;`Sulfur` `Oxygen` &nbsp;&nbsp; `Chlorine` `Oxygen` `Selenium` &nbsp;&nbsp; to 'This Flamingo'

<kbd>S</kbd><kbd>O</kbd> &nbsp;&nbsp; <kbd>Cl</kbd><kbd>O</kbd><kbd>Se</kbd>

I do think I should get extra points for using both `Francium` and `Gallium` in this section.

[Skip to the _Some fun goals for which to shoot_ section](#Some-fun-goals-for-which-to-shoot) if you don't want to see my `bash` ramblings.


## All the element symbols in a nice way

You can refer to the [Let us see if we can quickly find some examples that are more fun]() section to see some of the groundwork laid for this part.

```
$ a=$(lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    sed -n '112,141p' | awk '{print $3}' | tr '\n' ' '\
)
$ b=$(lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    awk 'NR>=152&&NR<= 309' | awk '{print $1}' | \
    grep "^[A-Za-z]\{1,2\}$" | tr '\n' ' ' \
)
$ echo "$a $b" | fold -w 50 -s
```

... which gives us the output

```
H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K
Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn  Ac Ag Al Am Ar
As At Au B Ba Be Bh Bi Bk Br C Ca Cd Ce Cf Cl Cm
Cn Co Cr Cs Cu Db Ds Dy Er Es Eu F Fe Fl Fm Fr Ga
Gd Ge H He Hf Hg Ho Hs I In Ir K Kr La Li Lr Lu
Lv Mc Md Mg Mn Mo Mt N Na Nb Nd Ne Nh Ni No Np O
Og Os P Pa Pb Pd Pm Po Pr Pt Pu Ra Rb Re Rf Rg Rh
Rn Ru S Sb Sc Se Sg Si Sm Sn Sr Ta Tb Tc Te Th Ti
Tl Tm Ts U V W Xe Y Yb Zn Zr
```

(I'm not going to make it look like the actual periodic table, right now, no matter how tempting it is.) (There will probably be a `bash` script forthcoming.)

(It would have been more efficient to put the output of `lynx` into a string, but I don't think it would have been as clear.)

## So, what does the CLI look like in v0.1.1?

```bash
 <=> conda environment, blank means none activated
[feature/cli-tokenizer] <=> git branch, blank means not in a git repo
bballdave025@MY-MACHINE ~/my_repos_dwb/mendeleev-spelling-bee
$ mendeleevspellingbee --help
usage: mendeleevspellingbee [-h] -d DICTIONARY [-s SYMBOL_LIST]
                            [-c SYMBOL_CSV] [-p {noun,verb,adjective,adverb}]
                            [-f] [--version]

Decode words using chemical element symbols

options:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        Comma-separated words or path to dictionary file
  -s SYMBOL_LIST, --symbol-list SYMBOL_LIST
                        Comma-delimited symbols or built-in set name
  -c SYMBOL_CSV, --symbol-csv SYMBOL_CSV
                        Path to CSV file containing custom symbol list
  -p {noun,verb,adjective,adverb}, --part-of-speech {noun,verb,adjective,adverb}
                        Filter words by part of speech (English only)
  -f, --try-flush       Enable flushing for the print command; trying to flush
                        per-line
  --version             show program's version number and exit
=====..........................................................retval=0.........


## Let's see if we can quickly find some examples that are more fun

Some quick `bash` fun for getting the element symbols. The list that appears on [Simple English Wikipedia](https://simple.wikipedia.org/wiki/) seems a good place to start.

```bash
$ type lynx
lynx is /usr/bin/lynx
$ cat >/dev/null << EOF
> #  If you don't have it, check out
> #+ https://lynx.invisible-island.net/lynx2.8.8/breakout/INSTALLATION
> #+  OR
> #+ https://www.linuxfromscratch.org/blfs/view/svn/basicnet/lynx.html
> #+ I'll put the archived version of the second after the quick code.
> EOF
$
```

([archived site as promised](https://web.archive.org/web/20240613145546/https://www.linuxfromscratch.org/blfs/view/svn/basicnet/lynx.html))

```
$ urlstr1="https://web.archive.org/web/20240613143341/"
$ #  really don't need that 1st 1 unless you want exact reproducibility
$ #+ so the final `lynx` command could be without "${urlstr1}"
$ urlstr2="https://simple.wikipedia.org/wiki/List_of_elements_by_symbol"
$ # lynx -dump -nolist "${urlstr1}${urlstr2}" | less # scroll through
```

Hit the <kbd>q</kbd> button. (N.B. I actually used `lynx -dump -nolist "${urlstr1}${urlstr2}" | less`)

```
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | sed -n '111,141p;142q'
   Number
   1 Hydrogen H 1 1
   2 Helium He 18 1
   3 Lithium Li 1 2
   4 Beryllium Be 2 2
   5 Boron B 13 2
   6 Carbon C 14 2
   7 Nitrogen N 15 2
   8 Oxygen O 16 2
   9 Fluorine F 17 2
   10 Neon Ne 18 2
   11 Sodium Na 1 3
   12 Magnesium Mg 2 3
   13 Aluminium Al 13 3
   14 Silicon Si 14 3
   15 Phosphorus P 15 3
   16 Sulfur S 16 3
   17 Chlorine Cl 17 3
   18 Argon Ar 18 3
   19 Potassium K 1 4
   20 Calcium Ca 2 4
   21 Scandium Sc 3 4
   22 Titanium Ti 4 4
   23 Vanadium V 5 4
   24 Chromium Cr 6 4
   25 Manganese Mn 7 4
   26 Iron Fe 8 4
   27 Cobalt Co 9 4
   28 Nickel Ni 10 4
   29 Copper Cu 11 4
   30 Zinc Zn 12 4

$ #  Don't want first or last lines, want field number 3
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    sed -n '112,141p' | awk '{print $3}' | tr '\n' ' '
H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn
```

If you want the element name included, try  `lynx -dump -nolist "${urlstr1}${urlstr2}" | sed -n '112,141p' | awk '{print $2 "=" $3}' | tr '\n' ' '`

The rest ... first we'll check out how to parse and cite things correctly ...

```
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    awk 'NR>=150&&NR<= 311' | head -n 5
   Chemical sym Name Origin of symbol Atomic No. Atomic mass Density (near
   r.t.) Melting point Boiling point Year of discovery Discoverer
   Ac Actinium 89 227.0278 u 10.07 g/cm^3 1047 °C 3197 °C 1899 Debierne
   Ag Silver Latin Argentum 47 107.8682 u 10.49 g/cm^3 961.9 °C 2212 °C
   prehistoric unknown
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    awk 'NR>=150&&NR<= 311' | tail -n 5
   Zn Zinc 30 65.39 u 7.14 g/cm^3 419.6 °C 907 °C prehistoric unknown
   Zr Zirconium 40 91.224 u 6.51 g/cm^3 1852 °C 4377 °C 1789 Klaproth
   Retrieved from
   "https://simple.wikipedia.org/w/index.php?title=List_of_elements_by_sym
   bol&oldid=9591700"
$ echo "Retrieved: $(date +'%s_%Y-%m-%dT%H:%M:%S%z')"
Retrieved: 1718290750_2024-06-13T08:59:10-0600
```

The rest in an almost-nice way (it's probably going to scroll off your screen). 

```
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    awk 'NR>=152&&NR<= 309' | awk '{print $1}' | \
    grep "^[A-Za-z]\{1,2\}$" | tr '\n' ' '
Ac Ag Al Am Ar As At Au B Ba Be Bh Bi Bk Br C Ca Cd Ce Cf Cl Cm Cn Co Cr Cs Cu Db Ds Dy Er Es Eu F Fe Fl Fm Fr Ga Gd Ge H He Hf Hg Ho Hs I In Ir K Kr La Li Lr Lu Lv Mc Md Mg Mn Mo Mt N Na Nb Nd Ne Nh Ni No Np O Og Os P Pa Pb Pd Pm Po Pr Pt Pu Ra Rb Re Rf Rg Rh Rn Ru S Sb Sc Se Sg Si Sm Sn Sr Ta Tb Tc Te Th Ti Tl Tm Ts U V W Xe Y Yb Zn Zr
```

Here, it would have been a bit more complicated to get the names and symbols, but it could be done (for example) with 
`lynx -dump -nolist "${urlstr1}${urlstr2}" | awk 'NR>=152&&NR<= 309' | sed -n '/^[ ]\+\([A-Za-z]\{1,2\}\)[ ]\([A-Za-z]\+\)[ ]/p' | awk '{print $2 "=" $1}'`

Oh, you should also note that I've used three ways to get the lines I wanted by line number. They are, without explanation, 1) ` | sed -n '{first},{next-to-last}p;{last}q'` (best for large files). 2) ` | sed -n '{first},{last}p'`. and 3) ` | awk 'NR>={first}&&NR<={last}'` (okay for large files, I believe).

## Let us see if we can quickly find some examples that are more fun

Some quick `bash` fun for getting the element symbols. The list that appears on [Simple English Wikipedia](https://simple.wikipedia.org/wiki/) seems a good place to start.

```bash
$ type lynx
lynx is /usr/bin/lynx
$ cat >/dev/null << EOF
> #  If you don't have it, check out
> #+ https://lynx.invisible-island.net/lynx2.8.8/breakout/INSTALLATION
> #+  OR
> #+ https://www.linuxfromscratch.org/blfs/view/svn/basicnet/lynx.html
> #+ I'll put the archived version of the second after the quick code.
> EOF
$
```

([archived site as promised](https://web.archive.org/web/20240613145546/https://www.linuxfromscratch.org/blfs/view/svn/basicnet/lynx.html))

```
$ urlstr1="https://web.archive.org/web/20240613143341/"
$ #  really don't need that 1st 1 unless you want exact reproducibility
$ #+ so the final `lynx` command could be without "${urlstr1}"
$ urlstr2="https://simple.wikipedia.org/wiki/List_of_elements_by_symbol"
$ # lynx -dump -nolist "${urlstr1}${urlstr2}" | less # scroll through
```

Hit the <kbd>q</kbd> button. (N.B. I actually used `lynx -dump -nolist "${urlstr1}${urlstr2}" | less`)

```
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | sed -n '111,141p;142q'
   Number
   1 Hydrogen H 1 1
   2 Helium He 18 1
   3 Lithium Li 1 2
   4 Beryllium Be 2 2
   5 Boron B 13 2
   6 Carbon C 14 2
   7 Nitrogen N 15 2
   8 Oxygen O 16 2
   9 Fluorine F 17 2
   10 Neon Ne 18 2
   11 Sodium Na 1 3
   12 Magnesium Mg 2 3
   13 Aluminium Al 13 3
   14 Silicon Si 14 3
   15 Phosphorus P 15 3
   16 Sulfur S 16 3
   17 Chlorine Cl 17 3
   18 Argon Ar 18 3
   19 Potassium K 1 4
   20 Calcium Ca 2 4
   21 Scandium Sc 3 4
   22 Titanium Ti 4 4
   23 Vanadium V 5 4
   24 Chromium Cr 6 4
   25 Manganese Mn 7 4
   26 Iron Fe 8 4
   27 Cobalt Co 9 4
   28 Nickel Ni 10 4
   29 Copper Cu 11 4
   30 Zinc Zn 12 4

$ #  Don't want first or last lines, want field number 3
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    sed -n '112,141p' | awk '{print $3}' | tr '\n' ' '
H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn
```

If you want the element name included, try  `lynx -dump -nolist "${urlstr1}${urlstr2}" | sed -n '112,141p' | awk '{print $2 "=" $3}' | tr '\n' ' '`

The rest ... first we'll check out how to parse and cite things correctly ...

```
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    awk 'NR>=150&&NR<= 311' | head -n 5
   Chemical sym Name Origin of symbol Atomic No. Atomic mass Density (near
   r.t.) Melting point Boiling point Year of discovery Discoverer
   Ac Actinium 89 227.0278 u 10.07 g/cm^3 1047 °C 3197 °C 1899 Debierne
   Ag Silver Latin Argentum 47 107.8682 u 10.49 g/cm^3 961.9 °C 2212 °C
   prehistoric unknown
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    awk 'NR>=150&&NR<= 311' | tail -n 5
   Zn Zinc 30 65.39 u 7.14 g/cm^3 419.6 °C 907 °C prehistoric unknown
   Zr Zirconium 40 91.224 u 6.51 g/cm^3 1852 °C 4377 °C 1789 Klaproth
   Retrieved from
   "https://simple.wikipedia.org/w/index.php?title=List_of_elements_by_sym
   bol&oldid=9591700"
$ echo "Retrieved: $(date +'%s_%Y-%m-%dT%H:%M:%S%z')"
Retrieved: 1718290750_2024-06-13T08:59:10-0600
```

The rest in an almost-nice way (it's probably going to scroll off your screen). 

```
$ lynx -dump -nolist "${urlstr1}${urlstr2}" | \
    awk 'NR>=152&&NR<= 309' | awk '{print $1}' | \
    grep "^[A-Za-z]\{1,2\}$" | tr '\n' ' '
Ac Ag Al Am Ar As At Au B Ba Be Bh Bi Bk Br C Ca Cd Ce Cf Cl Cm Cn Co Cr Cs Cu Db Ds Dy Er Es Eu F Fe Fl Fm Fr Ga Gd Ge H He Hf Hg Ho Hs I In Ir K Kr La Li Lr Lu Lv Mc Md Mg Mn Mo Mt N Na Nb Nd Ne Nh Ni No Np O Og Os P Pa Pb Pd Pm Po Pr Pt Pu Ra Rb Re Rf Rg Rh Rn Ru S Sb Sc Se Sg Si Sm Sn Sr Ta Tb Tc Te Th Ti Tl Tm Ts U V W Xe Y Yb Zn Zr
```

Here, it would have been a bit more complicated to get the names and symbols, but it could be done (for example) with 
`lynx -dump -nolist "${urlstr1}${urlstr2}" | awk 'NR>=152&&NR<= 309' | sed -n '/^[ ]\+\([A-Za-z]\{1,2\}\)[ ]\([A-Za-z]\+\)[ ]/p' | awk '{print $2 "=" $1}'`

Oh, you should also note that I've used three ways to get the lines I wanted by line number. They are, without explanation, 1) ` | sed -n '{first},{next-to-last}p;{last}q'` (best for large files). 2) ` | sed -n '{first},{last}p'`. and 3) ` | awk 'NR>={first}&&NR<={last}'` (okay for large files, I believe).


# Some fun further goals for which to shoot

## Find if a Mendeleevan string (I might have just made that word up) is sensible. 

This could, in probably a mid-difficulty (or at least mid-time-used) solution, use a context-free-grammar and a parser. 

If the time were there, the high-difficulty (or at least high-time-used) solution, a.k.a. <b>the fun solution</b>, is the task of collecting a dataset of sensible and non-sensible strings and to train a not-very-deep neural network. Since this would probably look for funny, 2-year-old time phrases, a custom dataset would be ideal. Perhaps one could use a web scraper for sensible examples and something such as the Library of Babel for those which are nonsensible. Actually, training something with a degree-of-sensibility output would be awesome, but would probably need more of a LLM-type solution and almost certainly a new dataset (unless perplexity could be hacked more than I realize it can be). By the way, asking an LLM such as [ChatGPT](https://chat.openai.com/) if the sentence makes sense is the least-fun solution.

A few low-difficulty (or at least low-time-used) solutions, some available tools such as those listed or discussed at the following places

https://nlp.stanford.edu/software/lex-parser.html

https://github.com/jxmorris12/language_tool_python

https://www.afterthedeadline.com/development.html

https://pypi.python.org/pypi/language-check

https://github.com/zoncoen/python-ginger

https://web.archive.org/web/20240613140257/https://stackoverflow.com/questions/10252448/how-to-check-whether-a-sentence-is-correct-simple-grammar-check-in-python
 (list/discussion of others)
 
https://www.openoffice.org/lingucomponent/grammar.html
 (list of others)

## See which molecules make words

## See if any 'shorthand' chemical formulas are sensible
