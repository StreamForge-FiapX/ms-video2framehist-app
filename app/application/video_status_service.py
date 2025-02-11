from app.domain.video_status import VideoStatus
from app.adapters.redis_video_status_repository import RedisVideoStatusRepository

class VideoStatusService:
    def __init__(self, repository: RedisVideoStatusRepository):
        self.repository = repository

    def get_video_statuses(self, user_email: str):
        keys = self.repository.get_user_video_keys(user_email)
        video_statuses = []

        for key in keys:
            data = self.repository.get_video_status_data(key)
            if data:
                video_status = VideoStatus(
                    file_name=data.get("video_title", "Desconhecido"),
                    status=data.get("status", "Desconhecido"),
                    upload_timestamp=data.get("last_updated", ""),
                    s3_object_key=data.get("s3_uri", "")
                )
                video_statuses.append(video_status)

        return video_statuses
