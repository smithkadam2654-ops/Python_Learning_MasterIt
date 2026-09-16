"""
Excel Processing Module

This module provides comprehensive Excel file operations and utilities including:
- Excel file reading and writing
- Workbook and worksheet management
- Cell formatting and styling
- Data validation and formulas
- Chart creation
- Data import/export
- Batch operations
- Template processing
- Data analysis helpers
- Pivot table creation

Note: This module uses openpyxl library for Excel operations.
Install with: pip install openpyxl

All functions include comprehensive docstrings and type hints.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import os


try:
    import openpyxl
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.chart import BarChart, LineChart, PieChart, Reference
    from openpyxl.utils import get_column_letter
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False


@dataclass
class CellRange:
    """Represents a cell range in Excel."""
    min_row: int
    max_row: int
    min_col: int
    max_col: int
    
    @property
    def address(self) -> str:
        """Get the range address (e.g., 'A1:C10')."""
        return f"{get_column_letter(self.min_col)}{self.min_row}:{get_column_letter(self.max_col)}{self.max_row}"


@dataclass
class ExcelStyle:
    """Represents Excel cell styling."""
    font_name: str = "Arial"
    font_size: int = 11
    font_bold: bool = False
    font_italic: bool = False
    font_color: str = "000000"
    fill_color: Optional[str] = None
    horizontal_alignment: str = "left"
    vertical_alignment: str = "bottom"
    border: bool = False


class ExcelManager:
    """Main Excel file manager class."""
    
    def __init__(self, file_path: Optional[str] = None):
        """Initialize Excel manager with optional file path."""
        self.file_path = file_path
        self.workbook: Optional[Workbook] = None
        self.current_worksheet = None
        
        if not EXCEL_AVAILABLE:
            raise ImportError("openpyxl library is required. Install with: pip install openpyxl")
    
    def create_workbook(self) -> Workbook:
        """Create a new workbook."""
        self.workbook = Workbook()
        self.current_worksheet = self.workbook.active
        return self.workbook
    
    def load_workbook(self, file_path: str) -> Workbook:
        """Load an existing workbook."""
        self.file_path = file_path
        self.workbook = load_workbook(file_path)
        self.current_worksheet = self.workbook.active
        return self.workbook
    
    def save_workbook(self, file_path: Optional[str] = None) -> None:
        """Save the workbook to file."""
        save_path = file_path or self.file_path
        if not save_path:
            raise ValueError("No file path specified")
        self.workbook.save(save_path)
    
    def close(self) -> None:
        """Close the workbook."""
        if self.workbook:
            self.workbook.close()
            self.workbook = None
            self.current_worksheet = None
    
    def create_worksheet(self, name: str) -> None:
        """Create a new worksheet."""
        if not self.workbook:
            self.create_workbook()
        self.workbook.create_sheet(name)
    
    def get_worksheet(self, name: str) -> Any:
        """Get a worksheet by name."""
        if not self.workbook:
            raise ValueError("No workbook loaded")
        return self.workbook[name]
    
    def set_active_worksheet(self, name: str) -> None:
        """Set the active worksheet."""
        self.current_worksheet = self.get_worksheet(name)
    
    def delete_worksheet(self, name: str) -> None:
        """Delete a worksheet."""
        if not self.workbook:
            raise ValueError("No workbook loaded")
        self.workbook.remove(self.workbook[name])
    
    def list_worksheets(self) -> List[str]:
        """List all worksheet names."""
        if not self.workbook:
            return []
        return self.workbook.sheetnames


class CellOperations:
    """Cell-level operations."""
    
    def __init__(self, excel_manager: ExcelManager):
        """Initialize cell operations with Excel manager."""
        self.manager = excel_manager
    
    def write_cell(self, row: int, col: int, value: Any, 
                   worksheet: Optional[Any] = None) -> None:
        """Write a value to a specific cell."""
        ws = worksheet or self.manager.current_worksheet
        ws.cell(row=row, column=col, value=value)
    
    def read_cell(self, row: int, col: int, 
                  worksheet: Optional[Any] = None) -> Any:
        """Read a value from a specific cell."""
        ws = worksheet or self.manager.current_worksheet
        return ws.cell(row=row, column=col).value
    
    def write_range(self, start_row: int, start_col: int, data: List[List[Any]],
                    worksheet: Optional[Any] = None) -> None:
        """Write data to a range of cells."""
        ws = worksheet or self.manager.current_worksheet
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                ws.cell(row=start_row + row_idx, column=start_col + col_idx, value=value)
    
    def read_range(self, start_row: int, start_col: int, end_row: int, end_col: int,
                   worksheet: Optional[Any] = None) -> List[List[Any]]:
        """Read data from a range of cells."""
        ws = worksheet or self.manager.current_worksheet
        data = []
        for row in range(start_row, end_row + 1):
            row_data = []
            for col in range(start_col, end_col + 1):
                row_data.append(ws.cell(row=row, column=col).value)
            data.append(row_data)
        return data
    
    def clear_cell(self, row: int, col: int, 
                   worksheet: Optional[Any] = None) -> None:
        """Clear a cell's value."""
        ws = worksheet or self.manager.current_worksheet
        ws.cell(row=row, column=col).value = None
    
    def clear_range(self, start_row: int, start_col: int, end_row: int, end_col: int,
                    worksheet: Optional[Any] = None) -> None:
        """Clear a range of cells."""
        ws = worksheet or self.manager.current_worksheet
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                ws.cell(row=row, column=col).value = None
    
    def insert_row(self, row: int, worksheet: Optional[Any] = None) -> None:
        """Insert a new row."""
        ws = worksheet or self.manager.current_worksheet
        ws.insert_rows(row)
    
    def delete_row(self, row: int, worksheet: Optional[Any] = None) -> None:
        """Delete a row."""
        ws = worksheet or self.manager.current_worksheet
        ws.delete_rows(row)
    
    def insert_column(self, col: int, worksheet: Optional[Any] = None) -> None:
        """Insert a new column."""
        ws = worksheet or self.manager.current_worksheet
        ws.insert_cols(col)
    
    def delete_column(self, col: int, worksheet: Optional[Any] = None) -> None:
        """Delete a column."""
        ws = worksheet or self.manager.current_worksheet
        ws.delete_cols(col)


