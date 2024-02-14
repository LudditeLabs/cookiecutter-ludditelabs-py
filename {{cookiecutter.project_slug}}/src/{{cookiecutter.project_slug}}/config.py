{%- if cookiecutter.with_cli and cookiecutter.with_cli_history %}
from pathlib import Path

{% endif -%}
from pydantic import BaseSettings{% if cookiecutter.with_cli and cookiecutter.with_cli_history %}, validator{% endif %}


class Settings(BaseSettings):
    class Config:
        env_prefix = "{{ cookiecutter.project_slug }}_"
        env_nested_delimiter = "__"

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

    @validator("CLI_HISTORY_FILE", pre=True)
    def validate_cli_history_file(cls, v: Path) -> Path:
        return Path(v).expanduser().resolve()
    {%- endif %}


{% if cookiecutter.with_cli %}settings = Settings(){% endif %}
