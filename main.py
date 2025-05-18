import hashlib
import os
import platform
import psutil
import re
import socket
import uuid
import webbrowser
from os.path import basename

from cryptocode import decrypt as aes_256_decrypt
from cryptocode import encrypt as aes_256_encrypt
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.core.window import Window

import xf_utils as xu

Window.size = 650, 500
checker = xu.Checker()


class LoginScreen(Screen):

    def goto_loan_application_scr(self):

        passwd_is_correct = False
        user_name_is_correct = False

        with open('C:/Users/iceman/PycharmProjects/XFinanceApp/.xf-data/stored_passwd_hash', 'r') as passwd_hash_file:
            stored_passwd_hash = passwd_hash_file.read()
            if hashlib.sha256(bytes(self.ids.login_passwd.text, 'utf-8')).hexdigest() == stored_passwd_hash:
                passwd_is_correct = True

        with open('C:/Users/iceman/PycharmProjects/XFinanceApp/.xf-data/stored_user_name_hash', 'r') as user_name_hash_file:
            stored_user_name_hash = user_name_hash_file.read()
            if hashlib.sha256(bytes(self.ids.user_name.text, 'utf-8')).hexdigest() == stored_user_name_hash:
                user_name_is_correct = True

        if not passwd_is_correct:
            self.ids.error_info_login_passwd.text = 'Password is incorrect'
        if passwd_is_correct:
            self.ids.error_info_login_passwd.text = ''
        if len(self.ids.login_passwd.text) == 0:
            self.ids.error_info_login_passwd.text = "Password can't be empty"

        if not user_name_is_correct:
            self.ids.error_info_user_name.text = 'Username is incorrect'
        if user_name_is_correct:
            self.ids.error_info_user_name.text = ''
        if len(self.ids.user_name.text) == 0:
            self.ids.error_info_user_name.text = "Username can't be empty"

        if passwd_is_correct and user_name_is_correct:
            self.manager.current = 'loan_application_scr'


