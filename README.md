# What this does:
First argument is the main file, second one is the project root.

`./vhdltree.py test/main.vhd test/`
```
E3i1 : test/lib/E3.vhd
e2I1 : test/e2.vhd
    e3i2 : test/lib/E3.vhd
e1i1 : test/e1.vhd
    e4içàéè_éè_1 : test/lib/deep/e4.vhd
e1i2 : test/e1.vhd
    e4içàéè_éè_1 : test/lib/deep/e4.vhd
```

*Yes, the names used in the test are minimal because I am lazy and ugly to push the regex a minimum.*

Real project, 156 total instantiated entities (approx. 10 levels deep), 1.6GB project root with 45000 files and directories approx 15 levels deep:
```
real    0m0.219s
user    0m0.165s
sys     0m0.053s
```

# Caveats:
* The construction of the file list is not that efficient, we still `os.walk` the whole project directory, even though we do it only once.
* I am not that versed in VHDL syntax, so the regular expression to find entities is really minimal.
* To find an entity file, we do not respect the library prefix at all. I don't even know how libraries work in VHDL in terms of where the files should be.
* As a consequence (other than speed) we cannot guarantee that the file examined for an entity is the actual file the compiler will use if there are files with the same basename in different directories. The way `vhd_files` maps basenames to paths depends on the order of `os.walk` and the `EXCLUDES` variable.
* Case insensitive, spaces agnostic because VHDL.
