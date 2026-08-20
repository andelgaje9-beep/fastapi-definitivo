"""
Módulo de configuración de la aplicación.

Este archivo centraliza la carga de variables de entorno y parámetros 
de seguridad/infraestructura. Utiliza la clase Settings basada en 
Pydantic para validar y acceder a valores como la URL de la base de datos, 
la clave secreta para JWT y el tiempo de expiración de los tokens.

La idea es mantener la configuración desacoplada del código, 
permitiendo cambiar fácilmente entre entornos (local, render, producción) 
mediante archivos .env específicos. 

Se expone una instancia global `settings` que puede importarse en cualquier 
parte de la aplicación para acceder a la configuración.
"""


# from pydantic_settings import BaseSettings
# from pydantic import ConfigDict

# class Settings(BaseSettings):
#     database_hostname : str
#     database_port: str 
#     database_password: str 
#     database_name: str
#     database_username: str
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int
    
#     model_config = ConfigDict(env_file=".env")
    
# settings = Settings()

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.getenv("ENVIRONMENT", "local")


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env.render" if env == "render" else ".env"
    )


settings = Settings()
print(settings)



