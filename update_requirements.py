#!/usr/bin/env python3
# Script to add test dependencies to requirements.txt

requirements_file = "/workspaces/skills-getting-started-with-github-copilot/requirements.txt"
new_deps = ["pytest", "pytest-asyncio"]

# Read existing requirements
with open(requirements_file, "r") as f:
    existing = f.read().strip().split("\n")

# Add new dependencies if not already present
for dep in new_deps:
    if dep not in existing:
        existing.append(dep)

# Write updated requirements
with open(requirements_file, "w") as f:
    f.write("\n".join(existing) + "\n")

print("✓ Updated requirements.txt with pytest dependencies")
