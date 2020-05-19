import datetime
import os.path

__name__ = "__logger__"


class Logger:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if Logger.__instance is None:
            Logger.__instance = object.__new__(cls)

        return Logger.__instance

    def __init__(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            self.path_logger = os.path.join(path, "log.log")
            with open(self.path_logger, "w") as f:
                f.write(f"Logger initialized at {datetime.datetime.now()}\n")
                f.close()

    def log(self, message,):
        with open(self.path_logger, "a") as f:
            f.write(f"{datetime.datetime.now()}: {message}\n")
            f.close()


if __name__ == "__logger__":
    pass



