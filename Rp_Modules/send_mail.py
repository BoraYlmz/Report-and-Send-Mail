import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from io import BytesIO
from plyer import notification
import os
from dotenv import load_dotenv

class Send_Mail:
    def __init__(self,Mail_Header:str,to_mail:str,to_name:str,excel_file):
        load_dotenv(dotenv_path='Parts/private_data.env')
        self.Mail_Header = Mail_Header
        self.server = smtplib.SMTP('smtp.office365.com',587)  # SMTP sunucu adresiniz
        self.sender_email = os.getenv('SMTP_MAİL')
        self.password = os.getenv('SMTP_PASS')
        self.receiver_email = to_mail
        self.receiver_name = to_name
        self.excel_file = excel_file
        self.send()

    def send(self):
        message = MIMEMultipart()
        message['Subject'] = Header(self.Mail_Header, "UTF-8")
        message['From'] = self.sender_email
        message['To'] = self.receiver_email

        html_body = f"""
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <center>
            <div style="border:1px solid gray; height:800px;width: 700px;background-color: #ffffff;">
                <div style="height:150px;width: 100%; border:1px solid gray;">
                    <img src="cid:oslogo" style ="height:150px; width:auto;" >
                </div>
                <div style="height:500px;width: 100%; border:1px solid gray;">
                    <p style="text-align: left; padding-left:50px; margin:0px; padding-top:50px;">Sayın <b>{self.receiver_name}</b>,</p>
                    <p style="text-align: left; padding-left:25px; margin:0px;">Kurumumuzdan talep etmiş olduğunuz otomatik {self.Mail_Header} Raporu ekte gönderilmiştir.</p>
                    <div style="height:100px;width: 350px; border:1px solid gray;margin-top: 20%;">
                        <img align="left" src="cid:excellogo" style ="height:90px; width:auto; padding-left:10px;padding-top:5px;" > <p style="padding-top:20px;font-size:18px;font-weight:bold;">Rapor.xlsx</p>
                    </div>
                </div>
                <div style="height:146px;width: 100%; border:1px solid gray;">
                    <p style="padding-left:25px;text-align:left;text-indent:50px;">Eğer rapor talebi size ait değil veya otomatik rapor gönderimini durdurmak isterseniz Okulunuzla ilgilenen <b><span style="color:#a60c26;">Okul İlişkileri Yöneticiniz</b></span> ile veya <b><span style="color:#a60c26;">bilgi@okulsepeti.com.tr</b></span> adresinden bildirebilirsiniz.
                </div>
            </div>
            </center>
        </body>
        </html>
        """
        message.attach(MIMEText(html_body, 'html'))
        icon_path = os.path.join(os.getcwd(), r"Rp_Modules\icons", "mail_header_logo.png")
        with open(icon_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<oslogo>')
            img.add_header('Content-Disposition', 'inline')
            message.attach(img)
        excel_icon_path = os.path.join(os.getcwd(), r"Rp_Modules\icons", "excel_logo.png")
        with open(excel_icon_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<excellogo>')
            img.add_header('Content-Disposition', 'inline')
            message.attach(img)
        
        attachment = MIMEApplication(self.excel_file.read(), _subtype='xlsx')
        attachment.add_header('Content-Disposition', 'attachment', filename="Rapor.xlsx")
        message.attach(attachment)
        # with open(self.excel_file, 'rb') as file:
        #     part = MIMEApplication(file.read(), Name=self.excel_file)
        #     part['Content-Disposition'] = f'attachment; filename="{self.excel_file}"'
        #     message.attach(part)

        try:
            self.server.starttls()
            self.server.login(self.sender_email, self.password)
            self.server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            print('Email sent successfully!')
            notification.notify(
            title='Rapor Gönderim Bildirimi',
                message=f'{self.receiver_name} adlı kişiye {self.Mail_Header} konulu mail gönderildi',
                app_name='OS Oto Rapor Gönderimi',
            )
        except Exception as e:
            print(f'Error: {e}')
            notification.notify(
            title='Rapor Gönderim Bildirimi',
                message=f'{self.receiver_name} adlı kişiye {self.Mail_Header} konulu mail {e} hatasından dolayı gönderilemedi',
                app_name='OS Oto Rapor Gönderimi',
            )
        finally:
            self.server.quit()



