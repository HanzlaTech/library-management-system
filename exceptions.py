from logger import log
from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from customclass import InternalServer_Error
async def handler503(request:Request,exc:Exception):
    return JSONResponse(
        status_code=503,
        content={"msg":"Service Unavailable","Status":False}
    )

async def handler429(request:Request,exc:Exception):
    return JSONResponse(
        status_code=409,
        content={'msg':'Retry after sometime','status':False}
    )

async def handler422(request,exc:Exception):
    return JSONResponse(
        status_code=422,
        content={'msg':'Invalid data is send from Request','status':False}
    )


async def handler403(request:Request,exc:Exception):
    if isinstance(exc,HTTPException):
     return JSONResponse(
        status_code=exc.status_code,
        content={'msg':exc.detail,'status':False}
    )
    else:
       return JSONResponse(
          status_code=403,
          content={'msg':'Role invalid','status':False}
       )

async def handler500(req,exc:Exception):
   if isinstance(exc,InternalServer_Error):
    return JSONResponse(
        status_code=exc.code,
        content={'msg':exc.msg,'status':False}
    )
   else :
      return JSONResponse(
         status_code=500,
         content={'msg':'Internal Server Error','status':False}
      )