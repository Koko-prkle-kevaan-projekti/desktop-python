import os
import dotenv
from tassu_tutka import error


class Settings:
    @staticmethod
    def load_settings():
        """Load settings as environment variables."""
        dotenv.load_dotenv(f"{os.getenv('HOME')}/.ttutka.dotenv")

    @staticmethod
    def save_settings(**kwargs: str):
        """Save settings to ~/.ttutka.dotenv

        Update existing values.
        """
        home = os.getenv("HOME") or ""
        if not home:
            raise error.NoHomeDirectoryFound(
                "Need to have home directory for settings file."
            )
        for k, v in kwargs.items():
            dotenv.set_key(f"{home}/.ttutka.dotenv", k, v)

    @staticmethod
    def wipe_settings():
        home = os.getenv("HOME") or ""
        if not home:
            raise error.NoHomeDirectoryFound(
                "Need to have home directory for settings file."
            )
        with open(home + "/.ttutka.dotenv", "w") as fh:
            pass
