import os
import pytest

from vhdltree.logic import find_vhd, _vhdltree, vhdltree


@pytest.fixture()
def cd_proot():
    proot = os.path.join(os.path.dirname(__file__), 'dummy_project')
    os.chdir(proot)


@pytest.mark.usefixtures("cd_proot")
class TestIntegration:
    def test_find_vhd(self):
        assert dict(find_vhd('./')) == {
            'e2': './e2.vhd',
            'e3': './lib/E3.vhd',
            'e4': './lib/deep/e4.vhd',
            'e5': './lib/e5.vhd',
            'e6': './lib/deep/e6.vhd',
            'e7': './e7.vhd',
            'e_1': './e_1.vhd',
            'long_component_name5678': './long_component_name5678.vhd',
            'main': './main.vhd'
        }

    def test_vhdltree_logic(self):
        vhd_files = {
            'e2': './e2.vhd',
            'e3': './lib/E3.vhd',
            'e4': './lib/deep/e4.vhd',
            'e5': './lib/e5.vhd',
            'e6': './lib/deep/e6.vhd',
            'e7': './e7.vhd',
            'e_1': './e_1.vhd',
            'long_component_name5678': './long_component_name5678.vhd',
            'main': './main.vhd'
        }
        assert tuple(_vhdltree(0, './main.vhd', vhd_files)) == (
            (0, 'e1i1', './long_component_name5678.vhd'),
            (1, 'long_ent17y_n4m3_with_numbers4567', './lib/deep/e4.vhd'),
            (0, 'e1i2', './long_component_name5678.vhd'),
            (1, 'long_ent17y_n4m3_with_numbers4567', './lib/deep/e4.vhd'),
            (0, 'e2I1', './e2.vhd'),
            (1, 'NO_PREFIX', './lib/E3.vhd'),
            (1, 'bad_prefix', './lib/E3.vhd'),
            (0, 'E3_i1', './lib/E3.vhd'),
            (0, 'truncate_before_dot', './lib/deep/e4.vhd'),
            (0, 'the', './e_1.vhd'),
            (1, 'chain', './lib/e5.vhd'),
            (2, 'goes', './lib/deep/e6.vhd'),
            (3, 'on', './e7.vhd'),
            (0, 'not_found', '')
        )

    def test_integration(self, capsys):
        vhdltree('./main.vhd', './')
        out, err = capsys.readouterr()
        assert not err
        assert out == """e1i1 : ./long_component_name5678.vhd
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
"""
