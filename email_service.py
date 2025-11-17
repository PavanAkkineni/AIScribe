# Email Service for AIscribe - Send and Receive Emails

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime
from logger_config import setup_logger
from email_config import EMAIL_CONFIG

logger = setup_logger('EmailService')

class EmailService:
    """Service for sending and receiving emails via SMTP and IMAP"""
    
    def __init__(self):
        """Initialize email service with config"""
        self.smtp_server = EMAIL_CONFIG['smtp']['server']
        self.smtp_port = EMAIL_CONFIG['smtp']['port']
        self.imap_server = EMAIL_CONFIG['imap']['server']
        self.imap_port = EMAIL_CONFIG['imap']['port']
        self.username = EMAIL_CONFIG['smtp']['username']
        self.password = EMAIL_CONFIG['smtp']['password']
        self.from_email = EMAIL_CONFIG['from_email']
        self.from_name = EMAIL_CONFIG['from_name']
        
        logger.info(f"📧 EmailService initialized with {self.from_email}")
    
    def send_email(self, to_email, subject, body_html, patient_id):
        """
        Send an email via SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: Email body (HTML format)
            patient_id: Patient identifier
            
        Returns:
            dict with success status and message
        """
        try:
            logger.info(f"📤 Sending email to {to_email}")
            logger.info(f"   Subject: {subject}")
            
            # Create message
            message = MIMEMultipart('alternative')
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = to_email
            message['Subject'] = subject
            message['Reply-To'] = self.from_email
            
            # Add custom headers for tracking
            message['X-Patient-ID'] = patient_id
            message['X-AIscribe-Type'] = 'visit-summary'
            
            # Attach HTML body
            html_part = MIMEText(body_html, 'html')
            message.attach(html_part)
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(self.username, self.password)
                server.send_message(message)
            
            logger.info(f"✅ Email sent successfully to {to_email}")
            
            return {
                'success': True,
                'message': f'Email sent to {to_email}',
                'sent_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def fetch_inbox_emails(self, patient_email=None, limit=50):
        """
        Fetch emails from inbox via IMAP
        
        Args:
            patient_email: Filter emails from specific patient email address
            limit: Maximum number of emails to fetch
            
        Returns:
            list of email dictionaries
        """
        try:
            logger.info(f"📬 Fetching inbox emails{f' for {patient_email}' if patient_email else ''}...")
            
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.username, self.password)
            mail.select('inbox')
            
            # Search for emails
            if patient_email:
                # Search for emails from this patient email
                search_criteria = f'(FROM "{patient_email}")'
                logger.info(f"   Search criteria: {search_criteria}")
            else:
                search_criteria = 'ALL'
            
            status, messages = mail.search(None, search_criteria)
            email_ids = messages[0].split()
            
            logger.info(f"   Found {len(email_ids)} email(s) matching criteria")
            
            # Get the latest emails (up to limit)
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            email_ids = list(reversed(email_ids))  # Newest first
            
            emails = []
            
            for email_id in email_ids:
                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            
                            # Decode subject
                            subject = self._decode_header(msg['Subject'])
                            from_email = msg['From']
                            to_email = msg['To']
                            date_str = msg['Date']
                            message_id = msg['Message-ID']
                            in_reply_to = msg.get('In-Reply-To', '')
                            references = msg.get('References', '')
                            
                            # Try to extract patient ID from headers
                            email_patient_id = msg.get('X-Patient-ID', '')
                            
                            # Get email body
                            body = self._get_email_body(msg)
                            
                            # Parse date
                            try:
                                email_date = email.utils.parsedate_to_datetime(date_str)
                                timestamp = email_date.isoformat()
                            except:
                                timestamp = datetime.now().isoformat()
                            
                            emails.append({
                                'id': message_id,
                                'from': from_email,
                                'to': to_email,
                                'subject': subject,
                                'body': body,
                                'timestamp': timestamp,
                                'patient_id': email_patient_id or 'unknown',
                                'direction': 'inbound',
                                'in_reply_to': in_reply_to,
                                'references': references
                            })
                            
                except Exception as e:
                    logger.warning(f"Error processing email {email_id}: {str(e)}")
                    continue
            
            mail.close()
            mail.logout()
            
            logger.info(f"✅ Fetched {len(emails)} emails from inbox")
            
            return emails
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch emails: {str(e)}")
            logger.exception(e)
            return []
    
    def _decode_header(self, header_value):
        """Decode email header"""
        if header_value is None:
            return ''
        
        decoded_parts = decode_header(header_value)
        decoded_string = ''
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                try:
                    decoded_string += part.decode(encoding or 'utf-8')
                except:
                    decoded_string += part.decode('utf-8', errors='ignore')
            else:
                decoded_string += str(part)
        
        return decoded_string
    
    def _get_email_body(self, msg):
        """Extract email body from message"""
        body = ''
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                
                # Skip attachments
                if 'attachment' in content_disposition:
                    continue
                
                # Get plain text or HTML
                if content_type == 'text/plain':
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
                elif content_type == 'text/html' and not body:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = str(msg.get_payload())
        
        # Clean up quoted/forwarded text
        body = self._extract_reply_content(body)
        
        return body
    
    def _extract_reply_content(self, body):
        """Extract only the new reply content, removing quoted text"""
        if not body:
            return body
        
        lines = body.split('\n')
        reply_lines = []
        
        # Common patterns that indicate quoted/forwarded content
        quote_markers = [
            'On ',  # "On Fri, Nov 14, 2025 at 7:47 PM"
            '>', # Quoted lines starting with >
            '-----Original Message-----',
            'From:',
            'Sent:',
            'To:',
            'Subject:',
            '________________________________',
            '---',
            'wrote:',
            '<',  # Email addresses in headers
        ]
        
        in_reply = True
        
        for line in lines:
            stripped = line.strip()
            
            # Check if this line starts quoted content
            if any(stripped.startswith(marker) for marker in quote_markers):
                in_reply = False
                continue
            
            # Check for "wrote:" at end of line (common in Gmail)
            if 'wrote:' in stripped.lower():
                in_reply = False
                continue
            
            # Check if line contains email pattern (likely a header)
            if '@' in stripped and ('<' in stripped or 'gmail.com' in stripped or '.com>' in stripped):
                in_reply = False
                continue
            
            # If we're still in the reply section, keep the line
            if in_reply and stripped:
                reply_lines.append(line)
        
        # Join reply lines
        reply_text = '\n'.join(reply_lines).strip()
        
        # If we got nothing or very little, return original (might be a plain email)
        if len(reply_text) < 5 and len(body) > 50:
            # Try alternative: get everything before first quote marker
            for marker in ['On ', 'wrote:', '-----Original']:
                if marker in body:
                    reply_text = body.split(marker)[0].strip()
                    break
            
            if not reply_text or len(reply_text) < 5:
                reply_text = body  # Return original if extraction fails
        
        return reply_text if reply_text else body

