import os
import sys
import yaml

def List_templates(designs_dir = "./designs"):
    

    if not os.path.isdir(designs_dir):
        print(f"Directory not found: {designs_dir}")
        sys.exit(1)
    yaml_files = [
        f for f in os.listdir(designs_dir)
        if f.lower().endswith((".yaml", ".yml"))
    ]

    if not yaml_files:
        print("No YAML files found in ./designs")
        return
    
    print("\nYAML files in ./designs:")
    for idx, filename in enumerate(yaml_files, start=1):
        print(f"{idx}. {filename}")
    
    return yaml_files

def get_selected_template(design_index=None):
    try:
        designs_dir = "./designs"
        yaml_file = List_templates(designs_dir)

        if design_index is None:
            selected_desing = input("please select a design: ")
        else:
            selected_desing = str(design_index)

        try:
            selection_idx = int(selected_desing) - 1
        except ValueError:
            print("invalid input type")
            raise TypeError

        if selection_idx < 0 or selection_idx >= len(yaml_file):
            raise ValueError

        selected_file_name = yaml_file[selection_idx]
        
        return selected_file_name,selected_desing


    except ValueError:
        print("Invalid selection.")
        sys.exit(1)
    except TypeError:
        print("Type error occured")
        sys.exit(1)
    

