from datetime import datetime
from io import BytesIO
import base64
from typing import List
from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import EmailStr, UUID4
from sqlalchemy.ext.asyncio import AsyncSession
import segno
import uuid

from app.database import get_async_session
from app.repository.reviewer import ReviewerRepository
from app.schemas import AddReview, QRImageData, Review
from app.utils.enums import Status
from app import http_exceptions as http_e
from app.configs.config import settings

router = APIRouter()

@router.post(
        path="/reviews/actions/create_review",
        response_model=QRImageData
        )
async def create_review(
    files_upload: List[UploadFile] = File(default=None, description="Important: Unset 'Send empty value', otherwise won't work"),
    review_text: str = Form(min_length=8, max_length=255),
    # Опциональные для заполнения заявителем поля
    email: EmailStr = Form(default=None),
    first_name: str = Form(default=None, min_length=2, max_length=32),
    last_name: str = Form(default=None, min_length=2, max_length=32),
    patronymic: str = Form(default=None, min_length=2, max_length=32),
    department: str = Form(default=None, min_length=2, max_length=64, description="Department of... "),
    session: AsyncSession = Depends(get_async_session)
    ):

    filenames = []

    # Если были получены какие-то файлы
    if files_upload:
        SUPPORTED_FiLETYPES = ["image/png", "image/jpg", "image/jpeg"]
        # Проверяем, каждый ли файл удовлетворяет ограничениям
        for file in files_upload:
            # Фильтруем формат файла
            if file.content_type not in SUPPORTED_FiLETYPES:
                raise http_e.UnsupportedMediaType
            
            # Фильтруем размер файла
            if file.size > settings.MAXIMUM_UPLOAD_FILE_SIZE_BYTES:
                raise http_e.FileSizeCapOverflowException(filename=file.filename, max_size=settings.MAXIMUM_UPLOAD_FILE_SIZE_BYTES)

        # Путь до папки с изображениями относительно данного файла
        IMAGES_DIRECTORY = "images/"
        for file in files_upload:
            file_contents = file.file.read()
            filename_random = f"{str(uuid.uuid4())}_{file.filename}"
            with open(f"{IMAGES_DIRECTORY}{filename_random}", 'wb') as file_object:
                file_object.write(file_contents)
                file_object.close()
            
            filenames.append(filename_random)
    
    review = AddReview(
        # Красивый вывод: datetime.now(timezone.utc).strftime('%d.%m.%Y - %H:%M')
        review_creation_date = datetime.utcnow(),
        review_status = Status.Created,
        review_text = review_text,
        email = email,
        first_name = first_name,
        last_name = last_name,
        patronymic = patronymic,
        department = department,
        images = dict(filenames = filenames)
    )

    review_uuid = await ReviewerRepository.AddReview(session, review)

    BACKEND_ENDPOINT = "api/reviews/actions/see_review/id?uuid="
    FRONTEND_ENDPOINT = "frontend_endpoint"
    review_link = f"{settings.WEB_APP_URL}:{settings.FRONTEND_PORT}/{FRONTEND_ENDPOINT}/{review_uuid}"

    # Создаём QR
    QR_Bytes = segno.make(content=review_link, micro=False)
    # Создаем буфер
    buffer = BytesIO()
    # Сохраняем байты изображения QR-кода в буфер
    QR_Bytes.save(
        buffer,
        kind="png",
        scale=5.0
        )
    
    qr_image_data = QRImageData(
        review_uuid=str(review_uuid),
        mime="image/png",
        image_base64_bytes=base64.b64encode(buffer.getvalue())
    )

    return qr_image_data


@router.get(
        path="/reviews/actions/see_review/{id}",
        response_model=Review
        )
async def see_review_by_uuid(
    uuid: UUID4,
    session: AsyncSession = Depends(get_async_session)
    ):

    review = await ReviewerRepository.GetReviewByUUID(session, uuid)
    if review is None:
        raise http_e.ReviewNotFoundException
    return review