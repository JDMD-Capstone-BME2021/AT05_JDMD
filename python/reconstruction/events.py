from python.reconstruction.structs import ReconstructionOptions

from threading import Event
from threading import Lock
from python.reconstruction.structs import ImgLoadOptions


class ReconstructionEvent(Event):
    def __init__(self):
        super().__init__()
        self._lock = Lock()
        self._reconstruction_opts = None

    @property
    def reconstruction_options(self) -> ReconstructionOptions:
        return self._reconstruction_opts

    def set(self, opts):
        with self._lock:
            self._reconstruction_opts = opts
        super().set()

    def clear(self) -> None:
        with self._lock:
            self._reconstruction_opts = None
        super().clear()


class LoadimagesEvent(Event):
    def __init__(self):
        super().__init__()
        self._lock = Lock()
        self._load_opts = None

    @property
    def load_options(self) -> ImgLoadOptions:
        return self._load_opts

    def set(self, opts):
        with self._lock:
            self._load_opts = opts
        super().set()

    def clear(self) -> None:
        with self._lock:
            self._load_opts = None
        super().clear()
