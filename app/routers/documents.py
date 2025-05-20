from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from app.schemas.document import DocumentCreate, DocumentRead, FileUploadResponse
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_services, Services

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED, summary="자료 등록")
async def create_document(
    payload: DocumentCreate, 
    user: dict = Depends(get_current_user), 
    service: Services = Depends(get_services)
):
    return await service.document.create_document(
        inspector_id=user["id"],
        course_id=payload.course_id,
        source_url=payload.source_url,
        source_type=payload.source_type
    )


@router.get("/{doc_id}/status", response_model=DocumentRead, status_code=status.HTTP_200_OK, summary="자료 상태 조회")
async def get_document(
    doc_id: str,
    user: dict = Depends(get_current_user),
    service: Services = Depends(get_services)
):
    return await service.document.get_document_status(inspector_id=user["id"], document_id=doc_id)


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED, summary="파일 업로드 후 URL반환")
async def upload_file(
    file: UploadFile = File(...),
    course_id: str = Form(...),
    user: dict = Depends(get_current_user),
    service: Services = Depends(get_services)
):
    try:
        url = await service.document.upload_file(
            inspector_id=user["id"],
            course_id=course_id,
            file=file
        )
    except HTTPException as e:
        raise e

    return FileUploadResponse(url=url)
