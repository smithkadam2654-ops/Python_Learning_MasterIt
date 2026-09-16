"""
GUI Utilities Module

This module provides comprehensive graphical user interface utilities including:
- Simple GUI components with Tkinter
- Dialog boxes and input forms
- File dialogs and browsers
- Progress dialogs
- Message boxes
- Menu systems
- Canvas drawing
- Event handling
- Widget styling
- Form validation

Note: This module uses Tkinter for GUI operations.
Tkinter is included with standard Python installation.

All functions include comprehensive docstrings and type hints.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from datetime import datetime
import threading


@dataclass
class DialogResult:
    """Container for dialog results."""
    accepted: bool
    data: Any
    cancelled: bool


class SimpleWindow:
    """Simple window manager."""
    
    def __init__(self, title: str = "Window", size: Tuple[int, int] = (400, 300)):
        """Initialize simple window."""
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.root.resizable(True, True)
        
        self.widgets = {}
        self.layouts = {}
    
    def add_label(self, text: str, row: int = 0, column: int = 0, 
                  padx: int = 5, pady: int = 5) -> tk.Label:
        """Add label to window."""
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky="w")
        self.widgets[f"label_{row}_{column}"] = label
        return label
    
    def add_button(self, text: str, command: Callable, 
                  row: int = 0, column: int = 0,
                  padx: int = 5, pady: int = 5) -> tk.Button:
        """Add button to window."""
        button = tk.Button(self.root, text=text, command=command)
        button.grid(row=row, column=column, padx=padx, pady=pady)
        self.widgets[f"button_{row}_{column}"] = button
        return button
    
    def add_entry(self, row: int = 0, column: int = 0,
                 padx: int = 5, pady: int = 5, width: int = 20) -> tk.Entry:
        """Add entry field to window."""
        entry = tk.Entry(self.root, width=width)
        entry.grid(row=row, column=column, padx=padx, pady=pady)
        self.widgets[f"entry_{row}_{column}"] = entry
        return entry
    
    def add_text(self, row: int = 0, column: int = 0,
                padx: int = 5, pady: int = 5, 
                width: int = 40, height: int = 10) -> tk.Text:
        """Add text area to window."""
        text = tk.Text(self.root, width=width, height=height)
        text.grid(row=row, column=column, padx=padx, pady=pady)
        self.widgets[f"text_{row}_{column}"] = text
        return text
    
    def add_combobox(self, values: List[str], row: int = 0, column: int = 0,
                    padx: int = 5, pady: int = 5, width: int = 20) -> ttk.Combobox:
        """Add combobox to window."""
        combobox = ttk.Combobox(self.root, values=values, width=width)
        combobox.grid(row=row, column=column, padx=padx, pady=pady)
        self.widgets[f"combobox_{row}_{column}"] = combobox
        return combobox
    
    def add_checkbox(self, text: str, row: int = 0, column: int = 0,
                    padx: int = 5, pady: int = 5) -> tk.Checkbutton:
        """Add checkbox to window."""
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.root, text=text, variable=var)
        checkbox.grid(row=row, column=column, padx=padx, pady=pady, sticky="w")
        self.widgets[f"checkbox_{row}_{column}"] = checkbox
        return checkbox
    
    def add_radiobutton(self, text: str, variable: tk.Variable, 
                      value: Any, row: int = 0, column: int = 0,
                      padx: int = 5, pady: int = 5) -> tk.Radiobutton:
        """Add radio button to window."""
        radiobutton = tk.Radiobutton(self.root, text=text, variable=variable, value=value)
        radiobutton.grid(row=row, column=column, padx=padx, pady=pady, sticky="w")
        return radiobutton
    
    def add_progressbar(self, row: int = 0, column: int = 0,
                       padx: int = 5, pady: int = 5, length: int = 200) -> ttk.Progressbar:
        """Add progress bar to window."""
        progress = ttk.Progressbar(self.root, length=length, mode='determinate')
        progress.grid(row=row, column=column, padx=padx, pady=pady)
        self.widgets[f"progress_{row}_{column}"] = progress
        return progress
    
    def add_listbox(self, row: int = 0, column: int = 0,
                   padx: int = 5, pady: int = 5, 
                   width: int = 30, height: int = 10) -> tk.Listbox:
        """Add listbox to window."""
        listbox = tk.Listbox(self.root, width=width, height=height)
        listbox.grid(row=row, column=column, padx=padx, pady=pady)
        self.widgets[f"listbox_{row}_{column}"] = listbox
        return listbox
    
    def add_scrollbar(self, widget: tk.Widget, row: int = 0, column: int = 0,
                    padx: int = 5, pady: int = 5) -> tk.Scrollbar:
        """Add scrollbar to widget."""
        scrollbar = tk.Scrollbar(self.root, command=widget.yview)
        scrollbar.grid(row=row, column=column, padx=padx, pady=pady)
        widget.config(yscrollcommand=scrollbar.set)
        return scrollbar
    
    def add_canvas(self, row: int = 0, column: int = 0,
                  padx: int = 5, pady: int = 5,
                  width: int = 400, height: int = 300) -> tk.Canvas:
        """Add canvas to window."""
        canvas = tk.Canvas(self.root, width=width, height=height)
        canvas.grid(row=row, column=column, padx=padx, pady=pady)
        self.widgets[f"canvas_{row}_{column}"] = canvas
        return canvas
    
    def add_separator(self, row: int = 0, column: int = 0,
                     padx: int = 5, pady: int = 5, orient: str = "horizontal") -> ttk.Separator:
        """Add separator to window."""
        separator = ttk.Separator(self.root, orient=orient)
        separator.grid(row=row, column=column, padx=padx, pady=pady, sticky="ew")
        return separator
    
    def get_widget(self, name: str) -> Optional[tk.Widget]:
        """Get widget by name."""
        return self.widgets.get(name)
    
    def clear_widgets(self) -> None:
        """Clear all widgets from window."""
        for widget in self.widgets.values():
            widget.destroy()
        self.widgets.clear()
    
    def center_window(self) -> None:
        """Center window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def run(self) -> None:
        """Start the main event loop."""
        self.root.mainloop()
    
    def close(self) -> None:
        """Close the window."""
        self.root.destroy()