class StylingOperations:
    """Cell styling and formatting operations."""
    
    def __init__(self, excel_manager: ExcelManager):
        """Initialize styling operations with Excel manager."""
        self.manager = excel_manager
    
    def apply_style(self, row: int, col: int, style: ExcelStyle,
                    worksheet: Optional[Any] = None) -> None:
        """Apply style to a cell."""
        ws = worksheet or self.manager.current_worksheet
        cell = ws.cell(row=row, column=col)
        
        # Font styling
        cell.font = Font(
            name=style.font_name,
            size=style.font_size,
            bold=style.font_bold,
            italic=style.font_italic,
            color=style.font_color
        )
        
        # Fill styling
        if style.fill_color:
            cell.fill = PatternFill(start_color=style.fill_color, end_color=style.fill_color, fill_type="solid")
        
        # Alignment
        cell.alignment = Alignment(
            horizontal=style.horizontal_alignment,
            vertical=style.vertical_alignment
        )
        
        # Border
        if style.border:
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            cell.border = thin_border
    
    def apply_style_to_range(self, start_row: int, start_col: int, end_row: int, end_col: int,
                             style: ExcelStyle, worksheet: Optional[Any] = None) -> None:
        """Apply style to a range of cells."""
        ws = worksheet or self.manager.current_worksheet
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                self.apply_style(row, col, style, ws)
    
    def create_header_style(self) -> ExcelStyle:
        """Create a standard header style."""
        return ExcelStyle(
            font_name="Arial",
            font_size=12,
            font_bold=True,
            font_color="FFFFFF",
            fill_color="4472C4",
            horizontal_alignment="center",
            border=True
        )
    
    def create_number_style(self) -> ExcelStyle:
        """Create a standard number style."""
        return ExcelStyle(
            font_name="Arial",
            font_size=11,
            horizontal_alignment="right"
        )
    
    def create_title_style(self) -> ExcelStyle:
        """Create a title style."""
        return ExcelStyle(
            font_name="Arial",
            font_size=16,
            font_bold=True,
            font_color="000000",
            horizontal_alignment="center"
        )
    
    def auto_fit_column(self, col: int, worksheet: Optional[Any] = None) -> None:
        """Auto-fit column width based on content."""
        ws = worksheet or self.manager.current_worksheet
        column_letter = get_column_letter(col)
        max_length = 0
        
        for row in range(1, ws.max_row + 1):
            cell_value = ws.cell(row=row, column=col).value
            if cell_value:
                cell_length = len(str(cell_value))
                if cell_length > max_length:
                    max_length = cell_length
        
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column_letter].width = adjusted_width
    
    def auto_fit_all_columns(self, worksheet: Optional[Any] = None) -> None:
        """Auto-fit all columns in the worksheet."""
        ws = worksheet or self.manager.current_worksheet
        for col in range(1, ws.max_column + 1):
            self.auto_fit_column(col, ws)


