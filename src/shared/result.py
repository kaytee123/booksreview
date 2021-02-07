
class Error():
    def __init__(self, message, code="", extension={}):
        self.__message = message
        self.__code = code
        self.__extension = extension

    def to_dict(self):
        return {
            'code': self.__code,
            'extension': self.__extension,
            'message': self.__message,
        }


class Result:

    def __init__(self, status, data):
        self.__status = status
        self.__data = data

    @staticmethod
    def ok(data):
        return Result("ok", data)

    @staticmethod
    def err(error: Error):
        return Result("err", error)

    def match(self, ok_fn, err_fn):
        if self.__status == "ok":
            return ok_fn(self.__data)

        return err_fn(self.__data)

    def is_ok(self):
        return self.__data if self.__status == 'ok' else False

    def is_err(self):
        return self.__data if self.__status == 'err' else False
