{%- if cookiecutter.with_cli and cookiecutter.with_cli_history %}
from pathlib import Path

from pydantic import field_validator
{% endif -%}
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="{{ cookiecutter.settings_env_prefix | lower }}_",
        env_nested_delimiter="__",
    )

    {%- if cookiecutter.with_cli and cookiecutter.with_cli_history %}

    CLI_HISTORY: bool = True
    """Save CLI history to a file.

    See Also:
        :attr:`.CLI_HISTORY_FILE`.
    """

    CLI_HISTORY_FILE: Path = "~/.{{ cookiecutter.project_slug | replace('_', '-')}}-history"
    """CLI history filename.

    See Also:
        :attr:`.CLI_HISTORY`.
    """

    @field_validator("CLI_HISTORY_FILE", mode="before")
    def validate_cli_history_file(cls, v: Path) -> Path:
        return Path(v).expanduser().resolve()
    {%- endif %}


settings = Settings()

