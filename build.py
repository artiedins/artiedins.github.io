import os
import yaml
import re


def slugify(text):
    """Convert text to a URL-friendly slug."""
    return re.sub(r"[^\w\-]", "", text.lower().replace(" ", "-"))


def generate_recipe_pages():
    recipes = []
    recipe_dir = "data"
    output_dir = "recipe_details"

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(recipe_dir):
        if filename.lower().endswith(".yaml"):
            file_path = os.path.join(recipe_dir, filename)
            with open(file_path, "r") as file:
                recipe = yaml.safe_load(file)
                recipes.append(recipe)

            recipe_name = recipe["name"]
            slug = slugify(recipe_name)
            output_file = os.path.join(output_dir, f"{slug}.md")

            with open(output_file, "w") as file:
                file.write(f"# {recipe_name}\n\n")

                file.write("## Ingredients\n\n")
                for ingredient in recipe.get("ingredients", []):
                    file.write(f"- {ingredient}\n")
                file.write("\n")

                file.write("## Equipment\n\n")
                for item in recipe.get("equipment", []):
                    file.write(f"- {item}\n")
                file.write("\n")

                file.write("## Notes\n\n")
                for note in recipe.get("notes", []):
                    file.write(f"- {note}\n")

    # Generate main recipes.md file
    recipes.sort(key=lambda x: x["name"].lower())

    with open("recipes.md", "w") as file:
        file.write("# Recipes\n\n")
        for recipe in recipes:
            recipe_name = recipe["name"]
            slug = slugify(recipe_name)
            file.write(f"- [{recipe_name}]({output_dir}/{slug}.md)\n")


if __name__ == "__main__":
    generate_recipe_pages()