class FormulaOperations:
    """Excel formula operations."""
    
    def __init__(self, excel_manager: ExcelManager):
        """Initialize formula operations with Excel manager."""
        self.manager = excel_manager
    
    def write_formula(self, row: int, col: int, formula: str,
                      worksheet: Optional[Any] = None) -> None:
        """Write a formula to a cell."""
        ws = worksheet or self.manager.current_worksheet
        ws.cell(row=row, column=col, value=formula)
    
    def sum_range(self, start_row: int, start_col: int, end_row: int, end_col: int,
                  output_row: int, output_col: int, worksheet: Optional[Any] = None) -> None:
        """Write SUM formula for a range."""
        ws = worksheet or self.manager.current_worksheet
        start_cell = f"{get_column_letter(start_col)}{start_row}"
        end_cell = f"{get_column_letter(end_col)}{end_row}"
        formula = f"=SUM({start_cell}:{end_cell})"
        ws.cell(row=output_row, column=output_col, value=formula)
    
    def average_range(self, start_row: int, start_col: int, end_row: int, end_col: int,
                      output_row: int, output_col: int, worksheet: Optional[Any] = None) -> None:
        """Write AVERAGE formula for a range."""
        ws = worksheet or self.manager.current_worksheet
        start_cell = f"{get_column_letter(start_col)}{start_row}"
        end_cell = f"{get_column_letter(end_col)}{end_row}"
        formula = f"=AVERAGE({start_cell}:{end_cell})"
        ws.cell(row=output_row, column=output_col, value=formula)
    
    def count_range(self, start_row: int, start_col: int, end_row: int, end_col: int,
                    output_row: int, output_col: int, worksheet: Optional[Any] = None) -> None:
        """Write COUNT formula for a range."""
        ws = worksheet or self.manager.current_worksheet
        start_cell = f"{get_column_letter(start_col)}{start_row}"
        end_cell = f"{get_column_letter(end_col)}{end_row}"
        formula = f"=COUNT({start_cell}:{end_cell})"
        ws.cell(row=output_row, column=output_col, value=formula)
    
    def max_range(self, start_row: int, start_col: int, end_row: int, end_col: int,
                  output_row: int, output_col: int, worksheet: Optional[Any] = None) -> None:
        """Write MAX formula for a range."""
        ws = worksheet or self.manager.current_worksheet
        start_cell = f"{get_column_letter(start_col)}{start_row}"
        end_cell = f"{get_column_letter(end_col)}{end_row}"
        formula = f"=MAX({start_cell}:{end_cell})"
        ws.cell(row=output_row, column=output_col, value=formula)
    
    def min_range(self, start_row: int, start_col: int, end_row: int, end_col: int,
                  output_row: int, output_col: int, worksheet: Optional[Any] = None) -> None:
        """Write MIN formula for a range."""
        ws = worksheet or self.manager.current_worksheet
        start_cell = f"{get_column_letter(start_col)}{start_row}"
        end_cell = f"{get_column_letter(end_col)}{end_row}"
        formula = f"=MIN({start_cell}:{end_cell})"
        ws.cell(row=output_row, column=output_col, value=formula)
    
    def vlookup(self, lookup_value: str, table_range: str, col_index: int, 
                output_row: int, output_col: int, worksheet: Optional[Any] = None) -> None:
        """Write VLOOKUP formula."""
        ws = worksheet or self.manager.current_worksheet
        formula = f"=VLOOKUP(\"{lookup_value}\",{table_range},{col_index},FALSE)"
        ws.cell(row=output_row, column=output_col, value=formula)


