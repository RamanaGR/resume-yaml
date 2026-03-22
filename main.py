import os
import sys
import yaml
import shutil
import subprocess
from datetime import datetime
from read_templates import get_selected_template

def process_resume(selected_desing, output_filename, output_file_path=None):
    if output_file_path:
        output_dir = os.path.dirname(os.path.abspath(output_file_path))
        source_dir = os.path.join(output_dir, "rendercv_output")
    else:
        source_dir = "./rendercv_output"
    
    target_dir = f"./resumes/{output_filename}"
    timestamp = datetime.now().strftime("%y-%m-%d-%H-%M")
    if not output_filename.endswith('.pdf'):
        output_filename = f"{timestamp}_{output_filename}_d{selected_desing}.pdf"

    os.makedirs(target_dir, exist_ok=True)

    if not os.path.isdir(source_dir):
        # Fallback check for flat structure if rendercv output changed
        if os.path.exists(output_file_path.replace(".yaml", ".pdf")):
             source_pdf = output_file_path.replace(".yaml", ".pdf")
             new_path = os.path.join(target_dir, output_filename)
             shutil.move(source_pdf, new_path)
             print(f"Processed PDF moved to {new_path}")
             return
        else:
             raise FileNotFoundError(f"{source_dir} does not exist and PDF not found.")

    pdf_file = None
    for f in os.listdir(source_dir):
        if f.lower().endswith(".pdf"):
            pdf_file = f
            break

    if pdf_file is None:
        raise FileNotFoundError("No PDF file found in rendercv_output")

    old_path = os.path.join(source_dir, pdf_file)
    new_path = os.path.join(target_dir, output_filename)
    shutil.move(old_path, new_path)
    shutil.rmtree(source_dir)
    print(f"Processed PDF moved to {new_path}")

def merge_dicts(a, b):
    result = a.copy()
    result.update(b)
    return result

