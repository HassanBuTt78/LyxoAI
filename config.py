OPENAI_API = "Your Open API Key"
DATABASE_URI = "your mongodb URI"

class Config:
    DEBUG = False
    OPENAI_API = "Your Open API Key"
    DATABASE_URI = "your mongodb URI"

    # Other configuration settings

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
