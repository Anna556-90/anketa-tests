import pytest
from wordcount import chastota

# Задача Р5
@pytest.fixture
def fayl_s_textom(tmp_path):
    put = tmp_path / "text.txt"
    put.write_text("Мама мыла раму. Рама, мама, рама!", encoding="utf-8")
    return put

def test_chastota_mama_rama(fayl_s_textom):
    stat = chastota(fayl_s_textom)
    assert stat["мама"] == 2
    assert stat["рама"] == 2

def test_chastota_net_punktuacii(fayl_s_textom):
    stat = chastota(fayl_s_textom)
    assert "рама," not in stat
    assert "раму." not in stat

def test_chastota_raznye_slova(fayl_s_textom):
    stat = chastota(fayl_s_textom)
    assert len(stat) == 4