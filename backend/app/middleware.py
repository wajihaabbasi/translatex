from fastapi.middleware.cors import CORSMiddleware

def initialize_application_middleware(app_instance) -> None:
    """
    Configures application-wide security settings, 
    including Cross-Origin Resource Sharing (CORS).
    """
    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )