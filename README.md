# Usage:
`vhdltree [-p,--project PROJECT_ROOT] MAIN_VHD`

# With Provided Test Project:
`$ vhdltree test/dummy_project/main.vhd -p test/dummy_project`
```
e1i1 : ./long_component_name5678.vhd
    long_ent17y_n4m3_with_numbers4567 : ./lib/deep/e4.vhd
e1i2 : ./long_component_name5678.vhd
    long_ent17y_n4m3_with_numbers4567 : ./lib/deep/e4.vhd
e2I1 : ./e2.vhd
    NO_PREFIX : ./lib/E3.vhd
    bad_prefix : ./lib/E3.vhd
E3_i1 : ./lib/E3.vhd
truncate_before_dot : ./lib/deep/e4.vhd
the : ./e_1.vhd
    chain : ./lib/e5.vhd
        goes : ./lib/deep/e6.vhd
            on : ./e7.vhd
not_found : Not found
```

*Yes, the names used in the test are minimal because I am lazy and ugly to push the regex a minimum.*

Real project, 156 total instantiated entities (approx. 10 levels deep), 1.6GB project root with 45000 files and directories approx. 15 levels deep:
```
real    0m0.149s
user    0m0.123s
sys     0m0.025s
```

# Caveats:
* As of [a360c80](https://github.com/nathdwek/vhdltree/commit/a360c80ef496e0f71a81545485b1524ceee8b0d6): Python >= 3.5 required.
* As of [e443187](https://github.com/nathdwek/vhdltree/commit/e443187c79cf45b9bcbb49cdf3527d8df034ba2b): Does not match VHDL extended identifiers. The regex can be changed back to extremely bare in order to match more exotic identifiers.
* To find an entity file, we do not respect the library prefix at all. I don't even know how libraries work in VHDL in terms of where the files should be.
* As a consequence (other than speed) we cannot guarantee that the file examined for an entity is the actual file the compiler will use if there are files with the same basename in different directories. The way `vhd_files` maps basenames to paths depends on their "tree" order and the `EXCLUDES` variable.
* Case insensitive, spaces agnostic because VHDL.
