import uvicorn
from fastapi import FastAPI
from app.middleware import initialize_application_middleware
from app.routes import router as api_router

def create_application() -> FastAPI:
    """Assembles and configures the FastAPI application instances cleanly."""

    application = FastAPI(
        title="TranslateX", 
        description="Real-time text translations powered by Groq."
    )
    
    # Inject security middlewares
    initialize_application_middleware(application)
    
    # Mount modular application routes sub-trees
    application.include_router(api_router)
    
    return application

app = create_application()

if __name__ == "__main__":
    # Bootstraps local debugging microserver configurations directly using main modules
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)