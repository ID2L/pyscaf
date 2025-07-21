from pathlib import Path

import tomli
import tomli_w


def merge_toml_files(input_path: Path, output_path: Path):
    """
    Merges all content from input_path TOML file into output_path TOML file.
    Recursively merges sections and avoids duplicates by intelligently combining content.
    """
    # Read files
    input_data = {}
    output_data = {}
    if input_path.exists():
        with open(input_path, "rb") as f:
            input_data = tomli.load(f)
    if output_path.exists():
        with open(output_path, "rb") as f:
            output_data = tomli.load(f)

    def deep_merge(source, destination):
        """
        Recursively merge source dict into destination dict.
        For lists, extend them. For other types, source overwrites destination.
        """
        for key, value in source.items():
            if key in destination:
                if isinstance(destination[key], dict) and isinstance(value, dict):
                    # Both are dicts, merge recursively
                    deep_merge(value, destination[key])
                elif isinstance(destination[key], list) and isinstance(value, list):
                    # Both are lists, extend destination with new items
                    for item in value:
                        if item not in destination[key]:
                            print(f"Adding {item} to {key}\n")
                            destination[key].append(item)
                else:
                    # Source overwrites destination for other types
                    print(f"Overwriting {key} with {value}\n")
                    destination[key] = value
            else:
                # Key doesn't exist in destination, add it
                print(f"Adding {key} to {destination}\n")
                destination[key] = value

    # Merge all content from input into output
    deep_merge(input_data, output_data)

    # Write output file
    with open(output_path, "wb") as f:
        tomli_w.dump(output_data, f)
