import boto3
import json
from botocore.exceptions import ClientError
from app.core.config import Settings
from app.schemas.email import EmailTemplate
import logging
from typing import Dict

logger = logging.getLogger(__name__)
settings = Settings()

class SESEmailService:
    def __init__(self):
        self.ses_client = boto3.client(
            'ses',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.source_email = settings.SES_SOURCE_EMAIL

    async def send_password_reset(
        self,
        email: str,
        reset_token: str,
        username: str
    ) -> bool:
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        template = EmailTemplate(
            template_name="PasswordReset",
            context={
                "username": username,
                "reset_link": reset_link
            }
        )
        
        return await self.send_email(
            to_email=email,
            subject="Password Reset Request",
            template=template
        )

    async def send_email(
        self,
        to_email: str,
        subject: str,
        template: EmailTemplate
    ) -> bool:
        try:
            response = self.ses_client.send_templated_email(
                Source=self.source_email,
                Destination={
                    'ToAddresses': [to_email]
                },
                Template=template.template_name,
                TemplateData=json.dumps(template.context)
            )
            
            logger.info(f"Email sent successfully to {to_email}. MessageId: {response['MessageId']}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False 