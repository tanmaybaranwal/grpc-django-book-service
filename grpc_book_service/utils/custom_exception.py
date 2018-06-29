class CustomException(Exception):
    def __init__(self, message='', res_status=''):
        super(CustomException, self).__init__(message)
        self.res_status = res_status
