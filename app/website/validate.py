import re


class Validate:
    def __init__(self, to_validate, regex):
        self.to_validate = to_validate
        self.regex = regex

    def check(self):
        if re.fullmatch(self.regex, self.to_validate):
            return True
        return False


class ValidatePassword(Validate):

    def __init__(self, to_validate):
        super().__init__(to_validate, "[A-Za-z0-9@#$%^&+=_]{8,150}")


class ValidateName(Validate):

    def __init__(self, to_validate):
        super().__init__(to_validate, "[A-za-z ,-ÄÖÜäöüß]{3,150}")


class ValidateEmail(Validate):

    def __init__(self, to_validate):
        super().__init__(to_validate, "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+.([A-Z|a-z]{2,})+")


class ValidateGroupname(Validate):

    def __init__(self, to_validate):
        super().__init__(to_validate, "[A-za-z ,-ÄÖÜäöüß0-9]{3,100}")