def build_resume(output_path):
    print(f"Processing output file at: {output_path}")
    print(f"\nRunning: rendercv render {output_path}")
    try:
        # Added --dont-open-browser to prevent auto-opening
        result = subprocess.run(
            ["rendercv", "render", output_path],
            check=True,
            text=True,
            capture_output=True
        )
        print("Command output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error while running rendercv:")
        print("STDERR:", e.stderr)
        raise

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_yaml_file> <outputfilename> [design_index] [max_highlights]")
        sys.exit(1)

    input_yaml_path = sys.argv[1]
    ouput_File_name = sys.argv[2]
    design_index = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    # Optional: maximum number of bullets to keep per `highlights` list
    max_highlights = int(sys.argv[4]) if len(sys.argv) > 4 else None

    # Load Data
    with open(input_yaml_path, "r", encoding="utf-8") as f:
        data_dict = yaml.safe_load(f)

    # Load Design
    cwd = os.getcwd()
    selected_file_name, selected_Design = get_selected_template(design_index)
    selected_path = os.path.join(cwd, "designs", selected_file_name)

    with open(selected_path, "r", encoding="utf-8") as f:
        design_dict = yaml.safe_load(f)

    # ---- Extract v2.6 compatible fields from design file (NO HARDCODING) ----
    compatible_design = {}
    
    if 'design' in design_dict:
        design_section = design_dict['design']
        compatible_design['design'] = {}
        
        # Extract theme (required)
        if 'theme' in design_section:
            compatible_design['design']['theme'] = design_section['theme']
            
        # Extract entries configuration (fix for page breaks)
        if 'entries' in design_section:
            compatible_design['design']['entries'] = design_section['entries']
        
        # Extract page settings
        if 'page' not in compatible_design['design']:
            compatible_design['design']['page'] = {}

        # Note: show_page_numbering is not supported in rendercv v2.6, so we skip it
        # Page numbering is controlled by the theme, not a design setting
        
        # Map disable_last_updated_date to show_top_note
        if 'disable_last_updated_date' in design_section:
            compatible_design['design']['page']['show_top_note'] = not design_section['disable_last_updated_date']
        
        # Extract margins and map to page settings
        if 'margins' in design_section:
            margins = design_section['margins']
            if 'page_top' in margins:
                compatible_design['design']['page']['top_margin'] = margins['page_top']
            if 'page_bottom' in margins:
                compatible_design['design']['page']['bottom_margin'] = margins['page_bottom']
            if 'page_left' in margins:
                compatible_design['design']['page']['left_margin'] = margins['page_left']
            if 'page_right' in margins:
                compatible_design['design']['page']['right_margin'] = margins['page_right']
            
            # Map entry_area_vertical_between to sections.space_between_regular_entries
            if 'entry_area_vertical_between' in margins:
                if 'sections' not in compatible_design['design']:
                    compatible_design['design']['sections'] = {}
                compatible_design['design']['sections']['space_between_regular_entries'] = margins['entry_area_vertical_between']
            
            # Note: highlights_area_vertical_between is not directly supported in v2.6
            # This setting would need to be handled via theme customization
        
        # Extract header settings
        if 'header' in design_section:
            if 'header' not in compatible_design['design']:
                compatible_design['design']['header'] = {}
            
            # Extract header alignment
            if 'alignment' in design_section['header']:
                compatible_design['design']['header']['alignment'] = design_section['header']['alignment']
            
            # Extract entry_area_vertical_between from header (if not already set from margins)
            if 'entry_area_vertical_between' in design_section['header']:
                if 'sections' not in compatible_design['design']:
                    compatible_design['design']['sections'] = {}
                if 'space_between_regular_entries' not in compatible_design['design']['sections']:
                    compatible_design['design']['sections']['space_between_regular_entries'] = design_section['header']['entry_area_vertical_between']
            
            # Extract connections settings
            if 'connections' in design_section['header']:
                if 'connections' not in compatible_design['design']['header']:
                    compatible_design['design']['header']['connections'] = {}
                connections = design_section['header']['connections']
                if 'show_icons' in connections:
                    compatible_design['design']['header']['connections']['show_icons'] = connections['show_icons']
                if 'separator' in connections:
                    compatible_design['design']['header']['connections']['separator'] = connections['separator']
                if 'hyperlink' in connections:
                    compatible_design['design']['header']['connections']['hyperlink'] = connections['hyperlink']
                if 'display_urls_instead_of_usernames' in connections:
                    compatible_design['design']['header']['connections']['display_urls_instead_of_usernames'] = connections['display_urls_instead_of_usernames']

            # Note: do not copy arbitrary header keys into the compatible design
            # because rendercv v2.6 schema will reject unknown fields. Only
            # connection-related keys are passed above; other header styling
            # (font/spacing) is controlled via the theme or should be handled
            # in templates rather than injected here.
    
    # Preserve locale if present (v2.6 compatible)
    if 'locale' in design_dict:
        locale = design_dict['locale']
        language_map = {
            'en': 'english', 'da': 'danish', 'fr': 'french', 'de': 'german',
            'hi': 'hindi', 'id': 'indonesian', 'it': 'italian', 'ja': 'japanese',
            'ko': 'korean', 'zh': 'mandarin_chineese', 'pt': 'portuguese',
            'ru': 'russian', 'es': 'spanish', 'tr': 'turkish'
        }
        if 'language' in locale:
            lang_value = locale['language']
            if lang_value in language_map:
                lang_value = language_map[lang_value]
            compatible_design['locale'] = {'language': lang_value}
    
    # Preserve rendercv_settings if present
    if 'rendercv_settings' in design_dict:
        compatible_design['rendercv_settings'] = design_dict['rendercv_settings']
    elif 'settings' in design_dict:
        compatible_design['settings'] = design_dict['settings']
    
    # Merge
    merged_dict = merge_dicts(data_dict, compatible_design)
    
    # Clean up None values and invalid fields before writing
    def remove_none_values(d):
        """Recursively remove None values and invalid fields from dictionary"""
        if isinstance(d, dict):
            cleaned = {}
            for k, v in d.items():
                # Remove sort_entries from sections (not supported in v2.6)
                if k == 'sort_entries' and isinstance(v, str) and v == 'none':
                    continue
                if v is not None:
                    cleaned[k] = remove_none_values(v)
            return cleaned
        elif isinstance(d, list):
            return [remove_none_values(item) for item in d]
        else:
            return d
    
    cleaned_dict = remove_none_values(merged_dict)

    def trim_highlights(cv_dict, max_n: int):
        """Trim `highlights` lists on all section entries to at most max_n items."""
        if not max_n:
            return
        cv = cv_dict.get('cv') or {}
        sections = cv.get('sections') or {}
        for section_name, entries in sections.items():
            if not isinstance(entries, list):
                continue
            for entry in entries:
                if isinstance(entry, dict) and 'highlights' in entry and isinstance(entry['highlights'], list):
                    entry['highlights'] = entry['highlights'][:max_n]

    # Apply trimming if requested by CLI
    if max_highlights is not None:
        trim_highlights(cleaned_dict, max_highlights)

    # Output
    timestamp = datetime.now().strftime("%d-%m-%H-%M")
    output_folder = f"./output/file_{selected_file_name}_{timestamp}"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, selected_file_name)

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(cleaned_dict, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    build_resume(output_file)
    process_resume(selected_Design, ouput_File_name, output_file)

if __name__ == "__main__":
    main()