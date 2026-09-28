# Create: Ultimate Factory — Forge 1.20.1

Unofficial Forge port of Create: Ultimate Factory 2.2.4, adapted from the supplied NeoForge 1.21.1 JAR with permission to port. Original mod and branding by Robin Frt.

This addon is data-driven: it adds 33 recipes for Create processing, plus four optional recipes for Aeronautics, TFMG, and WSTweaks, and the two coral item tags used by the recipes. It requires Minecraft 1.20.1, Forge 47+, and Create.

The 1.20.1 port converts recipe result/fluid schemas, Forge optional-mod conditionals, tag paths, and pack metadata while keeping the recipe IDs, ingredients, outputs, chances, and processing times from the reference JAR.

## Build

Use Java 17 and run `./gradlew build`. The output JAR is in `build/libs/`. GitHub Actions runs the build and validates the converted recipe data.
