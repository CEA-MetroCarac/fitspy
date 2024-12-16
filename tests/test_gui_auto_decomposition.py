import sys
import pytest
from pathlib import Path
from pytest import approx

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_gui_auto_decomposition import gui_auto_decomposition
from utils import extract_results, display_is_ok

# REFS shared with test_nogui_auto_decomposition
REFS = [[142.2017338937751, 28029.56087034003, 8.277805414840545],
        [137.67515324567708, 18759.15930233963, 14.979941168937462],
        [366.6105573370797, 8114.486816783022, 43.73282414562729]]


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_auto_decomposition(tmp_path):
    gui_auto_decomposition(dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    for result, reference in zip(results, REFS):
        assert result == approx(reference, rel=2e-2)
