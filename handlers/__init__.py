from aiogram import Router
# from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from .base_handlers import base_router
from .callback_handlers import callback_router
from .fsm_handlers import fsm_router
from .group_handlers import group_router
from .threading_handlers import threading_router

main_handler_router = Router(name=__name__)
main_handler_router.include_routers(
    base_router,
    callback_router,
    fsm_router,
    group_router,
    threading_router
)   
