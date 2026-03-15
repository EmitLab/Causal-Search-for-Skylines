import sys
import win32com.client as win32
from tkinter import Tk, filedialog

# -----------------------------
# Helper: file chooser dialog
# -----------------------------
def choose_excel_file():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select Excel file",
        filetypes=[
            ("Excel files", "*.xlsx *.xls *.xlsm *.xlsb"),
        ]
    )

# -----------------------------
# Helper: convert #RRGGBB to Excel RGB int
# -----------------------------
def hex_to_rgb_int(hex_str: str) -> int:
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return b << 16 | g << 8 | r

# -----------------------------
# Category color map
# -----------------------------
COLOR_MAP = {
    "BNL":   hex_to_rgb_int("#00B4B0"),
    "SFS":   hex_to_rgb_int("#E9D065"),
    "SaLSa": hex_to_rgb_int("#92B4E6"),
    "D&C":   hex_to_rgb_int("#8FC3A3"),
    "BBS":   hex_to_rgb_int("#DE82A5"),
}

# -----------------------------
# Marker styles (distinct & readable)
# -----------------------------
MARKER_MAP = {
    "BNL":   None,  # no marker
    "SFS":   8,     # xlMarkerStyleCircle
    "SaLSa": 2,     # xlMarkerStyleDiamond
    "D&C":   1,     # xlMarkerStyleSquare
    "BBS":   3,     # xlMarkerStyleTriangle
}

# Line chart types
LINE_CHART_TYPES = [4, 65, 66, 67]

# -----------------------------
# Open Excel
# -----------------------------
excel = win32.gencache.EnsureDispatch("Excel.Application")
excel.Visible = False

file_path = choose_excel_file()
if not file_path:
    sys.exit(0)

wb = excel.Workbooks.Open(file_path)

# -----------------------------
# Apply styling
# -----------------------------
for ws in wb.Sheets:
    for chart_obj in ws.ChartObjects():
        chart = chart_obj.Chart
        if chart.ChartType not in LINE_CHART_TYPES:
            continue

        for series in chart.SeriesCollection():
            name = series.Name
            if name not in COLOR_MAP:
                continue

            color = COLOR_MAP[name]

            # Line
            series.Format.Line.Visible = True
            series.Format.Line.ForeColor.RGB = color
            series.Format.Line.Weight = 2

            # Marker
            if name in MARKER_MAP and MARKER_MAP[name] is not None:
                series.MarkerStyle = MARKER_MAP[name]
                series.MarkerSize = 7
                series.MarkerForegroundColor = color
                series.MarkerBackgroundColor = color

# -----------------------------
# Save & close
# -----------------------------
wb.Save()
wb.Close()
excel.Quit()

print("Line charts updated using category-based colors and markers!")
