import asyncio
from asyncio.tasks import create_task
from functools import wraps
from starlette.concurrency import run_in_threadpool
import logging
from typing import Callable, Optional, Awaitable

logger = logging.getLogger('main')



# Copied from code shared on Gitter (https://gitter.im/tiangolo/fastapi) by @dmontagu
# Decorator for fastapi
def repeat_every(*, seconds: float, wait_first: bool = False):
    def decorator(func: Callable[[], Optional[Awaitable[None]]]):
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped():
            async def loop():
                if wait_first:
                    await asyncio.sleep(seconds)
                while True:
                    try:
                        if is_coroutine:
                            await func()
                        else:
                            await run_in_threadpool(func)
                    except Exception as e:
                        logger.error(str(e))
                    await asyncio.sleep(seconds)

            create_task(loop())

        return wrapped

    return decorator
