import imaplib
import email
import os

# Function to download attachments from emails
def download_attachments(username, password, folder='INBOX', attachment_dir='attachments'):
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select(folder)

    # Search for emails with attachments
    result, data = mail.search(None, 'ALL')
    ids = data[0].split()

    # Loop through each email ID
    for email_id in ids:
        # Fetch the email
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Loop through each part of the email
        for part in msg.walk():
            # Check if part is an attachment
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            # Extract attachment filename
            filename = part.get_filename()
            if filename:
                # Save attachment to the attachment directory
                if not os.path.exists(attachment_dir):
                    os.makedirs(attachment_dir)
                filepath = os.path.join(attachment_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))

    # Close the connection
    mail.close()
    mail.logout()

# Example usage
if __name__ == "__main__":
    # Replace 'your_email@gmail.com' and 'your_password' with your Gmail credentials
    download_attachments('example@gmail.com', 'password')
