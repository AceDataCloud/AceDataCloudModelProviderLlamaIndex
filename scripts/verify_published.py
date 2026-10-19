"""Read-only installed native package checks; never execute a model or media tool."""
import importlib
from importlib.metadata import version
import json
import os
from pathlib import Path

PACKAGES = {
    "llama-index-llms-acedatacloud": ("llama_index.llms.acedatacloud", "AceDataCloud", 0),
    "llama-index-tools-suno-acedatacloud": ("llama_index.tools.suno_acedatacloud", "SunoToolSpec", 2),
    "llama-index-tools-seedance-acedatacloud": ("llama_index.tools.seedance_acedatacloud", "SeedanceToolSpec", 3),
    "llama-index-tools-happyhorse-acedatacloud": ("llama_index.tools.happyhorse_acedatacloud", "HappyHorseToolSpec", 3),
    "llama-index-tools-gpt-image-acedatacloud": ("llama_index.tools.gpt_image_acedatacloud", "GPTImageToolSpec", 3),
    "llama-index-tools-nano-banana-acedatacloud": ("llama_index.tools.nano_banana_acedatacloud", "NanoBananaToolSpec", 3),
}
package = os.environ["PACKAGE"]
expected_version = os.environ["VERSION"]
module_name, class_name, count = PACKAGES[package]
assert version(package) == expected_version
module = importlib.import_module(module_name)
assert "site-packages" in module.__file__
cls = getattr(module, class_name)
if count:
    import asyncio
    instance = cls(api_token="schema-only-not-a-real-key")
    try:
        tools = instance.to_tool_list()
        assert len(tools) == count
        schemas = [{"name": t.metadata.name, "parameters": t.metadata.get_parameters_dict()} for t in tools]
        assert "schema-only-not-a-real-key" not in json.dumps(schemas)
        assert all("api_token" not in json.dumps(s["parameters"]) for s in schemas)
        result = {"tools": schemas}
    finally:
        asyncio.run(instance.aclose())
else:
    instance = cls(model="explicit-schema-only-model", context_window=4096, api_token="schema-only-not-a-real-key")
    assert instance.class_name() == "AceDataCloud_LLM"
    assert not instance.metadata.is_function_calling_model
    assert "schema-only-not-a-real-key" not in instance.model_dump_json()
    result = {"native_class": instance.class_name(), "metadata": instance.metadata.model_dump(),
              "model_list": "No network discovery or hardcoded list; caller explicitly selects an available model."}
result.update({"package": package, "version": version(package), "loaded_from": module.__file__,
               "installation": "ordinary package-name pip install from official https://pypi.org/simple",
               "api_key": "dummy only; no API/LLM/media calls", "paid_generation": False})
Path("consumer.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
