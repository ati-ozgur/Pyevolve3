from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parent
EXAMPLES_DIR = SOURCE_DIR.parents[1] / "examples"
OUTPUT_FILE = SOURCE_DIR / "examples.md"


def main() -> None:
    example_files = sorted(EXAMPLES_DIR.glob("pyevolve_ex*.py"))
    if not example_files:
        raise FileNotFoundError(f"No example files found in {EXAMPLES_DIR}")

    sections = [
        "# Examples",
        "",
        "All the examples can be downloaded from the [download sec](intro.md#download_sec) section, **they are not**",
        "included in the installation package.",
        "",
    ]

    for example_file in example_files:
        title = example_file.stem.removeprefix("pyevolve_").replace("_", " ")
        title = title.replace("ex", "Example").replace("ga", "Genetic Algorithm").replace("tsp", "Traveling Sales Person")
        title = title.title()
        relative_path = example_file.relative_to(SOURCE_DIR.parents[1]).as_posix()
        include_path = f"../../{relative_path}"
        sections.extend(
            [
                f"## {title}",
                "",
                f"Filename: `{relative_path}`",
                "",
                "```python",
                "",
                f"{{{{< include {include_path} >}}}}",
                "",
                "```",
                "",
            ]
        )

    OUTPUT_FILE.write_text("\n".join(sections), encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with {len(example_files)} examples.")


if __name__ == "__main__":
    main()
