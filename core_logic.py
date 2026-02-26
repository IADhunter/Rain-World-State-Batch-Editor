import os

def process_line_by_line(input_lines, rules_main, rules_fade, decal_mult, light_mult, 
                        p_a_target, f_a_active, f_a_target, f_a_opacity,
                        grime_mult, clouds_mult, fade_b_opacity):
    new_lines = []
    found_palette = False
    found_fade = False

    try:
        f_b_op_factor = float(fade_b_opacity)
    except:
        f_b_op_factor = 1.0

    for line in input_lines:
        clean_line = line.strip()

        # --- MODULE: PALETTES & FADES ---
        if clean_line.startswith("Palette:"):
            found_palette = True
            val = clean_line.split(":")[1].strip()
            if val in rules_main:
                line = f"Palette: {rules_main[val]}\n"
        
        elif clean_line.startswith("FadePalette:"):
            found_fade = True
            parts = clean_line.split(":")[1].strip().split(",")
            orig_id = parts[0].strip()
            
            if orig_id in rules_fade:
                try:
                    old_op = float(parts[1].strip()) if len(parts) > 1 else 0.1
                    final_op = round(old_op * f_b_op_factor, 7)
                except:
                    final_op = 0.1
                line = f"FadePalette: {rules_fade[orig_id]}, {final_op}\n"
            
            elif f_b_op_factor != 1.0:
                try:
                    old_op = float(parts[1].strip()) if len(parts) > 1 else 0.1
                    line = f"FadePalette: {orig_id}, {round(old_op * f_b_op_factor, 7)}\n"
                except: pass

        # --- MODULE: GRIME & CLOUDS ---
        elif clean_line.startswith("Grime:"):
            try:
                val = float(clean_line.split(":")[1].strip())
                line = f"Grime: {round(val * grime_mult, 7)}\n"
            except: pass

        elif clean_line.startswith("Clouds:"):
            try:
                val = float(clean_line.split(":")[1].strip())
                line = f"Clouds: {round(val * clouds_mult, 7)}\n"
            except: pass

        # --- MODULE: PLACED OBJECTS (Decals & Lights) ---
        elif clean_line.startswith("PlacedObjects:"):
            header_prefix = "PlacedObjects: "
            content = clean_line.replace(header_prefix, "")
            objects = content.split(",")
            processed_objects = []
            
            for obj in objects:
                if not obj.strip(): continue
                
                # Sub-Module: CustomDecals
                if "CustomDecal" in obj:
                    d_parts = obj.split("~")
                    if len(d_parts) > 19:
                        for i in [12, 14, 16, 18]:
                            try:
                                d_parts[i] = str(round(float(d_parts[i]) * decal_mult, 7))
                            except: pass
                        obj = "~".join(d_parts)
                
                # Sub-Module: LightSources
                elif "LightSource" in obj:
                    l_parts = obj.split("~")
                    try:
                        header = l_parts[0].split("><")
                        header[-1] = str(round(float(header[-1]) * light_mult, 7))
                        l_parts[0] = "><".join(header)
                        obj = "~".join(l_parts)
                    except: pass
                
                processed_objects.append(obj)
            line = header_prefix + ",".join(processed_objects) + "\n"

        new_lines.append(line)

    while new_lines and not new_lines[-1].strip():
        new_lines.pop()

    if not found_palette and p_a_target:
        if new_lines and not new_lines[-1].endswith('\n'): new_lines[-1] += '\n'
        new_lines.append(f"Palette: {p_a_target}\n")

    if not found_fade and f_a_active and f_a_target:
        if new_lines and not new_lines[-1].endswith('\n'): new_lines[-1] += '\n'
        new_lines.append(f"FadePalette: {f_a_target}, {f_a_opacity}\n")


    return new_lines
