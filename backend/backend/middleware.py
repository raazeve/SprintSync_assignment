# middleware.py
import logging
import time

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        user_id = request.user.id if request.user.is_authenticated else "anonymous"

        log_data = {
            "method": request.method,
            "path": request.path,
            "user_id": user_id,
            "status_code": response.status_code,
            "latency": round(duration, 4)
        }
        logger.info(msg="API Request", extra=log_data)

        if 400 <= response.status_code < 500:
            logger.warning(msg="Client Error", extra=log_data)
        elif response.status_code >= 500:
            logger.error(msg="Server Error", extra=log_data)

        return response