class ChartOperations:
    """Chart creation and management."""
    
    def __init__(self, excel_manager: ExcelManager):
        """Initialize chart operations with Excel manager."""
        self.manager = excel_manager
    
    def create_bar_chart(self, data_range: CellRange, title: str, 
                         worksheet: Optional[Any] = None) -> BarChart:
        """Create a bar chart."""
        ws = worksheet or self.manager.current_worksheet
        chart = BarChart()
        chart.type = "col"
        chart.style = 10
        chart.title = title
        
        data = Reference(ws, min_col=data_range.min_col, min_row=data_range.min_row,
                        max_col=data_range.max_col, max_row=data_range.max_row)
        chart.add_data(data, titles_from_data=True)
        
        ws.add_chart(chart, f"{ws.max_row + 2}")
        return chart
    
    def create_line_chart(self, data_range: CellRange, title: str,
                          worksheet: Optional[Any] = None) -> LineChart:
        """Create a line chart."""
        ws = worksheet or self.manager.current_worksheet
        chart = LineChart()
        chart.style = 10
        chart.title = title
        
        data = Reference(ws, min_col=data_range.min_col, min_row=data_range.min_row,
                        max_col=data_range.max_col, max_row=data_range.max_row)
        chart.add_data(data, titles_from_data=True)
        
        ws.add_chart(chart, f"{ws.max_row + 2}")
        return chart
    
    def create_pie_chart(self, data_range: CellRange, title: str,
                         worksheet: Optional[Any] = None) -> PieChart:
        """Create a pie chart."""
        ws = worksheet or self.manager.current_worksheet
        chart = PieChart()
        chart.style = 10
        chart.title = title
        
        data = Reference(ws, min_col=data_range.min_col, min_row=data_range.min_row,
                        max_col=data_range.max_col, max_row=data_range.max_row)
        chart.add_data(data)
        
        ws.add_chart(chart, f"{ws.max_row + 2}")
        return chart


