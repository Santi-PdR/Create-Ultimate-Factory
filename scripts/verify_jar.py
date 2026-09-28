import json
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
jars = sorted((ROOT / "build/libs").glob("*.jar"))
assert len(jars) == 1, f"Expected one distributable JAR, found {len(jars)}"

with ZipFile(jars[0]) as jar:
    names = set(jar.namelist())
    assert "create_ultimate_factory/CreateUltimateFactoryMod.class" in names
    assert "META-INF/mods.toml" in names
    metadata = jar.read("META-INF/mods.toml").decode()
    assert 'modId="create_ultimate_factory"' in metadata
    assert "${" not in metadata, "Unexpanded metadata placeholder in packaged JAR"
    assert "logo.png" in names

    recipes = sorted(
        name
        for name in names
        if name.startswith("data/create_ultimate_factory/recipes/") and name.endswith(".json")
    )
    assert len(recipes) == 37, f"Expected 37 packaged recipes, found {len(recipes)}"
    conditionals = 0
    for name in recipes:
        data = json.loads(jar.read(name))
        if data.get("type") == "forge:conditional":
            conditionals += 1
        assert "neoforge:" not in jar.read(name).decode(), f"NeoForge condition left in {name}"
    assert conditionals == 7, f"Expected seven packaged optional recipes, found {conditionals}"

    tags = {
        "data/create_ultimate_factory/tags/items/corals.json",
        "data/create_ultimate_factory/tags/items/dead_corals.json",
    }
    assert tags <= names, "One or more converted coral item tags are missing"
    pack = json.loads(jar.read("pack.mcmeta"))
    assert pack["pack"]["pack_format"] == 15

print(f"Verified packaged JAR {jars[0].name}: entry point, metadata, 37 recipes, 2 tags, and 1.20.1 pack format.")
