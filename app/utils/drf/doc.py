class ResponseErrors(object):
    def __new__(cls, title, *errors):
        return cls.to_dict(title, *errors)

    @staticmethod
    def to_dict(title, *errors):
        return {
            title: {
                error.case: {
                    'code': error.code,
                    'message': error.message,
                } for error in errors
            }
        }
