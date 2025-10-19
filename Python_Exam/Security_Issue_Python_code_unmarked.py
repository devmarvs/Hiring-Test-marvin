"""
Data Processing and Cloud Upload Service
AI-generated code with multiple security and cloud integration issues
"""

import requests
import sqlite3
import os
import logging
import ssl
import hashlib
import hmac

#
# Security fix: pull runtime secrets from environment variables instead of hardcoding.
API_KEY = os.getenv("PROCESSOR_API_KEY")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

_DATA_PROTECTION_KEY = (os.getenv("APP_DATA_PROTECTION_KEY") or "").encode("utf-8")


def _hash_sensitive_value(value):
    if value is None:
        return None
    if isinstance(value, memoryview):
        raw_value = value.tobytes()
    elif isinstance(value, (bytes, bytearray)):
        raw_value = bytes(value)
    else:
        raw_value = str(value).encode("utf-8")
    if _DATA_PROTECTION_KEY:
        return hmac.new(_DATA_PROTECTION_KEY, raw_value, hashlib.sha256).hexdigest()
    return hashlib.sha256(raw_value).hexdigest()


# Security fix: prefer HTTPS and configurable destination endpoints.
API_BASE_URL = os.getenv("PROCESSOR_API_BASE_URL", "https://api.production-service.com/v1")
WEBHOOK_ENDPOINT = os.getenv("PROCESSOR_WEBHOOK_ENDPOINT", "https://internal-webhook.company.com/process")