class DataImportExport:
    """Data import and export operations."""
    
    def __init__(self, excel_manager: ExcelManager):
        """Initialize data import/export with Excel manager."""
        self.manager = excel_manager
    
    def import_from_list(self, data: List[List[Any]], start_row: int = 1, 
                         start_col: int = 1, worksheet: Optional[Any] = None) -> None:
        """Import data from list of lists."""
        ws = worksheet or self.manager.current_worksheet
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                ws.cell(row=start_row + row_idx, column=start_col + col_idx, value=value)
    
    def import_from_dict(self, data: List[Dict], start_row: int = 1,
                         start_col: int = 1, worksheet: Optional[Any] = None) -> None:
        """Import data from list of dictionaries."""
        ws = worksheet or self.manager.current_worksheet
        
        if not data:
            return
        
        # Write headers
        headers = list(data[0].keys())
        for col_idx, header in enumerate(headers):
            ws.cell(row=start_row, column=start_col + col_idx, value=header)
        
        # Write data
        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(headers):
                ws.cell(row=start_row + row_idx + 1, column=start_col + col_idx, 
                       value=row_data.get(header))
    
    def export_to_list(self, start_row: int = 1, start_col: int = 1,
                       end_row: Optional[int] = None, end_col: Optional[int] = None,
                       worksheet: Optional[Any] = None) -> List[List[Any]]:
        """Export data to list of lists."""
        ws = worksheet or self.manager.current_worksheet
        
        if end_row is None:
            end_row = ws.max_row
        if end_col is None:
            end_col = ws.max_column
        
        data = []
        for row in range(start_row, end_row + 1):
            row_data = []
            for col in range(start_col, end_col + 1):
                row_data.append(ws.cell(row=row, column=col).value)
            data.append(row_data)
        
        return data
    
    def export_to_dict(self, start_row: int = 1, start_col: int = 1,
                       end_row: Optional[int] = None, end_col: Optional[int] = None,
                       has_headers: bool = True, worksheet: Optional[Any] = None) -> List[Dict]:
        """Export data to list of dictionaries."""
        ws = worksheet or self.manager.current_worksheet
        
        if end_row is None:
            end_row = ws.max_row
        if end_col is None:
            end_col = ws.max_column
        
        data = []
        
        if has_headers:
            # Read headers
            headers = []
            for col in range(start_col, end_col + 1):
                headers.append(ws.cell(row=start_row, column=col).value)
            
            # Read data rows
            for row in range(start_row + 1, end_row + 1):
                row_data = {}
                for col_idx, header in enumerate(headers):
                    row_data[header] = ws.cell(row=row, column=start_col + col_idx).value
                data.append(row_data)
        else:
            # Read all rows as data
            for row in range(start_row, end_row + 1):
                row_data = {}
                for col in range(start_col, end_col + 1):
                    row_data[f"Column_{col}"] = ws.cell(row=row, column=col).value
                data.append(row_data)
        
        return data


class ValidationOperations:
    """Data validation operations."""
    
    def __init__(self, excel_manager: ExcelManager):
        """Initialize validation operations with Excel manager."""
        self.manager = excel_manager
    
    def add_dropdown_validation(self, row: int, col: int, options: List[str],
                                worksheet: Optional[Any] = None) -> None:
        """Add dropdown validation to a cell."""
        ws = worksheet or self.manager.current_worksheet
        cell = ws.cell(row=row, column=col)
        
        from openpyxl.worksheet.datavalidation import DataValidation
        dv = DataValidation(type="list", formula1=f'"{",".join(options)}"')
        dv.add(cell)
        ws.add_data_validation(dv)
    
    def add_number_validation(self, row: int, col: int, min_val: Optional[float] = None,
                              max_val: Optional[float] = None, worksheet: Optional[Any] = None) -> None:
        """Add number validation to a cell."""
        ws = worksheet or self.manager.current_worksheet
        cell = ws.cell(row=row, column=col)
        
        from openpyxl.worksheet.datavalidation import DataValidation
        dv = DataValidation(type="whole")
        
        if min_val is not None and max_val is not None:
            dv.operator = "between"
            dv.formula1 = min_val
            dv.formula2 = max_val
        elif min_val is not None:
            dv.operator = "greaterThanOrEqual"
            dv.formula1 = min_val
        elif max_val is not None:
            dv.operator = "lessThanOrEqual"
            dv.formula1 = max_val
        
        dv.add(cell)
        ws.add_data_validation(dv)


