import re


class Validate:
    def __init__(self, to_validate):
        self.to_validate = to_validate

    def password(self):
        regex = "[A-Za-z0-9@#$%^&+=_]{8,150}"
        if re.fullmatch(regex, self.to_validate):
            return True
        return False

    def name(self):
        regex = "[A-za-z ,-ÄÖÜäöüß]{3,150}"
        if re.fullmatch(regex, self.to_validate):
            return True
        return False

    def email(self):
        regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+.([A-Z|a-z]{2,})+"
        if re.fullmatch(regex, self.to_validate):
            return True
        return False

    def group_name(self):
        regex = "[A-za-z ,-ÄÖÜäöüß0-9]{3,100}"
        if re.fullmatch(regex, self.to_validate):
            return True
        return False


