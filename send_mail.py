import smtplib
from email.message import EmailMessage
from email.header import Header
from email.utils import formataddr
from jinja2 import Template
import mimetypes

def sendered_mails(EMAIL_ADDRESS, EMAIL_PASSWORD, HOST):
    def fabricy(title_month, path_to_zip, filename, list_addres):
        text_mail =  f'''
        <p>
            Планы работы на день </p>
        <p>  Методические планы и план-конспекты
            В {title_month} месяце
        </p>
        '''
        if not text_mail: 
            return

        msg = EmailMessage()
        msg['Subject'] = "План работ, План-конспекты"
        displayname = 'ПНК 3го караула'
        msg['From'] = Header(formataddr( (displayname, EMAIL_ADDRESS)), 'utf-8')
        msg['To'] = ', '.join( list_addres ) 
        
        msg.set_content( text_mail,subtype='html' )
        
        ctype, encoding = mimetypes.guess_type(path_to_zip)

        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path_to_zip, 'rb') as fp:
            msg.add_attachment(fp.read(),
                maintype=maintype,
                subtype=subtype,
                filename=filename)

        with smtplib.SMTP_SSL(HOST, 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
            smtp.send_message(msg)

    return fabricy



# if __name__ == '__main__':
#     main()
