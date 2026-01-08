from pydantic import BaseModel
from typing import List, Any, Optional, Dict

class CellStyle(BaseModel):
    bg_color: Optional[str] = None  # Hex color: "FF0000" para rojo
    font_color: Optional[str] = None
    bold: Optional[bool] = False
    italic: Optional[bool] = False
    font_size: Optional[int] = 11
    alignment: Optional[str] = None  # "center", "left", "right"

class ColumnConfig(BaseModel):
    name: str
    width: Optional[float] = None  # Ancho de columna
    style: Optional[CellStyle] = None

class ExcelRequestDto(BaseModel):
    columns: List[str]
    rows: List[List[Any]]
    filename: Optional[str] = "archive.xlsx"
    
    # Nuevos campos para diseño
    header_style: Optional[CellStyle] = None
    column_configs: Optional[List[ColumnConfig]] = None
    row_styles: Optional[Dict[int, CellStyle]] = None  # Estilos por fila