from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path as FilePath
from src.dto.ia import PromptRequestDto
from src.services.ia_services import generate_excel_structure
from src.dto.excel import ExcelRequestDto
from src.services.excel_services import createExcelService

router = APIRouter(
    prefix= "/excel",
    tags= ["EXCEL"]
)

@router.post("/")
def createExcel(body:ExcelRequestDto):
    return createExcelService(body)

@router.post("/from-prompt")
def create_excel_from_prompt(body: PromptRequestDto):
    print(f"\n Received prompt: {body.prompt}\n")
    
    try:
        data = generate_excel_structure(body.prompt)
        excel_data = ExcelRequestDto(
            columns=data["columns"],
            rows=data["rows"],
            filename="generated.xlsx",
            header_style=data.get("header_style"),
            column_configs=data.get("column_configs"),
            row_styles=data.get("row_styles")
        )
        
        result = createExcelService(excel_data)

        return {
            "success": True,
            "filename": result["filename"],
            "columns": result["columns"],
            "rows": result["rows"],
            "header_style": result["header_style"],
            "column_configs": result["column_configs"],
            "total_rows": result["total_rows"],
            "rows_added": result["rows_added"]
        }
    
    except ValueError as e:
        print(f"❌ ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    

@router.get("/download/{filename}")
def download_excel(filename: str):
    """
    Descarga el archivo Excel generado.
    """
    file_path = FilePath(filename)
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(path=file_path, filename=file_path.name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")