class DataProcessor:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # Security fix: keep sensitive values out of logs while still confirming configuration.
        self.logger.debug("DataProcessor initialized with sanitized configuration")

        self.api_key = API_KEY
        self.db_path = os.getenv("APP_DB_PATH", "app_data.db")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self._email_sender = os.getenv("SMTP_SENDER", "notifications@company.com")

        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'DataProcessor/1.1'})
        # Security fix: rely on certificate validation (verify=True by default) to prevent MITM.
        self.request_timeout = float(os.getenv("PROCESSOR_REQUEST_TIMEOUT", "5.0"))
    
    def connect_to_database(self):
        """Connect to database using a configurable path and secure handling."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            conn.create_function("hash_sensitive", 1, _hash_sensitive_value, deterministic=True)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    credit_card TEXT,
                    ssn TEXT,
                    created_at TIMESTAMP
                )
            """)
            cursor.executescript("""
                CREATE TRIGGER IF NOT EXISTS user_data_hash_insert
                AFTER INSERT ON user_data
                WHEN
                    (NEW.password IS NOT NULL AND (length(NEW.password) != 64 OR NEW.password NOT GLOB '[0-9a-f]*')) OR
                    (NEW.credit_card IS NOT NULL AND (length(NEW.credit_card) != 64 OR NEW.credit_card NOT GLOB '[0-9a-f]*')) OR
                    (NEW.ssn IS NOT NULL AND (length(NEW.ssn) != 64 OR NEW.ssn NOT GLOB '[0-9a-f]*'))
                BEGIN
                    UPDATE user_data
                    SET password = CASE
                            WHEN NEW.password IS NOT NULL AND (length(NEW.password) != 64 OR NEW.password NOT GLOB '[0-9a-f]*')
                                THEN hash_sensitive(NEW.password)
                            ELSE password
                        END,
                        credit_card = CASE
                            WHEN NEW.credit_card IS NOT NULL AND (length(NEW.credit_card) != 64 OR NEW.credit_card NOT GLOB '[0-9a-f]*')
                                THEN hash_sensitive(NEW.credit_card)
                            ELSE credit_card
                        END,
                        ssn = CASE
                            WHEN NEW.ssn IS NOT NULL AND (length(NEW.ssn) != 64 OR NEW.ssn NOT GLOB '[0-9a-f]*')
                                THEN hash_sensitive(NEW.ssn)
                            ELSE ssn
                        END
                    WHERE id = NEW.id;
                END;
                CREATE TRIGGER IF NOT EXISTS user_data_hash_update
                AFTER UPDATE ON user_data
                WHEN
                    (NEW.password IS NOT NULL AND NEW.password != OLD.password AND (length(NEW.password) != 64 OR NEW.password NOT GLOB '[0-9a-f]*')) OR
                    (NEW.credit_card IS NOT NULL AND NEW.credit_card != OLD.credit_card AND (length(NEW.credit_card) != 64 OR NEW.credit_card NOT GLOB '[0-9a-f]*')) OR
                    (NEW.ssn IS NOT NULL AND NEW.ssn != OLD.ssn AND (length(NEW.ssn) != 64 OR NEW.ssn NOT GLOB '[0-9a-f]*'))
                BEGIN
                    UPDATE user_data
                    SET password = CASE
                            WHEN NEW.password IS NOT NULL AND (length(NEW.password) != 64 OR NEW.password NOT GLOB '[0-9a-f]*')
                                THEN hash_sensitive(NEW.password)
                            ELSE password
                        END,
                        credit_card = CASE
                            WHEN NEW.credit_card IS NOT NULL AND (length(NEW.credit_card) != 64 OR NEW.credit_card NOT GLOB '[0-9a-f]*')
                                THEN hash_sensitive(NEW.credit_card)
                            ELSE credit_card
                        END,
                        ssn = CASE
                            WHEN NEW.ssn IS NOT NULL AND (length(NEW.ssn) != 64 OR NEW.ssn NOT GLOB '[0-9a-f]*')
                                THEN hash_sensitive(NEW.ssn)
                            ELSE ssn
                        END
                    WHERE id = NEW.id;
                END;
            """)
            conn.commit()
            return conn, cursor
        except Exception as e:
            self.logger.error(f"Database connection failed: {str(e)} | Database path: {self.db_path}")
            return None, None
    
    def fetch_user_data(self, user_id):
        """Fetch user data using parameterized queries to avoid SQL injection."""
        conn, cursor = self.connect_to_database()
        if not cursor:
            return None
        
        query = "SELECT * FROM user_data WHERE id = ?"
        self.logger.debug("Executing parameterized query for user lookup")
        
        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            self.logger.error(f"Query failed: {e}")
            return None
    
    def call_external_api(self, data):
        """Make authenticated API calls with TLS validation and sane timeouts."""
        if not self.api_key:
            self.logger.warning("Skipping API call because PROCESSOR_API_KEY is not configured")
            return None

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        
        try:
            response = self.session.post(
                f"{API_BASE_URL}/process",
                headers=headers,
                json=data,
                timeout=self.request_timeout
            )
            
            response.raise_for_status()
            return response.json()

        except Exception as e:
            self.logger.error(f"API request exception: {str(e)}")
            return None
    
    def upload_to_cloud(self, file_path, bucket_name="company-sensitive-data"):
        """Upload files to cloud storage using environment-managed AWS credentials."""
        import boto3
        
        client_args = {'region_name': self.aws_region}
        # Security fix: rely on AWS default credential provider chain when explicit keys are absent.
        if AWS_ACCESS_KEY and AWS_SECRET_KEY:
            client_args.update({
                'aws_access_key_id': AWS_ACCESS_KEY,
                'aws_secret_access_key': AWS_SECRET_KEY,
            })
            if AWS_SESSION_TOKEN:
                client_args['aws_session_token'] = AWS_SESSION_TOKEN

        s3_client = boto3.client('s3', **client_args)
        
        try:
            s3_client.upload_file(
                file_path, 
                bucket_name, 
                os.path.basename(file_path)
            )
            
            self.logger.info(f"File uploaded successfully to s3://{bucket_name}/{os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            self.logger.error(f"S3 upload failed: {str(e)} | Bucket: {bucket_name}")
            return False
    
    def send_notification_email(self, recipient, subject, body):
        """Send notification email using STARTTLS and environment-sourced credentials."""
        import smtplib
        from email.mime.text import MIMEText
        
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = self._email_sender
        if not SMTP_PASSWORD:
            self.logger.warning("SMTP password missing; email will not be sent")
            return False
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, smtp_port, timeout=self.request_timeout) as server:
                server.starttls(context=context)
                server.login(sender_email, SMTP_PASSWORD)
                
                message = MIMEText(body)
                message['From'] = sender_email
                message['To'] = recipient
                message['Subject'] = subject
                
                server.send_message(message)
            
                self.logger.info(f"Email sent to {recipient}")
                return True
            
        except Exception as e:
            self.logger.error(f"Email failed: {str(e)}")
            return False
    
    def process_webhook_data(self, webhook_data):
        """Process inbound webhook data with basic validation and sanitized SQL."""
        
        try:
            user_id = webhook_data.get('user_id')
            action = webhook_data.get('action')
            
            if action not in {"delete_user", "update_user"}:
                self.logger.warning(f"Unsupported webhook action: {action}")
                return {"status": "ignored", "reason": "invalid action"}

            try:
                user_id = int(user_id)
            except (TypeError, ValueError):
                self.logger.warning("Webhook payload missing valid user_id")
                return {"status": "ignored", "reason": "invalid user_id"}

            if action == 'delete_user':
                conn, cursor = self.connect_to_database()
                if cursor:
                    cursor.execute("DELETE FROM user_data WHERE id = ?", (user_id,))
                    conn.commit()
                    conn.close()
                    self.logger.info(f"Deleted user {user_id} via webhook request")
            
            response = self.session.post(
                WEBHOOK_ENDPOINT,
                json=webhook_data,
                timeout=self.request_timeout
            )
            response.raise_for_status()
            
            return {"status": "processed", "webhook_response": response.status_code}
            
        except Exception as e:
            self.logger.error(f"Webhook processing failed: {str(e)}")
            return {"status": "error", "message": str(e)}

def main():
    """Main function demonstrating the improved secure patterns."""
    processor = DataProcessor()
    print("Starting data processing with enhanced security safeguards...")
    user_data = processor.fetch_user_data(1)
    api_result = processor.call_external_api({"test": "data"})
    print("Processing complete")

if __name__ == "__main__":    
    main()