def create_sample_excel_file(file_path: str = "sample.xlsx") -> None:
    """Create a sample Excel file with various features."""
    if not EXCEL_AVAILABLE:
        print("openpyxl library is required. Install with: pip install openpyxl")
        return
    
    manager = ExcelManager()
    manager.create_workbook()
    
    # Create operations
    cell_ops = CellOperations(manager)
    style_ops = StylingOperations(manager)
    formula_ops = FormulaOperations(manager)
    import_export = DataImportExport(manager)
    
    # Sample data
    headers = ["Name", "Age", "Salary", "Department"]
    data = [
        ["John Doe", 30, 50000, "Engineering"],
        ["Jane Smith", 25, 45000, "Marketing"],
        ["Bob Johnson", 35, 60000, "Engineering"],
        ["Alice Brown", 28, 55000, "Sales"],
        ["Charlie Wilson", 32, 58000, "Engineering"]
    ]
    
    # Write headers with style
    import_export.import_from_list([headers], 1, 1)
    header_style = style_ops.create_header_style()
    style_ops.apply_style_to_range(1, 1, 1, 4, header_style)
    
    # Write data
    import_export.import_from_list(data, 2, 1)
    
    # Apply number style to salary column
    number_style = style_ops.create_number_style()
    style_ops.apply_style_to_range(2, 3, 6, 3, number_style)
    
    # Add formulas
    formula_ops.sum_range(2, 3, 6, 3, 7, 3)
    formula_ops.average_range(2, 3, 6, 3, 8, 3)
    formula_ops.max_range(2, 3, 6, 3, 9, 3)
    formula_ops.min_range(2, 3, 6, 3, 10, 3)
    
    # Add labels for formulas
    cell_ops.write_cell(7, 2, "Total:")
    cell_ops.write_cell(8, 2, "Average:")
    cell_ops.write_cell(9, 2, "Max:")
    cell_ops.write_cell(10, 2, "Min:")
    
    # Auto-fit columns
    style_ops.auto_fit_all_columns()
    
    # Save
    manager.save_workbook(file_path)
    manager.close()
    
    print(f"Sample Excel file created: {file_path}")


def demonstrate_excel_processing():
    """Demonstrate Excel processing functionality."""
    print("=== Excel Processing Demonstration ===\n")
    
    if not EXCEL_AVAILABLE:
        print("openpyxl library is required. Install with: pip install openpyxl")
        return
    
    # Create sample file
    print("1. Creating sample Excel file...")
    create_sample_excel_file("demo.xlsx")
    
    # Load and read
    print("\n2. Loading and reading Excel file...")
    manager = ExcelManager("demo.xlsx")
    manager.load_workbook("demo.xlsx")
    
    print(f"   Worksheets: {manager.list_worksheets()}")
    
    # Read data
    import_export = DataImportExport(manager)
    data = import_export.export_to_list(1, 1, 6, 4)
    print(f"   Data read: {len(data)} rows")
    
    # Cell operations
    print("\n3. Cell operations...")
    cell_ops = CellOperations(manager)
    print(f"   Cell A1: {cell_ops.read_cell(1, 1)}")
    cell_ops.write_cell(11, 1, "Additional Data")
    print(f"   Written to A11: {cell_ops.read_cell(11, 1)}")
    
    # Styling
    print("\n4. Styling operations...")
    style_ops = StylingOperations(manager)
    title_style = style_ops.create_title_style()
    style_ops.apply_style(11, 1, title_style)
    print("   Applied title style to cell A11")
    
    # Formulas
    print("\n5. Formula operations...")
    formula_ops = FormulaOperations(manager)
    cell_ops.write_cell(7, 5, "Total:")
    formula_ops.sum_range(2, 3, 6, 3, 7, 6)
    print(f"   SUM formula added to F7")
    
    # Dictionary import/export
    print("\n6. Dictionary import/export...")
    dict_data = [
        {"Product": "Laptop", "Price": 999, "Stock": 10},
        {"Product": "Mouse", "Price": 29, "Stock": 50},
        {"Product": "Keyboard", "Price": 79, "Stock": 25}
    ]
    
    manager.create_worksheet("Products")
    manager.set_active_worksheet("Products")
    import_export.import_from_dict(dict_data, 1, 1)
    print(f"   Imported {len(dict_data)} products to Products sheet")
    
    exported = import_export.export_to_dict(1, 1, 4, 3)
    print(f"   Exported back: {len(exported)} records")
    
    # Save and close
    print("\n7. Saving workbook...")
    manager.save_workbook("demo_updated.xlsx")
    manager.close()
    print("   Saved as demo_updated.xlsx")
    
    # Cleanup
    try:
        os.remove("demo.xlsx")
        os.remove("demo_updated.xlsx")
        print("\n8. Cleanup: Removed demo files")
    except:
        pass
    
    print("\n=== Demonstration Complete ===")


if __name__ == "__main__":
    demonstrate_excel_processing()