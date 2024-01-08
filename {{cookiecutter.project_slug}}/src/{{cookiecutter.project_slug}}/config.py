from pydantic import BaseSettings


class Settings(BaseSettings):
    pass

{%- if cookiecutter.with_cli == "y" %}
settings = Settings()
{%- endif %}
