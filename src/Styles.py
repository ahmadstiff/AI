from openpyxl.styles import Font, Color, PatternFill, Alignment, NamedStyle

__fontTitle = Font(
    name="Times New Roman",
    size=12,
    bold=True,
    italic=False,
    underline="none",
    strike=False,
    color="00FFFFFF",
)

__headerBgColor = PatternFill(
    fgColor="00000080",
    fill_type="solid",
)

__headerAlignment = Alignment(
    horizontal="center",
    vertical="center",
    text_rotation=0,
    wrap_text=True,
    shrink_to_fit=True,
    indent=0,
)

headerStyle = NamedStyle('headerStyle')
headerStyle.font = __fontTitle
headerStyle.fill = __headerBgColor
headerStyle.alignment = __headerAlignment

cellAlignment = Alignment(
    horizontal="center",
    vertical="center",
    text_rotation=0,
    wrap_text=True,
    shrink_to_fit=True,
    indent=0,
)