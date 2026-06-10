from fastapi import Request


async def dummy_auth_middleware(request: Request, call_next):
    # Placeholder: implement JWT/session auth here if needed
    response = await call_next(request)
    return response
