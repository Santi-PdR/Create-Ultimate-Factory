import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCE_ROOT = ROOT / "src/main/resources"
recipes = sorted((RESOURCE_ROOT / "data/create_ultimate_factory/recipes").rglob("*.json"))
compat = [path for path in recipes if "/compat/" in path.as_posix()]
assert len(recipes) == 37, f"Expected all 37 source recipes, found {len(recipes)}"
assert len(compat) == 4, f"Expected 4 optional compatibility recipes, found {len(compat)}"


def check_legacy_schema(value, path):
    if isinstance(value, dict):
        forbidden = {"id", "fluid_stack", "processing_time", "heat_requirement"}
        found = forbidden.intersection(value)
        assert not found, f"Unported 1.21 field(s) {sorted(found)} in {path}"
        for child in value.values():
            check_legacy_schema(child, path)
    elif isinstance(value, list):
        for child in value:
            check_legacy_schema(child, path)


def check_recipe_outputs(recipe, path):
    if recipe.get("type") == "forge:conditional":
        for entry in recipe.get("recipes", []):
            check_recipe_outputs(entry.get("recipe", {}), path)
        return
    for result in recipe.get("results", []):
        if "item" in result:
            assert isinstance(result["item"], str), f"Expected string item result in {path}"


conditionals = 0
for path in recipes:
    data = json.loads(path.read_text())
    check_legacy_schema(data, path)
    check_recipe_outputs(data, path)
    if data.get("type") == "forge:conditional":
        conditionals += 1
        assert len(data.get("recipes", [])) == 1, f"Invalid Forge conditional wrapper in {path}"
        assert data["recipes"][0].get("conditions"), f"Missing condition in {path}"
        assert isinstance(data["recipes"][0].get("recipe"), dict), f"Missing wrapped recipe in {path}"
assert conditionals == 7, f"Expected seven mod-gated recipes, found {conditionals}"

tags = sorted((RESOURCE_ROOT / "data/create_ultimate_factory/tags/items").glob("*.json"))
assert len(tags) == 2, f"Expected both source coral item tags, found {len(tags)}"
for path in tags:
    values = json.loads(path.read_text())["values"]
    assert len(values) == 15, f"Unexpected tag membership in {path}"

pack = json.loads((RESOURCE_ROOT / "pack.mcmeta").read_text())
assert pack["pack"]["pack_format"] == 15, "Expected Minecraft 1.20.1 pack format"
print(f"Validated {len(recipes)} recipes ({len(compat)} optional compat), {len(tags)} tags, and 1.20.1 pack metadata.")
