class BaseServiceError(Exception):
    code = 500


class ItemNotFound(BaseServiceError):
    code = 404


class RegisterError(BaseServiceError):
    code = 400


class DataError(BaseServiceError):
    code = 400
