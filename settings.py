from pydantic import BaseSettings, HttpUrl

class OuterAPISettings(BaseSettings):
    # 人力系统
    hr_base_url: HttpUrl = "https://hr.example.com/api/v1"
    hr_client_id: str
    hr_client_secret: str
    hr_token_ttl: int = 3600  # 秒

    # 财务系统
    finance_base_url: HttpUrl = "https://finance.example.com/open-api"
    finance_username: str
    finance_password: str
    finance_token_ttl: int = 7200

    class Config:
        env_file = ".env"   # 本地开发放 .env，生产用环境变量

settings = OuterAPISettings()