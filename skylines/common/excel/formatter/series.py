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
# Configuration: color and pattern maps
# -----------------------------
COLOR_MAP = {
    "Non-Causal": hex_to_rgb_int("#7F7F7F"),
    "Pref. Decor.": hex_to_rgb_int("#4EA72E"),
    "ddSky.": hex_to_rgb_int("#E97132"),
    "gnSky.": hex_to_rgb_int("#156082"),
    "lnSky. (0.9, 0.1)": hex_to_rgb_int("#0F9ED5"),
    "lnSky. (0.8, 0.2)": hex_to_rgb_int("#196B24"),
    "lnSky. (0.7, 0.3)": hex_to_rgb_int("#A02B93"),
    "lnSky. (0.6, 0.4)": hex_to_rgb_int("#0D3A4E"),
    "lnSky. w/ inf. DAG": hex_to_rgb_int("#009E73"),

    "(1.0, 0.0)": hex_to_rgb_int("#156082"),
    "(0.9, 0.1)": hex_to_rgb_int("#0F9ED5"),
    "(0.8, 0.2)": hex_to_rgb_int("#196B24"),
    "(0.7, 0.3)": hex_to_rgb_int("#A02B93"),
    "(0.6, 0.4)": hex_to_rgb_int("#0D3A4E"),

    "50K": hex_to_rgb_int("#BDBDFF"),
    "100K": hex_to_rgb_int("#A4EA58"),
    "200K": hex_to_rgb_int("#96CEFC"),
    "400K": hex_to_rgb_int("#FFC000"),

    "5 clusters": hex_to_rgb_int("#DE82A5"),
    "10 clusters": hex_to_rgb_int("#8FC3A3"),
    "15 clusters": hex_to_rgb_int("#92B4E6"),
    "20 clusters": hex_to_rgb_int("#E9D065"),
}

# -----------------------------
# Patterns
# -----------------------------
PATTERN_LIST = [
    None,  # no pattern
    34,    # msoPatternLargeGrid
    36,    # msoPatternLargeCheckerBoard
    14,    # msoPatternDarkVertical
    13,    # msoPatternDarkHorizontal
    33,    # msoPatternLargeConfetti
    32,    # msoPatternDashedHorizontal
    25,    # msoPatternWideDownwardDiagonal
    26,    # msoPatternWideUpwardDiagonal
]

PATTERN_MAP = {
    "Non-Causal": PATTERN_LIST[0],
    "Pref. Decor.": PATTERN_LIST[1],
    "ddSky.": PATTERN_LIST[2],
    "gnSky.": PATTERN_LIST[3],
    "lnSky. (0.9, 0.1)": PATTERN_LIST[4],
    "lnSky. (0.8, 0.2)": PATTERN_LIST[5],
    "lnSky. (0.7, 0.3)": PATTERN_LIST[6],
    "lnSky. (0.6, 0.4)": PATTERN_LIST[7],
    "lnSky. w/ inf. DAG": PATTERN_LIST[8],

    "(1.0, 0.0)": PATTERN_LIST[3],
    "(0.9, 0.1)": PATTERN_LIST[4],
    "(0.8, 0.2)": PATTERN_LIST[5],
    "(0.7, 0.3)": PATTERN_LIST[6],
    "(0.6, 0.4)": PATTERN_LIST[7],

    "50K": PATTERN_LIST[0],
    "100K": PATTERN_LIST[1],
    "200K": PATTERN_LIST[2],
    "400K": PATTERN_LIST[3],

    "5 clusters": PATTERN_LIST[0],
    "10 clusters": PATTERN_LIST[1],
    "15 clusters": PATTERN_LIST[2],
    "20 clusters": PATTERN_LIST[3],
}

# Numeric chart type constants for columns/bars
COLUMN_BAR_TYPES = [51, 52, 53, 57, 58, 59]

# -----------------------------
# Open Excel
# -----------------------------
excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = False  # optional: False for background execution

file_path = choose_excel_file()
if not file_path:
    sys.exit(0)

wb = excel.Workbooks.Open(file_path)

# -----------------------------
# Apply colors and patterns
# -----------------------------
for ws in wb.Sheets:
    for chart_obj in ws.ChartObjects():
        chart = chart_obj.Chart
        if chart.ChartType not in COLUMN_BAR_TYPES:
            continue

        for series in chart.SeriesCollection():
            name = series.Name
            if name in COLOR_MAP:
                # Set fill color
                series.Format.Fill.ForeColor.RGB = COLOR_MAP[name]

                # Set fill pattern
                if name in PATTERN_MAP and PATTERN_MAP[name] is not None:
                    series.Format.Fill.Patterned(PATTERN_MAP[name])
                else:
                    series.Format.Fill.Solid()
                
                # Set border same as fill
                series.Format.Line.Visible = True
                series.Format.Line.ForeColor.RGB = COLOR_MAP[name]
                series.Format.Line.Weight = 1  # adjust thickness if needed
        
        # Handle legends
        if chart.HasLegend:
            chart.Legend.Format.TextFrame2.TextRange.Font.Size = 27
            chart.Legend.Format.TextFrame2.TextRange.Font.Superscript = True
            chart.Legend.Format.TextFrame2.TextRange.Font.BaselineOffset = 0.04

# -----------------------------
# Save and close
# -----------------------------
wb.Save()
wb.Close()
excel.Quit()

print("Bar charts updated with colors and patterns!")
