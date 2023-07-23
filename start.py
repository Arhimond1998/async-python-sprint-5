import os
import uvicorn
from src.core.config import settings


if __name__ == '__main__':
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    os.environ.update({
        "NLS_LANG": "RUSSIAN_RUSSIA.UTF8",
        "PROJECT_ROOT": PROJECT_ROOT
    })

    uvicorn.run(
        'src.main:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        lifespan='on',
        access_log=True,
        loop='uvloop',
        reload=True
    )
