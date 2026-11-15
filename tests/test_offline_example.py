import json
import runpy
from pathlib import Path


async def test_offline_example_uses_memory_transport(capsys):
    example = Path(__file__).parents[1] / "examples" / "offline.py"
    namespace = runpy.run_path(str(example))
    await namespace["main"]()
    result = json.loads(capsys.readouterr().out)
    assert result == {"mode": "synthetic-offline", "class": "AceDataCloud_LLM", "reply": "Synthetic reply"}
