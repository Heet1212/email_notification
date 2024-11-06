import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader


class EmailSender:
    def __init__(self, mail_config):
        self.mail_config = mail_config
        self.env = Environment(loader=FileSystemLoader('templates'))

    def render_template(self, template_name):
        # Load and render the template with placeholders
        template = self.env.get_template(template_name)
        rendered_content = template.render(self.mail_config["templatePlaceHolder"])
        return rendered_content

    def send_email(self):
        subject = self.mail_config["mail_subject"]
        recipient_list = self.mail_config["mail_to"]
        template_name = "success_template.html" if "Success" in subject else "failure_template.html"
        html_content = self.render_template(template_name)

        # Construct the email
        msg = MIMEMultipart()
        msg["From"] = self.mail_config["mail_from"]
        msg["To"] = ", ".join(recipient_list)
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        # Use SMTP server details if provided, otherwise attempt to use local SMTP server
        if self.mail_config["send_method"] == "SMTP":
            smtp_params = self.mail_config["smtp_params"]
            smtp_server = smtp_params["mail_host"]
            smtp_port = smtp_params["port"]
            username = smtp_params["username"]
            password = smtp_params["password"]

            try:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:

                    server.login(username, password)
                    server.sendmail(msg["From"], recipient_list, msg.as_string())
                print("Email sent successfully using external SMTP.")
            except Exception as e:
                print(f"Failed to send email using SMTP. Error: {e}")
        else:
            print("Only SMTP method is supported on Windows.")


# Example usage
if __name__ == "__main__":
    # Example mail_config dictionary
    mail_config = {
        "mail_from": "vishwashah1104@gmail.com",
        "mail_to": ["heetshah381997@gmail.com"],
        "smtp_params": {
            "mail_host": "smtp.gmail.com",
            "port": 465,
            "username": "vishwashah1104@gmail.com",
            "password": "vypuwcsdtxxpwsgx"  # Replace with an app-specific password if using Gmail
        },
        "mail_subject": "Job Notification",
        "send_method": "SMTP",  # Only SMTP method is recommended on Windows
        "templatePlaceHolder": {
            "name": "Vijay",
            "jobid": "sfwxcvsfw",
            "job_started_on": "2024-10-11 12:34:22",
            "row_count": 34,
            "df_placeholder": {
                "table1_df": "table1 content",
                "failure_df": "failure content",
                "table_df": "sample table content"
            }
        }
    }

    email_sender = EmailSender(mail_config)
    email_sender.send_email()
