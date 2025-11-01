from celery import Celery

celery_app = Celery(
    'deepseek_clone',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
)


@celery_app.task
def process_file(file_path: str) -> str:
    return f"Processed {file_path} in background."
