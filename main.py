"""
main.py - Main application file with separate skill columns
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Classes import DataManager

class MHWBuilderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MHW Skill Builder")
        self.root.geometry("1600x900")
        
        # Load all data
        self.data_manager = DataManager("data")
        self.data_manager.load_all_data()
        
        # Selected skills: skill name -> desired level
        self.selected_skills = {}
        
        # Store references to skill widgets for easy removal
        self.skill_widgets = {}
        
        self.create_ui()
        self.root.mainloop()
    
    def create_ui(self):
        """Create the 4-section layout with split skill columns"""
        # ========== SECTION 1: TOP BAR ==========
        top_bar = tk.Frame(self.root, height=50, bg="#2c3e50")
        top_bar.pack(side="top", fill="x")
        top_bar.pack_propagate(False)
        
        tk.Label(top_bar, text="⚔️ Monster Hunter Skill Builder", 
                font=("Arial", 18, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(side="left", padx=20)
        
        # ========== MAIN AREA ==========
        main_pane = tk.PanedWindow(self.root, orient="horizontal", sashwidth=10)
        main_pane.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left column (split)
        left_pane = tk.PanedWindow(main_pane, orient="vertical", sashwidth=6)
        
        # SECTION 2A: Skill Selection with TWO columns
        section_2a = self.create_skill_selection_section()
        left_pane.add(section_2a, minsize=400)
        
        # SECTION 2B: Level Selection
        section_2b = self.create_level_selection_section()
        left_pane.add(section_2b, minsize=250)
        
        # SECTION 3: Build Results
        section_3 = self.create_build_results_section()
        
        # SECTION 4: Selected Skills
        section_4 = self.create_selected_skills_section()
        
        # Assemble
        main_pane.add(left_pane, minsize=500)
        main_pane.add(section_3, minsize=600)
        main_pane.add(section_4, minsize=300)
    
    def create_skill_selection_section(self):
        """SECTION 2A: Two-column skill selection"""
        frame = tk.Frame(bg="white", relief="ridge", bd=2)
        
        # Title
        title_frame = tk.Frame(frame, bg="#3498db")
        title_frame.pack(fill="x", pady=(0, 10))
        tk.Label(title_frame, text="🎯 SELECT SKILLS", 
                font=("Arial", 14, "bold"), bg="#3498db", fg="white").pack(pady=10)
        
        # Search bar
        search_frame = tk.Frame(frame, bg="white")
        search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg="white").pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<KeyRelease>", self.on_search_changed)
        
        # Skill type filter for regular skills
        tk.Label(search_frame, text="Type:", bg="white").pack(side="left", padx=(20, 5))
        
        self.type_var = tk.StringVar(value="All")
        type_menu = ttk.Combobox(search_frame, textvariable=self.type_var, 
                                values=["All", "Attack", "Defense", "Utility", "Other"],
                                state="readonly", width=12)
        type_menu.pack(side="left", padx=5)
        type_menu.bind("<<ComboboxSelected>>", self.on_type_changed)
        
        # Clear search button
        tk.Button(search_frame, text="X", width=3,
                 command=self.clear_search).pack(side="left", padx=5)
        
        # ========== TWO COLUMN LAYOUT ==========
        columns_frame = tk.Frame(frame, bg="white")
        columns_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)
        columns_frame.grid_rowconfigure(0, weight=1)
        
        # COLUMN 1: Regular Skills
        regular_frame = tk.Frame(columns_frame, bg="white", relief="groove", bd=1)
        regular_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        reg_title = tk.Frame(regular_frame, bg="#2980b9", height=30)
        reg_title.pack(fill="x", pady=(0, 5))
        reg_title.pack_propagate(False)
        
        tk.Label(reg_title, text="🛡️ REGULAR SKILLS", 
                font=("Arial", 11, "bold"), bg="#2980b9", fg="white").pack(pady=5)
        
        reg_list_frame = tk.Frame(regular_frame, bg="white")
        reg_list_frame.pack(fill="both", expand=True)
        
        self.regular_listbox = tk.Listbox(reg_list_frame, height=20, font=("Arial", 10))
        reg_scrollbar = tk.Scrollbar(reg_list_frame, command=self.regular_listbox.yview)
        self.regular_listbox.config(yscrollcommand=reg_scrollbar.set)
        
        self.regular_listbox.bind("<Double-Button-1>", 
                                 lambda e: self.add_selected_skill(from_regular=True))
        
        self.regular_listbox.pack(side="left", fill="both", expand=True)
        reg_scrollbar.pack(side="right", fill="y")
        
        # COLUMN 2: Group & Set Bonus Skills
        special_frame = tk.Frame(columns_frame, bg="white", relief="groove", bd=1)
        special_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        spec_title = tk.Frame(special_frame, bg="#8e44ad", height=30)
        spec_title.pack(fill="x", pady=(0, 5))
        spec_title.pack_propagate(False)
        
        tk.Label(spec_title, text="👥 GROUP & SET BONUS SKILLS", 
                font=("Arial", 11, "bold"), bg="#8e44ad", fg="white").pack(pady=5)
        
        spec_list_frame = tk.Frame(special_frame, bg="white")
        spec_list_frame.pack(fill="both", expand=True)
        
        self.special_listbox = tk.Listbox(spec_list_frame, height=20, font=("Arial", 10))
        spec_scrollbar = tk.Scrollbar(spec_list_frame, command=self.special_listbox.yview)
        self.special_listbox.config(yscrollcommand=spec_scrollbar.set)
        
        self.special_listbox.bind("<Double-Button-1>", 
                                 lambda e: self.add_selected_skill(from_regular=False))
        
        self.special_listbox.pack(side="left", fill="both", expand=True)
        spec_scrollbar.pack(side="right", fill="y")
        
        # DEBUG: Print skill counts
        print(f"DEBUG: Total skills loaded: {len(self.data_manager.skills)}")
        
        # Populate both lists
        self.update_skill_lists()
        
        return frame
    
    def create_level_selection_section(self):
        """SECTION 2B: Level selection area"""
        frame = tk.Frame(bg="white", relief="ridge", bd=2)
        
        title_frame = tk.Frame(frame, bg="#e74c3c")
        title_frame.pack(fill="x", pady=(0, 10))
        tk.Label(title_frame, text="📊 SET SKILL LEVELS", 
                font=("Arial", 14, "bold"), bg="#e74c3c", fg="white").pack(pady=10)
        
        self.level_widgets_frame = tk.Frame(frame, bg="white")
        self.level_widgets_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(self.level_widgets_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.level_widgets_frame, orient="vertical", command=canvas.yview)
        self.scrollable_level_frame = tk.Frame(canvas, bg="white")
        
        self.scrollable_level_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_level_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return frame
    
    def create_build_results_section(self):
        """SECTION 3: Build results display"""
        frame = tk.Frame(bg="#ecf0f1", relief="ridge", bd=2)
        
        title_frame = tk.Frame(frame, bg="#2c3e50")
        title_frame.pack(fill="x", pady=(0, 10))
        tk.Label(title_frame, text="🛡️ BUILD RESULTS", 
                font=("Arial", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
        
        self.results_text = tk.Text(frame, height=30, width=70,
                                   font=("Consolas", 10), wrap="word")
        scrollbar = tk.Scrollbar(frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        self.results_text.insert("1.0", "Builds will appear here...")
        self.results_text.config(state="disabled")
        
        return frame
    
    def create_selected_skills_section(self):
        """SECTION 4: Selected skills display"""
        frame = tk.Frame(bg="white", relief="ridge", bd=2)
        
        title_frame = tk.Frame(frame, bg="#27ae60")
        title_frame.pack(fill="x", pady=(0, 10))
        tk.Label(title_frame, text="📋 SELECTED SKILLS", 
                font=("Arial", 14, "bold"), bg="#27ae60", fg="white").pack(pady=10)
        
        self.selected_display = tk.Text(frame, height=20, width=30,
                                       font=("Consolas", 10))
        self.selected_display.pack(fill="both", expand=True, padx=10, pady=10)
        self.selected_display.insert("1.0", "No skills selected")
        self.selected_display.config(state="disabled")
        
        tk.Label(frame, text="Build Requirements:", 
                font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.stats_label = tk.Label(frame, text="Skills: 0\nTotal Levels: 0", 
                                   justify="left", anchor="w")
        self.stats_label.pack(fill="x", padx=10, pady=5)
        
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="Find Builds", bg="#3498db", fg="white",
                 command=self.find_builds).pack(side="left")
        tk.Button(btn_frame, text="Clear All", bg="#e74c3c", fg="white",
                 command=self.clear_all).pack(side="right")
        
        return frame
    
    # ========== EVENT HANDLERS ==========
    
    def on_search_changed(self, event=None):
        self.update_skill_lists()
    
    def on_type_changed(self, event=None):
        self.update_skill_lists()
    
    def clear_search(self):
        self.search_var.set("")
        self.type_var.set("All")
        self.update_skill_lists()
    
    def update_skill_lists(self):
        """Update both skill listboxes - FIXED VERSION"""
        # Clear both lists
        self.regular_listbox.delete(0, tk.END)
        self.special_listbox.delete(0, tk.END)
        
        search_term = self.search_var.get().strip().lower()
        skill_type = self.type_var.get()
        
        # DEBUG: Count skills by type
        type_counts = {}
        for skill in self.data_manager.skills.values():
            skill_type_name = skill.skill_type
            type_counts[skill_type_name] = type_counts.get(skill_type_name, 0) + 1
        
        print(f"DEBUG: Skill counts by type: {type_counts}")
        
        # Get all skills organized
        regular_skills = []
        special_skills = []
        
        for skill in self.data_manager.skills.values():
            # Apply search filter
            if search_term and search_term not in skill.name.lower():
                continue
            
            # Categorize skills
            if skill.skill_type == "Group" or skill.skill_type == "SetBonus":
                special_skills.append(skill)
            else:
                # Apply type filter for regular skills
                if skill_type != "All" and skill.skill_type != skill_type:
                    continue
                regular_skills.append(skill)
        
        print(f"DEBUG: Found {len(regular_skills)} regular skills, {len(special_skills)} special skills")
        
        # Sort all lists alphabetically
        regular_skills.sort(key=lambda s: s.name)
        special_skills.sort(key=lambda s: s.name)
        
        # Add regular skills to regular listbox
        for skill in regular_skills:
            self.regular_listbox.insert(tk.END, skill.name)
        
        # Add special skills to special listbox with appropriate icons
        for skill in special_skills:
            icon = "👥 " if skill.skill_type == "Group" else "⭐ "
            display_text = f"{icon}{skill.name}"
            
            # Add type indicator in parentheses
            if skill.skill_type == "Group":
                display_text += " (Group)"
            elif skill.skill_type == "SetBonus":
                display_text += " (Set Bonus)"
            
            self.special_listbox.insert(tk.END, display_text)
    
    def get_selected_skill_name(self, from_regular: bool = True) -> str:
        """Get the selected skill name from appropriate listbox"""
        if from_regular:
            selection = self.regular_listbox.curselection()
            if not selection:
                return None
            return self.regular_listbox.get(selection[0])
        else:
            selection = self.special_listbox.curselection()
            if not selection:
                return None
            # Extract skill name from display text (remove icon and type indicator)
            display_text = self.special_listbox.get(selection[0])
            # Remove icon and anything in parentheses
            skill_name = display_text.replace("👥 ", "").replace("⭐ ", "")
            skill_name = skill_name.split(" (")[0].strip()
            return skill_name
    
    def add_selected_skill(self, from_regular: bool = True):
        """Add selected skill from appropriate listbox"""
        skill_name = self.get_selected_skill_name(from_regular)
        if not skill_name:
            messagebox.showwarning("No Skill Selected", 
                                 f"Please select a skill from the {'regular' if from_regular else 'special'} list")
            return
        
        skill = self.data_manager.get_skill(skill_name)
        
        if not skill:
            messagebox.showerror("Error", f"Could not find skill: {skill_name}")
            return
        
        # Check if already added
        if skill_name in self.selected_skills:
            messagebox.showinfo("Already Added", f"{skill_name} is already selected")
            return
        
        # Create level selection widget
        widget_info = self.create_skill_level_widget(skill)
        
        # Add to selected skills (default level 1)
        self.selected_skills[skill_name] = 1
        
        # Store widget info for later removal
        self.skill_widgets[skill_name] = {
            'skill': skill,
            'frame': widget_info['frame'],
            'level_display': widget_info['level_display'],
            'indicators': widget_info['indicators']
        }
        
        # Update section 4
        self.update_selected_display()
    
    def create_skill_level_widget(self, skill):
        """Create widget for selecting skill level"""
        frame = tk.Frame(self.scrollable_level_frame, bg="white")
        frame.pack(fill="x", pady=5, padx=5)
        
        # Skill name with appropriate icon
        display_name = skill.name
        icon = ""
        if skill.skill_type == "Group":
            icon = "👥 "
        elif skill.skill_type == "SetBonus":
            icon = "⭐ "
        
        tk.Label(frame, text=f"{icon}{display_name}", width=24, anchor="w", 
                font=("Arial", 10)).pack(side="left")
        
        # Level display
        level_display = tk.Label(frame, text="Lv1", width=5,
                                font=("Arial", 10, "bold"), fg="#e74c3c")
        level_display.pack(side="right", padx=5)
        
        # Remove button
        remove_btn = tk.Button(frame, text="✕", font=("Arial", 8), 
                              bg="#e74c3c", fg="white", width=3,
                              command=lambda s=skill.name: self.remove_skill(s))
        remove_btn.pack(side="right", padx=2)
        
        # Level indicators (circles)
        indicators_frame = tk.Frame(frame, bg="white")
        indicators_frame.pack(side="left", padx=10)
        
        # Create clickable circles for each level
        indicators = []
        for i in range(skill.max_level):
            indicator = tk.Label(indicators_frame, text="○", font=("Arial", 16),
                               fg="gray", cursor="hand2")
            indicator.pack(side="left", padx=2)
            indicators.append(indicator)
            
            # Make clickable
            indicator.bind("<Button-1>", 
                          lambda e, idx=i, s=skill.name: 
                          self.set_skill_level(s, idx+1))
        
        return {
            'frame': frame,
            'level_display': level_display,
            'indicators': indicators,
            'remove_btn': remove_btn
        }
    
    def set_skill_level(self, skill_name, level):
        self.selected_skills[skill_name] = level
        
        if skill_name in self.skill_widgets:
            widget_info = self.skill_widgets[skill_name]
            widget_info['level_display'].config(text=f"Lv{level}")
            
            for i, indicator in enumerate(widget_info['indicators']):
                if i < level:
                    indicator.config(text="●", fg="#e74c3c")
                else:
                    indicator.config(text="○", fg="gray")
        
        self.update_selected_display()
    
    def remove_skill(self, skill_name):
        if skill_name in self.selected_skills:
            del self.selected_skills[skill_name]
        
        if skill_name in self.skill_widgets:
            self.skill_widgets[skill_name]['frame'].destroy()
            del self.skill_widgets[skill_name]
        
        self.update_selected_display()
    
    def update_selected_display(self):
        self.selected_display.config(state="normal")
        self.selected_display.delete("1.0", tk.END)
        
        if not self.selected_skills:
            self.selected_display.insert("1.0", "No skills selected")
            self.stats_label.config(text="Skills: 0\nTotal Levels: 0")
        else:
            regular_skills = []
            special_skills = []
            
            for skill_name, level in self.selected_skills.items():
                skill = self.data_manager.get_skill(skill_name)
                if skill:
                    if skill.skill_type in ["Group", "SetBonus"]:
                        special_skills.append((skill, level))
                    else:
                        regular_skills.append((skill, level))
            
            if regular_skills:
                self.selected_display.insert(tk.END, "🛡️ REGULAR SKILLS:\n", "section_title")
                self.selected_display.tag_config("section_title", font=("Consolas", 10, "bold"))
                
                for skill, level in sorted(regular_skills, key=lambda x: x[0].name):
                    self.selected_display.insert(tk.END, f"  • {skill.name}: Lv{level}\n")
                    effect = skill.get_effect(level)
                    if effect:
                        self.selected_display.insert(tk.END, f"    → {effect}\n")
                    if skill.description:
                        self.selected_display.insert(tk.END, f"    ({skill.description})\n")
                    self.selected_display.insert(tk.END, "\n")
            
            if special_skills:
                if regular_skills:
                    self.selected_display.insert(tk.END, "\n")
                
                self.selected_display.insert(tk.END, "👥 SPECIAL SKILLS:\n", "section_title")
                
                for skill, level in sorted(special_skills, key=lambda x: x[0].name):
                    icon = "👥 " if skill.skill_type == "Group" else "⭐ "
                    self.selected_display.insert(tk.END, f"  • {icon}{skill.name}: Lv{level}\n")
                    effect = skill.get_effect(level)
                    if effect:
                        self.selected_display.insert(tk.END, f"    → {effect}\n")
                    if skill.description:
                        self.selected_display.insert(tk.END, f"    ({skill.description})\n")
                    self.selected_display.insert(tk.END, "\n")
            
            total_skills = len(self.selected_skills)
            total_levels = sum(self.selected_skills.values())
            self.stats_label.config(
                text=f"Total Skills: {total_skills}\nTotal Levels: {total_levels}\n"
                     f"Regular: {len(regular_skills)}\nSpecial: {len(special_skills)}"
            )
        
        self.selected_display.config(state="disabled")
    
    def find_builds(self):
        if not self.selected_skills:
            messagebox.showwarning("No Skills", "Please select at least one skill")
            return
        
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        
        self.results_text.insert("1.0", "=== BUILD RESULTS ===\n\n")
        self.results_text.insert(tk.END, f"Searching for builds with {len(self.selected_skills)} skills:\n\n")
        
        regular_skills = []
        special_skills = []
        
        for skill_name, level in self.selected_skills.items():
            skill = self.data_manager.get_skill(skill_name)
            if skill:
                if skill.skill_type in ["Group", "SetBonus"]:
                    special_skills.append((skill, level))
                else:
                    regular_skills.append((skill, level))
        
        if regular_skills:
            self.results_text.insert(tk.END, "🛡️ REGULAR SKILLS:\n\n")
            for skill, level in regular_skills:
                armor_with_skill = self.data_manager.get_armor_by_skill(skill.name, level)
                decorations_with_skill = self.data_manager.get_decorations_by_skill(skill.name)
                
                self.results_text.insert(tk.END, f"• {skill.name}: Lv{level}\n")
                
                if armor_with_skill:
                    self.results_text.insert(tk.END, f"  Found in {len(armor_with_skill)} armor pieces\n")
                
                if decorations_with_skill:
                    self.results_text.insert(tk.END, f"  Available as {len(decorations_with_skill)} decorations\n")
                
                self.results_text.insert(tk.END, "\n")
        
        if special_skills:
            self.results_text.insert(tk.END, "👥 SPECIAL SKILLS:\n\n")
            for skill, level in special_skills:
                icon = "👥 " if skill.skill_type == "Group" else "⭐ "
                self.results_text.insert(tk.END, f"• {icon}{skill.name}: Lv{level}\n")
                
                matching_armor = []
                for armor in self.data_manager.armor:
                    if (skill.skill_type == "Group" and armor.group_skill == skill.name) or \
                       (skill.skill_type == "SetBonus" and armor.set_bonus_skill == skill.name):
                        matching_armor.append(armor)
                
                if matching_armor:
                    sets = set(a.set_name for a in matching_armor)
                    self.results_text.insert(tk.END, f"  Provided by {len(sets)} armor set(s)\n")
                    for set_name in sorted(sets)[:3]:
                        self.results_text.insert(tk.END, f"    - {set_name}\n")
                    if len(sets) > 3:
                        self.results_text.insert(tk.END, f"    ... and {len(sets) - 3} more\n")
                
                self.results_text.insert(tk.END, "\n")
        
        self.results_text.insert(tk.END, "\n[Build search algorithm to be implemented]")
        
        self.results_text.config(state="disabled")
    
    def clear_all(self):
        for skill_name, widget_info in list(self.skill_widgets.items()):
            widget_info['frame'].destroy()
        self.skill_widgets.clear()
        
        self.selected_skills.clear()
        self.update_selected_display()
        
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", "Builds will appear here...")
        self.results_text.config(state="disabled")

# Run the app
if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    
    app = MHWBuilderApp()