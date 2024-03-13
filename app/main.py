"""
    Definition of app
"""
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi, JSONResponse

from .routes import user

app = FastAPI()
app.include_router(user.router)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    """
        Handler to retrieve  and return exceptions
        :param request:
        :param exc:
        :return:
    """
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


def custom_openapi():
    """
        Creates swagger document for apis
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CRUD Operations",
        version="1.0.0",
        description="",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi_schema = custom_openapi()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
