from __future__ import annotations

import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    """Basic request logging to help trace unexpected issues in production."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        logger.info(
            "request",
            extra={
                "path": request.path,
                "method": request.method,
                "status_code": response.status_code,
            },
        )
        return response
