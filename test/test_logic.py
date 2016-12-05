from vhdltree.logic import find_entities


class TestFindEntities:
    def test_simple(self):
        assert tuple(find_entities(['e: entity c'])) == (('e', 'c'),)

    def test_libs(self):
        assert tuple(find_entities(['e: entity work.library.name.c'])) == (('e', 'c'),)

    def test_invalid_prefix(self):
        assert tuple(find_entities(['1e: entity c'])) == ()

    def test_invalid_suffix(self):
        assert tuple(find_entities('e: entity c_')) == ()

    def test_spacing(self):
        assert tuple(find_entities(['\t e :\tentity  c \n'])) == (('e', 'c'),)

    def test_real_identifiers(self):
        assert tuple(find_entities(['Mux_d2h_0 : entity work.muxes.std_mux'])) == (('Mux_d2h_0', 'std_mux'),)

    def test_several(self):
        found = tuple(find_entities([
            'e1: entity c1',
            'e2: entity c1',
            'e3: entity c2',
            'another statement'
        ]))
        assert found == (
            ('e1', 'c1'),
            ('e2', 'c1'),
            ('e3', 'c2')
        )