class RegisterScreen(Screen):

    def goto_terms_of_service_scr(self):
        self.manager.current = 'terms_of_service_scr'

    def on_leave(self, *args):
        pass

    def register_user(self):

        full_name = self.ids.full_name.text
        email = self.ids.email.text
        phone_no = self.ids.phone_no.text
        nin_no = self.ids.nin_no.text
        date_of_birth = self.ids.date_of_birth.text
        passwd = self.ids.passwd.text

        # check if full name is correct
        if checker.check_full_name(full_name) != []:
            self.ids.error_info_full_name.text = checker.check_full_name(full_name)[0]
        elif checker.check_full_name(full_name) == []:
            self.ids.error_info_full_name.text = ''

        # check if password is correct
        if checker.check_password(passwd) != []:
            self.ids.error_info_create_passwd.text = checker.check_password(passwd)[0]
        elif checker.check_password(passwd) == []:
            self.ids.error_info_create_passwd.text = ''

        # check if email is correct
        if checker.check_email(email) != []:
            self.ids.error_info_email.text = checker.check_email(email)[0]
        elif checker.check_email(email) == []:
            self.ids.error_info_email.text = ''

        # check if phone number is correct
        if checker.check_phone_no(phone_no) != []:
            self.ids.error_info_phone_no.text = checker.check_phone_no(phone_no)[0]
        elif checker.check_phone_no(phone_no) == []:
            self.ids.error_info_phone_no.text = ''

        # check if date of birth is correct
        if checker.check_date_of_birth(date_of_birth) != []:
            self.ids.error_info_date_of_birth.text = checker.check_date_of_birth(date_of_birth)[0]
        elif checker.check_date_of_birth(date_of_birth) == []:
            self.ids.error_info_date_of_birth.text = ''

        # check if NIN is correct
        if checker.check_nin_no(nin_no) != []:
            self.ids.error_info_nin_no.text = checker.check_nin_no(nin_no)[0]
        elif checker.check_nin_no(nin_no) == []:
            self.ids.error_info_nin_no.text = ''

        # check if current residence is correct
        if self.ids.current_residence.text == '':
            self.ids.error_info_current_residence.text = 'This field is required'
        if self.ids.current_residence.text != '':
            self.ids.error_info_current_residence.text = ''

        # check if current occupation is correct
        if self.ids.current_occupation.text == '':
            self.ids.error_info_current_occupation.text = 'This field is required'
        if self.ids.current_occupation.text != '':
            self.ids.error_info_current_occupation.text = ''

        full_name = self.ids.full_name.text
        email = self.ids.email.text
        phone_no = self.ids.phone_no.text
        nin_no = self.ids.nin_no.text
        current_occupation = self.ids.current_occupation.text
        current_residence = self.ids.current_residence.text
        date_of_birth = self.ids.date_of_birth.text
        passwd = self.ids.passwd.text

        user_name = '@' + full_name.lower().replace(' ', '') + date_of_birth[0:2]

        # if all are correct: encrypt info: save inf: goto to next screen
        if (
                checker.check_password(passwd) == [] and
                checker.check_full_name(full_name) == [] and
                checker.check_email(email) == [] and
                checker.check_date_of_birth(date_of_birth) == [] and
                checker.check_phone_no(phone_no) == [] and
                checker.check_nin_no(nin_no) == [] and
                self.ids.current_occupation.text != '' and
                self.ids.current_residence.text != ''
        ):
            passwd_hash = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
            user_name_hash = hashlib.sha256(user_name.encode('utf-8')).hexdigest()

            encrypted_passwd = aes_256_encrypt(phone_no, passwd)
            encrypted_full_name = aes_256_encrypt(full_name, passwd)
            encrypted_email = aes_256_encrypt(email, passwd)
            encrypted_nin_no = aes_256_encrypt(nin_no, passwd)
            encrypted_current_occupation = aes_256_encrypt(current_occupation, passwd)
            encrypted_current_residence = aes_256_encrypt(current_residence, passwd)
            encrypted_date_of_birth = aes_256_encrypt(date_of_birth, passwd)

            credentials_info = encrypted_full_name + '\n' + encrypted_passwd + '\n' + encrypted_email + '\n' + encrypted_nin_no + '\n' + encrypted_date_of_birth + '\n' + encrypted_current_residence + '\n' + encrypted_current_occupation

            try:
                os.mkdir('.xf-data')
            except FileExistsError:
                pass

            try:
                os.chdir('.xf-data')
                with open('C:/Users/iceman/PycharmProjects/XFinanceApp/.xf-data/stored_passwd_hash', 'w') as pw_hash_file:
                    pw_hash_file.write(passwd_hash)
                with open('C:/Users/iceman/PycharmProjects/XFinanceApp/.xf-data/stored_user_name_hash', 'w') as user_name_hash_file:
                    user_name_hash_file.write(user_name_hash)
                with open('C:/Users/iceman/PycharmProjects/XFinanceApp/.xf-data/credentials', 'w') as credentials_file:
                    credentials_file.write(credentials_info)
            except FileExistsError:
                pass

            # send code to the user
            import utils
            utils.send_code(email_addr=email)

            # go to confirmation screen
            self.manager.current = 'confirmation_scr'


class TermsOfServiceScreen(Screen):

    def on_enter(self, *args):
        with open('C:/Users/iceman/PycharmProjects/XFinanceApp/terms-of-service.txt', 'r') as terms_of_service_file:
            terms_of_service_text = terms_of_service_file.read()
            self.ids.terms_of_service.text = terms_of_service_text

    @staticmethod
    def open_mail_client():
        webbrowser.open('mailto:')

    def goto_register_scr(self):
        self.manager.current = 'register_scr'


