import customtkinter as ctk
from PIL import Image
import os
import sys
import core_logic as core

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, "internal", relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def get_external_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

class RuleRow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=0, **kwargs)
        self.entry_old = ctk.CTkEntry(self, width=66, height=22, corner_radius=0)
        self.entry_old.pack(side="left", padx=2)
        ctk.CTkLabel(self, text="To").pack(side="left", padx=2)
        self.entry_new = ctk.CTkEntry(self, width=66, height=22, corner_radius=0)
        self.entry_new.pack(side="left", padx=2)
        self.btn_del = ctk.CTkButton(self, text="-", width=24, height=22, 
                                     fg_color="#663333", corner_radius=0, command=self.destroy)
        self.btn_del.pack(side="left", padx=5)

class RWNexusApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RWSBE")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.app_dir = get_external_path()
        self.input_path = os.path.join(self.app_dir, "input")
        self.output_path = os.path.join(self.app_dir, "output")
        
        for folder in [self.input_path, self.output_path]:
            if not os.path.exists(folder): 
                os.makedirs(folder)

        self.bg_path = get_resource_path("background.jpg")

        self.rows_main_b = [] 
        self.rows_fade_b = [] 

        try:
            self.bg_img_raw = Image.open(self.bg_path)
            self.bg_img = ctk.CTkImage(light_image=self.bg_img_raw, size=(1000, 650))
            ctk.CTkLabel(self, image=self.bg_img, text="").place(x=0, y=0, relwidth=1, relheight=1)
        except: 
            pass
            
        self.frame_pa = ctk.CTkFrame(self, width=480, height=50, corner_radius=0, fg_color="#254f12")
        self.frame_pa.place(x=262, y=20)
        ctk.CTkLabel(self.frame_pa, text="Rain World States Batch Editor", font=("Trebuchet MS", 32, "bold")).place(x=10, y=5)

        self.console_log = ctk.CTkLabel(self, text="🍉 Init 🍉", font=("Trebuchet MS", 15), 
                                        width=240, height=30, text_color="#aaaaaa", fg_color="#1a1a1a", corner_radius=0)

        self.init_ui_elements()

    def init_ui_elements(self):
        ctk.CTkLabel(self, text="By IADhunter", font=("Trebuchet MS", 15), text_color="White").place(x=10, y=600)
        
        self.frame_pa = ctk.CTkFrame(self, width=440, height=40, corner_radius=0, fg_color="#254f12")
        self.frame_pa.place(x=40, y=110)
        ctk.CTkLabel(self.frame_pa, text="Palette Control", font=("Trebuchet MS", 20, "bold")).place(x=10, y=5)

        self.frame_pa = ctk.CTkFrame(self, width=210, height=110, corner_radius=0, fg_color="#444444")
        self.frame_pa.place(x=40, y=160)
        ctk.CTkLabel(self.frame_pa, text="main palette A").place(x=10, y=5)
        self.ent_pa_new = ctk.CTkEntry(self.frame_pa, width=120, corner_radius=0, placeholder_text="ID")
        self.ent_pa_new.place(x=10, y=40)

        self.frame_fa = ctk.CTkFrame(self, width=210, height=110, corner_radius=0, fg_color="#444444")
        self.frame_fa.place(x=270, y=160)
        self.sw_fade_a = ctk.CTkSwitch(self.frame_fa, text="fade palette A", progress_color="#254f12")
        self.sw_fade_a.place(x=10, y=5)
        self.ent_fa_new = ctk.CTkEntry(self.frame_fa, width=120, corner_radius=0, placeholder_text="ID")
        self.ent_fa_new.place(x=10, y=40)
        self.ent_fade_opacity = ctk.CTkEntry(self.frame_fa, width=50, corner_radius=0)
        self.ent_fade_opacity.insert(0, "0.1")
        self.ent_fade_opacity.place(x=148, y=40)

        self.btn_add_b1 = ctk.CTkButton(self, text="+ main palette B", width=210, corner_radius=0, fg_color="#a92446", command=lambda: self.add_rule_row(self.scroll_b1, self.rows_main_b))
        self.btn_add_b1.place(x=40, y=275)
        self.scroll_b1 = ctk.CTkScrollableFrame(self, width=194, height=205, corner_radius=0, fg_color="#2b2b2b")
        self.scroll_b1.place(x=40, y=343)
        self.btn_clear_b1 = ctk.CTkButton(self, text="Clear", width=210, height=22, fg_color="#443333", hover_color="#662222", corner_radius=0, command=lambda: self.clear_rules(self.rows_main_b))
        self.btn_clear_b1.place(x=40, y=555)
 
        self.btn_add_b2 = ctk.CTkButton(self, text="+ fade palette B", width=210, corner_radius=0, fg_color="#a92446", command=lambda: self.add_rule_row(self.scroll_b2, self.rows_fade_b))
        self.btn_add_b2.place(x=270, y=275)
        self.frame_fb_op = ctk.CTkFrame(self, width=210, height=30, corner_radius=0, fg_color="#444444")
        self.frame_fb_op.place(x=270, y=303)
        ctk.CTkLabel(self.frame_fb_op, text="Opacity:", font=("Trebuchet MS", 12)).place(x=10, y=1)
        self.ent_fade_b_opacity = ctk.CTkEntry(self.frame_fb_op, width=50, height=22, corner_radius=0)
        self.ent_fade_b_opacity.insert(0, "1.0")
        self.ent_fade_b_opacity.place(x=148, y=4)

        self.scroll_b2 = ctk.CTkScrollableFrame(self, width=194, height=205, corner_radius=0, fg_color="#2b2b2b")
        self.scroll_b2.place(x=270, y=343)
        self.btn_clear_b2 = ctk.CTkButton(self, text="Clear", width=210, height=22, fg_color="#443333", hover_color="#662222", corner_radius=0, command=lambda: self.clear_rules(self.rows_fade_b))
        self.btn_clear_b2.place(x=270, y=555)
        
        self.frame_obj = ctk.CTkFrame(self, width=240, height=40, corner_radius=0, fg_color="#254f12")
        self.frame_obj.place(x=720, y=110)
        ctk.CTkLabel(self.frame_obj, text="Ambient Control", font=("Trebuchet MS", 20, "bold")).place(x=10, y=5)
        
        self.frame_obj = ctk.CTkFrame(self, width=240, height=190, corner_radius=0, fg_color="#333333")
        self.frame_obj.place(x=720, y=160)
        
        ctk.CTkLabel(self.frame_obj, text="Decal Intensity:").place(x=15, y=15)
        self.ent_decal_mult = ctk.CTkEntry(self.frame_obj, width=65, corner_radius=0)
        self.ent_decal_mult.insert(0, "1.0")
        self.ent_decal_mult.place(x=150, y=15)
        
        ctk.CTkLabel(self.frame_obj, text="LightS Intensity:").place(x=15, y=55)
        self.ent_light_mult = ctk.CTkEntry(self.frame_obj, width=65, corner_radius=0)
        self.ent_light_mult.insert(0, "1.0")
        self.ent_light_mult.place(x=150, y=55)

        ctk.CTkLabel(self.frame_obj, text="Grime Intensity:").place(x=15, y=95)
        self.ent_grime_mult = ctk.CTkEntry(self.frame_obj, width=65, corner_radius=0)
        self.ent_grime_mult.insert(0, "1.0")
        self.ent_grime_mult.place(x=150, y=95)

        ctk.CTkLabel(self.frame_obj, text="Clouds Intensity:").place(x=15, y=135)
        self.ent_clouds_mult = ctk.CTkEntry(self.frame_obj, width=65, corner_radius=0)
        self.ent_clouds_mult.insert(0, "1.0")
        self.ent_clouds_mult.place(x=150, y=135)

        self.console_log.place(x=720, y=365)

        ctk.CTkButton(self, text="input", width=115, height=32, corner_radius=0, fg_color="#a92446", command=lambda: os.startfile(self.input_path)).place(x=720, y=540)
        ctk.CTkButton(self, text="output", width=115, height=32, corner_radius=0, fg_color="#a92446", command=lambda: os.startfile(self.output_path)).place(x=845, y=540)
        ctk.CTkButton(self, text="Generate", width=240, height=50, corner_radius=0, font=("Trebuchet MS", 18, "bold"), fg_color="#254f12", command=self.run_process).place(x=720, y=480)

    def add_rule_row(self, scroll_target, registry):
        new_row = RuleRow(scroll_target)
        new_row.pack(pady=2, fill="x")
        registry.append(new_row)

    def clear_rules(self, registry):
        for row in registry:
            if row.winfo_exists():
                row.destroy()
        registry.clear()

    def run_process(self):
        try:
            d_mult = float(self.ent_decal_mult.get())
            l_mult = float(self.ent_light_mult.get())
            g_mult = float(self.ent_grime_mult.get())
            c_mult = float(self.ent_clouds_mult.get())
            fb_opacity = self.ent_fade_b_opacity.get().strip()

            rules_main = {r.entry_old.get().strip(): r.entry_new.get().strip() for r in self.rows_main_b if r.winfo_exists() and r.entry_old.get().strip()}
            rules_fade = {r.entry_old.get().strip(): r.entry_new.get().strip() for r in self.rows_fade_b if r.winfo_exists() and r.entry_old.get().strip()}
            
            target_files = [f for f in os.listdir(self.input_path) if f.endswith(".txt")]
            processed = 0
            
            for file_name in target_files:
                with open(os.path.join(self.input_path, file_name), 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                result = core.process_line_by_line(
                    lines, rules_main, rules_fade, d_mult, l_mult, 
                    self.ent_pa_new.get().strip(), self.sw_fade_a.get(), 
                    self.ent_fa_new.get().strip(), self.ent_fade_opacity.get().strip(),
                    g_mult, c_mult, fb_opacity
                )
                
                with open(os.path.join(self.output_path, file_name), 'w', encoding='utf-8') as f:
                    f.writelines(result)
                processed += 1
            
            self.console_log.configure(text=f"🍉 Success: {processed} Settings 🍉", text_color="green")
        except Exception as e: self.console_log.configure(text=f"Error: {e}", text_color="red")

if __name__ == "__main__":
    app = RWNexusApp()
    app.mainloop()