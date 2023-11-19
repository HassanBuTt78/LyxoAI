OPENAI_API = "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"
DATABASE_URI = "mongodb+srv://Hassan:hassan@cluster0.wmrmexl.mongodb.net/"

class Config:
    DEBUG = False
    OPENAI_API = "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"
    DATABASE_URI = "mongodb+srv://Hassan:hassan@cluster0.wmrmexl.mongodb.net/"

    # Other configuration settings

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False