class ConfirmationScreen(Screen):

    def on_enter(self, *args):
        self.ids.user_name.text = self.ids.user_name.text + '@' + self.manager.get_screen(
            "register_scr").ids.full_name.text.lower().replace(' ', '') + self.manager.get_screen(
            "register_scr").ids.date_of_birth.text[0:2]
        self.ids.passwd.text = self.ids.passwd.text + self.manager.get_screen("register_scr").ids.passwd.text

    def goto_profile_scr(self):
        if os.getcwd() != '/home/iceman/Desktop/xfinance/.xf-data':
            os.chdir('/home/iceman/Desktop/xfinance/.xf-data')

        with open(basename('stored_confirmation_code_hash'), 'r') as confirmation_code_hash_file:
            stored_confirmation_code_hash = confirmation_code_hash_file.read()

        entered_confirmation_code_hash = hashlib.sha256(bytes(self.ids.confirmation_code.text, 'utf-8')).hexdigest()
        hash_of_empty_str = hashlib.sha256(bytes('', 'utf-8')).hexdigest()

        if entered_confirmation_code_hash == hash_of_empty_str:
            self.ids.error_info_confirmation_code.text = "Confirmation code can't be empty"
        elif entered_confirmation_code_hash == stored_confirmation_code_hash:
            self.manager.current = 'loan_application_scr'
        else:
            self.ids.error_info_confirmation_code.text = 'Code is not correct, Double check it and retry'


class FilePickerScreen1(Screen):

    def selected(self, file_name):
        if len(file_name) != 0:
            self.manager.get_screen('loan_application_scr').ids.national_id.source = file_name[0]

    def done_selection(self):
        self.manager.current = 'loan_application_scr'


class FilePickerScreen2(Screen):

    def selected(self, file_name):
        if len(file_name) != 0:
            self.manager.get_screen('loan_application_scr').ids.other_id_image.source = file_name[0]

    def done_selection(self):
        self.manager.current = 'loan_application_scr'


class FilePickerScreen3(Screen):

    def selected(self, file_name):
        if len(file_name) != 0:
            self.manager.get_screen('loan_application_scr').ids.selfie_image.source = file_name[0]

    def done_selection(self):
        self.manager.current = 'loan_application_scr'


class FilePickerScreen4(Screen):

    def selected(self, file_name):
        if len(file_name) != 0:
            self.manager.get_screen('loan_application_scr').ids.security_image.source = file_name[0]

    def done_selection(self):
        self.manager.current = 'loan_application_scr'


