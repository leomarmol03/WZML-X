"""Optional adapter for the native MEGA SDK Python bindings.

The Docker base image used by WZML-X provides a compiled ``mega`` module,
but that native extension is not part of the project's pip requirements. Keep
MEGA an optional integration so the rest of the bot can run in bare Linux
runtimes (including Google Colab) without silently importing an incompatible
PyPI package named ``mega``.
"""

try:
    from mega import (
        MegaApi,
        MegaCancelToken,
        MegaError,
        MegaListener,
        MegaRequest,
        MegaTransfer,
        MegaUploadOptions,
    )
except (ImportError, OSError) as exc:
    _binding_error = exc
else:
    _missing_api = [
        name
        for name in ("startDownload", "startUpload")
        if not callable(getattr(MegaApi, name, None))
    ]
    if not callable(getattr(MegaUploadOptions, "createInstance", None)):
        _missing_api.append("MegaUploadOptions.createInstance")
    _binding_error = (
        ImportError(
            "The imported 'mega' module does not expose the WZML-X API: "
            + ", ".join(_missing_api)
        )
        if _missing_api
        else None
    )

MEGA_SDK_IMPORT_ERROR = _binding_error
MEGA_SDK_AVAILABLE = _binding_error is None
MEGA_DISABLED_MESSAGE = (
    "MEGA is disabled or unavailable in this runtime. Use another source/destination "
    "or install the compatible native MEGA SDK binding."
)
MEGA_SDK_REQUIRED_MESSAGE = (
    "MEGA support requires the compatible native MEGA SDK Python binding, "
    "which is not installed or could not be loaded in this runtime."
)


class MegaSDKUnavailableError(RuntimeError):
    """Raised when a MEGA operation is attempted without its native SDK."""


def require_mega_sdk():
    """Fail with a clear error rather than an obscure missing-binding error."""
    if not MEGA_SDK_AVAILABLE:
        raise MegaSDKUnavailableError(
            MEGA_SDK_REQUIRED_MESSAGE
        ) from MEGA_SDK_IMPORT_ERROR


if not MEGA_SDK_AVAILABLE:

    class _UnavailableSDKType:
        def __init__(self, *args, **kwargs):
            require_mega_sdk()

        @classmethod
        def createInstance(cls, *args, **kwargs):
            require_mega_sdk()

        def __getattr__(self, name):
            require_mega_sdk()

    class MegaApi(_UnavailableSDKType):
        pass

    class MegaListener:
        def __init__(self, *args, **kwargs):
            pass

    class MegaError:
        API_OK = 0
        API_EAGAIN = -3
        API_ERATELIMIT = -4
        API_EINCOMPLETE = -13
        API_EOVERQUOTA = -17

    class MegaRequest:
        TYPE_ACCOUNT_DETAILS = 0
        TYPE_FETCH_NODES = 1
        TYPE_LOGIN = 2
        TYPE_EXPORT = 3
        TYPE_CREATE_FOLDER = 4
        TYPE_IMPORT_LINK = 5
        TYPE_GET_PUBLIC_NODE = 6

    class MegaTransfer:
        TYPE_UPLOAD = 0

    class MegaUploadOptions(_UnavailableSDKType):
        pass

    MegaCancelToken = None
