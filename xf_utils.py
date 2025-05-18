class Checker:

    def __init__(self):
        self.alphabets_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alphabets_lower = "abcdefghijklmnopqrstuvwxyz"
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.special_characters = '<>,.?;:"[]{}+=_-)`~!@#$%^&*('

    def check_full_name(self, full_name):
        errors_in_full_name = []
        number_in_name = False
        special_characters_in_full_name = False
        for character in self.special_characters:
            if character in full_name:
                special_characters_in_full_name = True
        for number in self.numbers:
            if str(number) in full_name:
                number_in_name = True
        if len(full_name) == 0:
            errors_in_full_name.append("Full name can't be empty")
        if len(full_name) > 25:
            errors_in_full_name.append('Full name too long')
        if len(full_name) < 7:
            errors_in_full_name.append('Full name too short')
        if number_in_name:
            errors_in_full_name.append('Numbers not allowed in full name')
        if special_characters_in_full_name:
            errors_in_full_name.append('Special characters not allowed in full mame')
        return errors_in_full_name

    @staticmethod
    def check_email(email):
        errors_in_email = []
        if len(email) == 0:
            errors_in_email.append("Email can't be empty")
        if len(email) < 5:
            errors_in_email.append('Email too short')
        if len(email) > 35:
            errors_in_email.append('Email too long')
        if '@' not in email or "." not in email:
            errors_in_email.append('Invalid email, please double check')

        return errors_in_email

    @staticmethod
    def check_password(password):
        errors_in_password = []
        special_symbols = ['$', '@', '#', '%', '/', '?', '!', '~', '^', '&', '*', '(', ')', '_', '-', '+', '=', '[',
                           ']']
        val = True

        if len(password) == 0:
            errors_in_password.append("Password can't be empty")
            val = False

        if len(password) < 8:
            errors_in_password.append('Password too short')
            val = False

        if len(password) > 20:
            errors_in_password.append('Password too long')
            val = False

        if not any(char.isdigit() for char in password):
            errors_in_password.append('Password too simple, include numbers')
            val = False

        if not any(char.isupper() for char in password):
            errors_in_password.append('Password too simple, include uppercase letter')
            val = False

        if not any(char.islower() for char in password):
            errors_in_password.append('Password too simple, include lowercase letter')
            val = False

        if not any(char in special_symbols for char in password):
            errors_in_password.append('Password too simple, include special characters')
            val = False
        if val:
            return errors_in_password

        return errors_in_password

    def check_phone_no(self, phone_no):
        errors_in_phone_no = []
        special_character_in_phone_number = False
        alphabet_lower_in_phone_number = False
        alphabet_upper_in_phone_number = False

        for alphabet in self.alphabets_upper:
            if alphabet in phone_no:
                alphabet_upper_in_phone_number = True
        for alphabet in self.alphabets_lower:
            if alphabet in phone_no:
                alphabet_lower_in_phone_number = True
        for special_char in self.special_characters:
            if special_char in phone_no:
                special_character_in_phone_number = True

        if alphabet_lower_in_phone_number or alphabet_upper_in_phone_number:
            errors_in_phone_no.append('Alphabets not allowed')
        if special_character_in_phone_number:
            errors_in_phone_no.append('Special characters not allowed')
        if len(phone_no) == 0:
            errors_in_phone_no.append("Phone number can't be empty")
        if len(phone_no) < 10:
            errors_in_phone_no.append('Phone number too short')
        if len(phone_no) > 10:
            errors_in_phone_no.append('Phone number too long')

        return errors_in_phone_no

    def check_date_of_birth(self, date_of_birth):
        errors_in_date_of_birth = []
        alphabet_upper_in_date_of_birth = False
        alphabet_lower_in_date_of_birth = False
        special_character_in_date_of_birth = False

        for alphabet in self.alphabets_upper:
            if alphabet in date_of_birth:
                alphabet_upper_in_date_of_birth = True
        for alphabet in self.alphabets_lower:
            if alphabet in date_of_birth:
                alphabet_lower_in_date_of_birth = True
        for special_char in self.special_characters:
            if special_char in date_of_birth:
                special_character_in_date_of_birth = True

        if special_character_in_date_of_birth:
            errors_in_date_of_birth.append('Special characters not allowed')
        if alphabet_lower_in_date_of_birth or alphabet_upper_in_date_of_birth:
            errors_in_date_of_birth.append('Alphabets not allowed')

        if len(date_of_birth) == 0:
            errors_in_date_of_birth.append("Date of birth can't be empty")
        if len(date_of_birth) > 10 or len(date_of_birth) < 10:
            errors_in_date_of_birth.append("Date of birth is invalid")

        return errors_in_date_of_birth

    def check_nin_no(self, nin_no):
        errors_in_nin_no = []
        special_character_in_nin_no = False
        for char in self.special_characters:
            if char in nin_no:
                special_character_in_nin_no = True
        if special_character_in_nin_no:
            errors_in_nin_no.append('Special characters not allowed')
        if len(nin_no) == 0:
            errors_in_nin_no.append("NIN number can't be empty")
        if len(nin_no) > 14:
            errors_in_nin_no.append('NIN number long short')
        if len(nin_no) < 14:
            errors_in_nin_no.append('NIN number too short')
        if nin_no[0:2] == 'CM' or nin_no[0:2] == 'CF':
            pass
        else:
            errors_in_nin_no.append('NIN number is invalid')

        return errors_in_nin_no


if __name__ == '__main__':
    Checker().check_password('')