class LoanApplicationScreen(Screen):

    def on_enter(self, *args):

        info = []
        with open('C:/Users/iceman/PycharmProjects/XFinanceApp/.xf-data/credentials', 'r') as credentials_file:
            credentials_info = credentials_file.readlines()
            for item in credentials_info:
                info.append(aes_256_decrypt(item, '@Jethro248'))
        self.ids.full_name.text = info[0]
        self.ids.phone_no.text = info[1]
        self.ids.email.text = info[2]
        self.ids.nin_no.text = info[3]
        self.ids.date_of_birth.text = info[4]
        self.ids.current_residence.text = info[5]
        self.ids.current_occupation.text = info[6]

    def goto_file_picker_scr(self):
        self.manager.current = 'file_picker_scr'

    def send_application(self):

        if (self.ids.national_id.source or self.ids.other_id_image.source or self.ids.selfie_image.source or
            self.ids.security_image.source) == '':
            self.ids.error_info_image.text = 'All Images are Required!'

        if (len(self.ids.loan_term.text) or len(self.ids.loan_amount.text) or len(self.ids.source_of_income.text) or
            len(self.ids.trustee_contact.text) or len(self.ids.security.text)) == 0:
            self.ids.error_info_details.text = 'All Fields are Required!'
        else:
            national_id_path = self.ids.national_id.source
            other_id_image_path = self.ids.other_id_image.source
            selfie_image_path = self.ids.selfie_image.source
            security_image_path = self.ids.security_image.source

            filename_paths = [national_id_path, other_id_image_path, selfie_image_path, security_image_path]

            if os.getcwd() != '/home/iceman/PycharmProjects/XFinanceApp/.xf-data':
                os.chdir('/home/iceman/PycharmProjects/XFinanceApp/.xf-data')
            else:
                info = []
                with open('C:/Users/iceman/PycharmProjects/XFinanceApp/.xf-data/credentials', 'r') as credentials_file:
                    credentials_info = credentials_file.readlines()
                    for item in credentials_info:
                        info.append(aes_256_decrypt(item, '@Jethro248'))
                self.ids.full_name.text = info[0]
                self.ids.phone_no.text = info[1]
                self.ids.email.text = info[2]
                self.ids.nin_no.text = info[3]
                self.ids.date_of_birth.text = info[4]
                self.ids.current_residence.text = info[5]
                self.ids.current_occupation.text = info[6]

                sender_email = 'finance.aixpro@gmail.com'
                user_id = 'finance.aixpro'
                receivers_email = [self.ids.email.text]
                email_subject = 'Loan Application'
                email_body = f'''
    BIODATA
    Full name: {self.ids.full_name.text}
    Phone number: {self.ids.phone_no.text}
    Email: {self.ids.email.text}
    NIN number: {self.ids.nin_no.text}
    Date of birth: {self.ids.date_of_birth.text}
    Current residence: {self.ids.current_residence.text}
    Current occupation: {self.ids.current_occupation.text}
                
    LOAN DETAILS
    Loan_amount: {self.ids.loan_amount.text}
    Loan_term: {self.ids.loan_term.text}
    Security: {self.ids.security.text}
    Trustee_contact: {self.ids.trustee_contact.text}
    Source_of_income: {self.ids.source_of_income.text}
                
    DEVICE INFO
    Platform: {platform.system()}
    Platform release: {platform.release()}
    Platform-version: {platform.version()}
    Architecture: {platform.machine()}
    Hostname: {socket.gethostname()}
    IP-address: {socket.gethostbyname(socket.gethostname())}
    MAC-address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
    Processor: {platform.processor()}
    RAM: {str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"}
    '''

                import email_sender
                email_sender.send_email(
                    password='scco mazj fwln uxyd',
                    files_path=filename_paths,
                    body=email_body,
                    subject=email_subject,
                    recipients_addr=receivers_email,
                    from_addr=sender_email,
                    user=user_id
                )

                self.manager.current = 'loan_confirmation_scr'


class LoanConfirmationScreen(Screen):
    pass


class XFinanceApp(App):

    def on_start(self):
        if not os.path.exists(basename('attachment')):
            os.mkdir(basename('/home/iceman/PycharmProjects/XFinanceApp/attachment'))
        else:
            pass

    def build(self):

        self.icon = basename('/home/iceman/PycharmProjects/AIXLoanApp/res/aix_icon.jpeg')

        login_scr = LoginScreen(name='login_scr')
        register_scr = RegisterScreen(name='register_scr')
        confirmation_scr = ConfirmationScreen(name='confirmation_scr')
        loan_application_scr = LoanApplicationScreen(name='loan_application_scr')
        loan_confirmation_scr = LoanConfirmationScreen(name='loan_confirmation_scr')
        terms_of_service_scr = TermsOfServiceScreen(name='terms_of_service_scr')

        file_picker_scr_1 = FilePickerScreen1(name='file_picker_scr_1')
        file_picker_scr_2 = FilePickerScreen2(name='file_picker_scr_2')
        file_picker_scr_3 = FilePickerScreen3(name='file_picker_scr_3')
        file_picker_scr_4 = FilePickerScreen4(name='file_picker_scr_4')

        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(login_scr)
        sm.add_widget(register_scr)
        sm.add_widget(confirmation_scr)
        sm.add_widget(loan_application_scr)
        sm.add_widget(loan_confirmation_scr)
        sm.add_widget(terms_of_service_scr)

        sm.add_widget(file_picker_scr_1)
        sm.add_widget(file_picker_scr_2)
        sm.add_widget(file_picker_scr_3)
        sm.add_widget(file_picker_scr_4)

        if os.path.exists('.xf-data'):
            sm.current = 'login_scr'
        elif not os.path.exists('.xf-data'):
            sm.current = 'register_scr'
        sm.current = 'loan_application_scr'
        return sm


if __name__ == '__main__':
    XFinanceApp().run()
