import pytest
from app.services.email import SESEmailService
from app.schemas.email import EmailTemplate
from unittest.mock import patch

@pytest.mark.asyncio
async def test_send_password_reset_email():
    with patch('boto3.client') as mock_ses:
        # Setup mock response
        mock_ses.return_value.send_templated_email.return_value = {
            'MessageId': 'test-message-id'
        }
        
        email_service = SESEmailService()
        result = await email_service.send_password_reset(
            email="test@example.com",
            reset_token="test-token-123",
            username="testuser"
        )
        
        assert result is True
        # Verify SES was called with correct parameters
        mock_ses.return_value.send_templated_email.assert_called_once()

@pytest.mark.asyncio
async def test_send_email_with_template():
    with patch('boto3.client') as mock_ses:
        mock_ses.return_value.send_templated_email.return_value = {
            'MessageId': 'test-message-id'
        }
        
        email_service = SESEmailService()
        template = EmailTemplate(
            template_name="PasswordReset",  # AWS SES template name
            context={
                "username": "testuser",
                "reset_link": "http://example.com/reset?token=test-token-123"
            }
        )
        
        result = await email_service.send_email(
            to_email="test@example.com",
            subject="Password Reset",
            template=template
        )
        
        assert result 