# What this does:
First argument is the main file, second one is the project root.

`./vhdltree.py test/main.vhd test/`
```
e1i1 : test/long_component_name5678.vhd
    long_ent17y_n4m3_with_numbers4567 : test/lib/deep/e4.vhd
E3_i1 : test/lib/E3.vhd
e2I1 : test/e2.vhd
    bad_prefix : test/lib/E3.vhd
    check_recurse : test/lib/E3.vhd
    NO_PREFIX : test/lib/E3.vhd
truncate_before_dot : test/lib/deep/e4.vhd
the : test/e_1.vhd
    chain : test/lib/e5.vhd
        goes : test/lib/deep/e6.vhd
            on : test/e7.vhd
e1i2 : test/long_component_name5678.vhd
    long_ent17y_n4m3_with_numbers4567 : test/lib/deep/e4.vhd
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
* As of [e443187](https://github.com/nathdwek/vhdltree/commit/e443187c79cf45b9bcbb49cdf3527d8df034ba2b): does not match VHDL extended identifiers. The regex can be changed back to extremely bare in order to match more exotic identifiers.
* To find an entity file, we do not respect the library prefix at all. I don't even know how libraries work in VHDL in terms of where the files should be.
* As a consequence (other than speed) we cannot guarantee that the file examined for an entity is the actual file the compiler will use if there are files with the same basename in different directories. The way `vhd_files` maps basenames to paths depends on the order of `os.walk` and the `EXCLUDES` variable.
* Case insensitive, spaces agnostic because VHDL.
