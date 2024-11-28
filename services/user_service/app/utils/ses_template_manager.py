import boto3
import json
from pathlib import Path
from app.core.config import Settings

settings = Settings()

class SESTemplateManager:
    def __init__(self):
        self.ses_client = boto3.client(
            'ses',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.templates_path = Path(__file__).parent.parent / "templates" / "ses"

    def create_or_update_template(self, template_name: str):
        template_file = self.templates_path / f"{template_name}.json"
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_file}")

        with open(template_file) as f:
            template_data = json.load(f)

        try:
            # Try to delete existing template
            self.ses_client.delete_template(TemplateName=template_name)
        except self.ses_client.exceptions.TemplateDoesNotExist:
            pass

        # Create new template
        self.ses_client.create_template(Template=template_data['Template'])
        print(f"Successfully created/updated template: {template_name}")

    def delete_template(self, template_name: str):
        try:
            self.ses_client.delete_template(TemplateName=template_name)
            print(f"Successfully deleted template: {template_name}")
        except self.ses_client.exceptions.TemplateDoesNotExist:
            print(f"Template does not exist: {template_name}") 