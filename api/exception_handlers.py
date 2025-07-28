from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def qloo_api_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Exception handler for Qloo API failures.
    Returns compliant error response as per hackathon requirements.
    
    On Qloo error, FastAPI returns 502 JSON {"error": "Qloo API failure"}
    """
    # Check if this is a Qloo-related error
    if exc.status_code == 502 and "Qloo API failure" in str(exc.detail):
        logger.error(f"Qloo API failure on {request.url}: {exc.detail}")
        
        return JSONResponse(
            status_code=502,
            content={"error": "Qloo API failure"}
        )
    
    # Re-raise if not a Qloo error
    raise exc

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    General exception handler for unexpected errors.
    Ensures consistent error format.
    """
    logger.error(f"Unexpected error on {request.url}: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