class DialogBox:
    """Dialog box utilities."""
    
    @staticmethod
    def show_info(title: str, message: str) -> None:
        """Show info dialog."""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_warning(title: str, message: str) -> None:
        """Show warning dialog."""
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_error(title: str, message: str) -> None:
        """Show error dialog."""
        messagebox.showerror(title, message)
    
    @staticmethod
    def ask_yes_no(title: str, message: str) -> bool:
        """Ask yes/no question."""
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def ask_ok_cancel(title: str, message: str) -> bool:
        """Ask ok/cancel question."""
        return messagebox.askokcancel(title, message)
    
    @staticmethod
    def ask_retry_cancel(title: str, message: str) -> bool:
        """Ask retry/cancel question."""
        return messagebox.askretrycancel(title, message)
    
    @staticmethod
    def ask_question(title: str, message: str) -> bool:
        """Ask yes/no question (returns True for yes)."""
        return messagebox.askquestion(title, message) == "yes"
    
    @staticmethod
    def get_string(title: str, prompt: str, default: str = "") -> Optional[str]:
        """Get string input from user."""
        return simpledialog.askstring(title, prompt, initialvalue=default)
    
    @staticmethod
    def get_integer(title: str, prompt: str, 
                   min_value: Optional[int] = None,
                   max_value: Optional[int] = None,
                   default: Optional[int] = None) -> Optional[int]:
        """Get integer input from user."""
        return simpledialog.askinteger(title, prompt, 
                                     minvalue=min_value, 
                                     maxvalue=max_value,
                                     initialvalue=default)
    
    @staticmethod
    def get_float(title: str, prompt: str,
                 min_value: Optional[float] = None,
                 max_value: Optional[float] = None,
                 default: Optional[float] = None) -> Optional[float]:
        """Get float input from user."""
        return simpledialog.askfloat(title, prompt,
                                    minvalue=min_value,
                                    maxvalue=max_value,
                                    initialvalue=default)
    
    @staticmethod
    def get_password(title: str, prompt: str) -> Optional[str]:
        """Get password input from user."""
        return simpledialog.askstring(title, prompt, show='*')


class FileDialog:
    """File dialog utilities."""
    
    @staticmethod
    def open_file(title: str = "Open File",
                 filetypes: Optional[List[Tuple[str, str]]] = None,
                 initialdir: Optional[str] = None) -> Optional[str]:
        """Open file dialog."""
        if filetypes is None:
            filetypes = [("All Files", "*.*")]
        
        return filedialog.askopenfilename(
            title=title,
            filetypes=filetypes,
            initialdir=initialdir
        )
    
    @staticmethod
    def save_file(title: str = "Save File",
                 filetypes: Optional[List[Tuple[str, str]]] = None,
                 initialdir: Optional[str] = None,
                 defaultextension: str = "") -> Optional[str]:
        """Save file dialog."""
        if filetypes is None:
            filetypes = [("All Files", "*.*")]
        
        return filedialog.asksaveasfilename(
            title=title,
            filetypes=filetypes,
            initialdir=initialdir,
            defaultextension=defaultextension
        )
    
    @staticmethod
    def select_directory(title: str = "Select Directory",
                       initialdir: Optional[str] = None) -> Optional[str]:
        """Select directory dialog."""
        return filedialog.askdirectory(title=title, initialdir=initialdir)
    
    @staticmethod
    def open_files(title: str = "Open Files",
                  filetypes: Optional[List[Tuple[str, str]]] = None,
                  initialdir: Optional[str] = None) -> Optional[List[str]]:
        """Open multiple files dialog."""
        if filetypes is None:
            filetypes = [("All Files", "*.*")]
        
        return filedialog.askopenfilenames(
            title=title,
            filetypes=filetypes,
            initialdir=initialdir
        )


