from fastapi import APIRouter, HTTPException, BackgroundTasks, status, Depends

from backend.email.envio_email import send_email, generate_pdf_report
from backend.security import get_current_user
from core.models import User

router = APIRouter()


@router.post('/relatorios/enviar', status_code=status.HTTP_202_ACCEPTED)
async def post_send_email(
    background_tasks: BackgroundTasks, 
    current_user: User = Depends(get_current_user)):
    try:

        file_path = await generate_pdf_report(current_user.email)
        background_tasks.add_task(send_email, current_user, file_path)

        return {
            "status": "success",
            "message": f"E-mail para {current_user.email} está sendo processado para envio"
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro no servidor: " + str(e))