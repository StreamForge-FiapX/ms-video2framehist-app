import json
import logging
from app.application.video_status_service import VideoStatusService
from app.adapters.redis_video_status_repository import RedisVideoStatusRepository

# Configuração do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Consulta o Redis para obter os status dos vídeos do usuário.
    """
    try:
        # Extrai o email do usuário da requisição
        query_params = event.get("queryStringParameters", {})
        user_email = query_params.get("UserEmail")

        if not user_email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'UserEmail é obrigatório'})
            }

        # Criar instâncias de repositório e serviço
        redis_repository = RedisVideoStatusRepository()
        video_status_service = VideoStatusService(redis_repository)

        # Buscar os status dos vídeos do usuário
        video_statuses = video_status_service.get_video_statuses(user_email)

        # Retornar resposta
        return {
            'statusCode': 200,
            'body': json.dumps({'Items': [status.to_dict() for status in video_statuses]})
        }

    except Exception as e:
        logger.error(f"Erro ao buscar dados do Redis: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