class FormBuilder:
    """Form builder for data entry."""
    
    def __init__(self, parent: tk.Tk):
        """Initialize form builder."""
        self.parent = parent
        self.fields: Dict[str, Dict[str, Any]] = {}
        self.entries: Dict[str, tk.Widget] = {}
        self.row = 0
    
    def add_text_field(self, label: str, field_name: str,
                      default: str = "", required: bool = False) -> None:
        """Add text field to form."""
        tk.Label(self.parent, text=label).grid(row=self.row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(self.parent)
        entry.insert(0, default)
        entry.grid(row=self.row, column=1, sticky="ew", padx=5, pady=5)
        
        self.fields[field_name] = {
            "type": "text",
            "label": label,
            "required": required,
            "default": default
        }
        self.entries[field_name] = entry
        self.row += 1
    
    def add_number_field(self, label: str, field_name: str,
                        default: Union[int, float] = 0,
                        required: bool = False,
                        min_value: Optional[Union[int, float]] = None,
                        max_value: Optional[Union[int, float]] = None) -> None:
        """Add number field to form."""
        tk.Label(self.parent, text=label).grid(row=self.row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(self.parent)
        entry.insert(0, str(default))
        entry.grid(row=self.row, column=1, sticky="ew", padx=5, pady=5)
        
        self.fields[field_name] = {
            "type": "number",
            "label": label,
            "required": required,
            "default": default,
            "min_value": min_value,
            "max_value": max_value
        }
        self.entries[field_name] = entry
        self.row += 1
    
    def add_dropdown_field(self, label: str, field_name: str,
                          options: List[str], default: str = "",
                          required: bool = False) -> None:
        """Add dropdown field to form."""
        tk.Label(self.parent, text=label).grid(row=self.row, column=0, sticky="w", padx=5, pady=5)
        combobox = ttk.Combobox(self.parent, values=options)
        combobox.set(default)
        combobox.grid(row=self.row, column=1, sticky="ew", padx=5, pady=5)
        
        self.fields[field_name] = {
            "type": "dropdown",
            "label": label,
            "required": required,
            "default": default,
            "options": options
        }
        self.entries[field_name] = combobox
        self.row += 1
    
    def add_checkbox_field(self, label: str, field_name: str,
                          default: bool = False) -> None:
        """Add checkbox field to form."""
        var = tk.BooleanVar(value=default)
        checkbox = tk.Checkbutton(self.parent, text=label, variable=var)
        checkbox.grid(row=self.row, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        self.fields[field_name] = {
            "type": "checkbox",
            "label": label,
            "default": default
        }
        self.entries[field_name] = var
        self.row += 1
    
    def add_textarea_field(self, label: str, field_name: str,
                          default: str = "", required: bool = False,
                          height: int = 5) -> None:
        """Add textarea field to form."""
        tk.Label(self.parent, text=label).grid(row=self.row, column=0, sticky="nw", padx=5, pady=5)
        text = tk.Text(self.parent, height=height)
        text.insert("1.0", default)
        text.grid(row=self.row, column=1, sticky="ew", padx=5, pady=5)
        
        self.fields[field_name] = {
            "type": "textarea",
            "label": label,
            "required": required,
            "default": default
        }
        self.entries[field_name] = text
        self.row += 1
    
    def get_data(self) -> Dict[str, Any]:
        """Get form data as dictionary."""
        data = {}
        
        for field_name, field_info in self.fields.items():
            widget = self.entries[field_name]
            
            if field_info["type"] == "text":
                data[field_name] = widget.get()
            elif field_info["type"] == "number":
                value = widget.get()
                try:
                    if "." in value:
                        data[field_name] = float(value)
                    else:
                        data[field_name] = int(value)
                except ValueError:
                    data[field_name] = field_info["default"]
            elif field_info["type"] == "dropdown":
                data[field_name] = widget.get()
            elif field_info["type"] == "checkbox":
                data[field_name] = widget.get()
            elif field_info["type"] == "textarea":
                data[field_name] = widget.get("1.0", tk.END).strip()
        
        return data
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate form data."""
        errors = []
        
        for field_name, field_info in self.fields.items():
            widget = self.entries[field_name]
            
            if field_info.get("required"):
                if field_info["type"] == "checkbox":
                    if not widget.get():
                        errors.append(f"{field_info['label']} is required")
                else:
                    value = widget.get() if hasattr(widget, 'get') else ""
                    if not value or value.strip() == "":
                        errors.append(f"{field_info['label']} is required")
            
            if field_info["type"] == "number":
                value = widget.get()
                try:
                    num = float(value)
                    if field_info.get("min_value") is not None and num < field_info["min_value"]:
                        errors.append(f"{field_info['label']} must be at least {field_info['min_value']}")
                    if field_info.get("max_value") is not None and num > field_info["max_value"]:
                        errors.append(f"{field_info['label']} must be at most {field_info['max_value']}")
                except ValueError:
                    errors.append(f"{field_info['label']} must be a number")
        
        return len(errors) == 0, errors
    
    def clear(self) -> None:
        """Clear all form fields."""
        for field_name, field_info in self.fields.items():
            widget = self.entries[field_name]
            
            if field_info["type"] in ["text", "number", "dropdown"]:
                widget.delete(0, tk.END)
                widget.insert(0, str(field_info["default"]))
            elif field_info["type"] == "checkbox":
                widget.set(field_info["default"])
            elif field_info["type"] == "textarea":
                widget.delete("1.0", tk.END)
                widget.insert("1.0", field_info["default"])


class ProgressBarDialog:
    """Progress bar dialog for long operations."""
    
    def __init__(self, title: str = "Progress", 
                 message: str = "Processing...",
                 maximum: int = 100):
        """Initialize progress dialog."""
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("400x150")
        self.root.resizable(False, False)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Message label
        self.message_label = tk.Label(self.root, text=message)
        self.message_label.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=350, mode='determinate', maximum=maximum)
        self.progress.pack(pady=10)
        
        # Percentage label
        self.percentage_label = tk.Label(self.root, text="0%")
        self.percentage_label.pack(pady=5)
        
        self.maximum = maximum
        self.current = 0
    
    def update(self, value: int, message: Optional[str] = None) -> None:
        """Update progress bar."""
        self.current = value
        self.progress['value'] = value
        percentage = int((value / self.maximum) * 100) if self.maximum > 0 else 0
        self.percentage_label.config(text=f"{percentage}%")
        
        if message:
            self.message_label.config(text=message)
        
        self.root.update()
    
    def increment(self, amount: int = 1, message: Optional[str] = None) -> None:
        """Increment progress bar."""
        self.update(self.current + amount, message)
    
    def close(self) -> None:
        """Close progress dialog."""
        self.root.destroy()
    
    def run(self) -> None:
        """Run progress dialog (blocks until closed)."""
        self.root.mainloop()


class MenuBuilder:
    """Menu builder for windows."""
    
    def __init__(self, parent: tk.Tk):
        """Initialize menu builder."""
        self.parent = parent
        self.menubar = tk.Menu(parent)
        self.menus: Dict[str, tk.Menu] = {}
    
    def add_menu(self, label: str) -> tk.Menu:
        """Add menu to menubar."""
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=label, menu=menu)
        self.menus[label] = menu
        return menu
    
    def add_menu_item(self, menu_label: str, item_label: str,
                     command: Callable, accelerator: Optional[str] = None) -> None:
        """Add item to menu."""
        if menu_label in self.menus:
            self.menus[menu_label].add_command(
                label=item_label,
                command=command,
                accelerator=accelerator
            )
    
    def add_separator(self, menu_label: str) -> None:
        """Add separator to menu."""
        if menu_label in self.menus:
            self.menus[menu_label].add_separator()
    
    def add_submenu(self, menu_label: str, submenu_label: str) -> tk.Menu:
        """Add submenu to menu."""
        if menu_label in self.menus:
            submenu = tk.Menu(self.menus[menu_label], tearoff=0)
            self.menus[menu_label].add_cascade(label=submenu_label, menu=submenu)
            return submenu
        return None
    
    def build(self) -> None:
        """Build and apply menubar to parent."""
        self.parent.config(menu=self.menubar)


class CanvasDrawer:
    """Canvas drawing utilities."""
    
    def __init__(self, canvas: tk.Canvas):
        """Initialize canvas drawer."""
        self.canvas = canvas
    
    def draw_line(self, x1: int, y1: int, x2: int, y2: int,
                 color: str = "black", width: int = 1) -> int:
        """Draw line on canvas."""
        return self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
    
    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int,
                      fill: str = "", outline: str = "black", width: int = 1) -> int:
        """Draw rectangle on canvas."""
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=width)
    
    def draw_oval(self, x1: int, y1: int, x2: int, y2: int,
                 fill: str = "", outline: str = "black", width: int = 1) -> int:
        """Draw oval on canvas."""
        return self.canvas.create_oval(x1, y1, x2, y2, fill=fill, outline=outline, width=width)
    
    def draw_circle(self, x: int, y: int, radius: int,
                   fill: str = "", outline: str = "black", width: int = 1) -> int:
        """Draw circle on canvas."""
        return self.draw_oval(x - radius, y - radius, x + radius, y + radius, 
                            fill, outline, width)
    
    def draw_text(self, x: int, y: int, text: str,
                 font: Optional[str] = None, size: int = 12,
                 color: str = "black") -> int:
        """Draw text on canvas."""
        font_spec = f"{font} {size}" if font else f"Arial {size}"
        return self.canvas.create_text(x, y, text=text, font=font_spec, fill=color)
    
    def draw_polygon(self, points: List[Tuple[int, int]],
                   fill: str = "", outline: str = "black", width: int = 1) -> int:
        """Draw polygon on canvas."""
        flat_points = [coord for point in points for coord in point]
        return self.canvas.create_polygon(flat_points, fill=fill, outline=outline, width=width)
    
    def clear(self) -> None:
        """Clear canvas."""
        self.canvas.delete("all")


def demonstrate_gui_utils():
    """Demonstrate GUI utilities functionality."""
    print("=== GUI Utilities Demonstration ===\n")
    
    print("Note: GUI utilities require a graphical environment.")
    print("The following components are available:")
    
    print("\n1. SimpleWindow:")
    print("   - Create windows with various widgets")
    print("   - Add labels, buttons, entries, text areas")
    print("   - Add comboboxes, checkboxes, radio buttons")
    print("   - Add progress bars, listboxes, canvas")
    print("   - Center windows and manage layout")
    
    print("\n2. DialogBox:")
    print("   - Show info, warning, error dialogs")
    print("   - Ask yes/no, ok/cancel questions")
    print("   - Get string, integer, float input")
    print("   - Get password input securely")
    
    print("\n3. FileDialog:")
    print("   - Open file dialog")
    print("   - Save file dialog")
    print("   - Select directory dialog")
    print("   - Open multiple files dialog")
    
    print("\n4. FormBuilder:")
    print("   - Build data entry forms")
    print("   - Add text, number, dropdown fields")
    print("   - Add checkboxes and textareas")
    print("   - Validate form data")
    print("   - Get form data as dictionary")
    
    print("\n5. ProgressBarDialog:")
    print("   - Show progress for long operations")
    print("   - Update progress and messages")
    print("   - Display percentage completion")
    
    print("\n6. MenuBuilder:")
    print("   - Create menu bars")
    print("   - Add menus and menu items")
    print("   - Add submenus and separators")
    print("   - Set keyboard accelerators")
    
    print("\n7. CanvasDrawer:")
    print("   - Draw lines, rectangles, ovals")
    print("   - Draw circles and polygons")
    print("   - Draw text with custom fonts")
    print("   - Clear canvas")
    
    print("\n=== Example Usage ===")
    print("""
# Simple Window Example:
window = SimpleWindow("My App", (500, 400))
window.add_label("Enter your name:", 0, 0)
entry = window.add_entry(0, 1)
window.add_button("Submit", lambda: print(entry.get()), 1, 0)
window.center_window()
window.run()

# Dialog Example:
DialogBox.show_info("Info", "Operation completed successfully")
if DialogBox.ask_yes_no("Confirm", "Are you sure?"):
    print("User confirmed")

# File Dialog Example:
file_path = FileDialog.open_file("Open File", [("Text Files", "*.txt")])
if file_path:
    print(f"Selected: {file_path}")

# Form Example:
form = FormBuilder(window)
form.add_text_field("Name:", "name", required=True)
form.add_number_field("Age:", "age", required=True, min_value=0)
form.add_dropdown_field("Country:", "country", ["USA", "UK", "Canada"])
data = form.get_data()
is_valid, errors = form.validate()
""")
    
    print("\n=== Demonstration Complete ===")
    print("GUI components require graphical environment to run interactively.")


if __name__ == "__main__":
    demonstrate_gui_utils()