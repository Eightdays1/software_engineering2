import re


class Validate:
    def __init__(self, to_validate):
        self.to_validate = to_validate

    def password(self):
        regex = "^(?=.*[A-Za-z])(?=.*0-9)(?=.*[@$!%*#?&])[A-Za-z0-9@$!%*#?&]{8,}$"
        if re.fullmatch(regex, self.to_validate):
            return True
        return False

    def name(self):
        regex = "/^[a-zA-ZàáâäãåąčćęèéėįìíîńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄĆČĖĘÈÉÊËÌÍÎÏŁŃÒÓÔÖØÚÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$/u"
        if re.fullmatch(regex, self.to_validate):
            return True
        return False

    def email(self):
        regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+.([A-Z|a-z]{2,})+"
        if re.fullmatch(regex, self.to_validate):
            return True
        return False


