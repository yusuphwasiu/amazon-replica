import click
from app.utils.ses_template_manager import SESTemplateManager

@click.group()
def cli():
    pass

@cli.command()
@click.argument('template_name')
def create_template(template_name):
    """Create or update an SES template"""
    manager = SESTemplateManager()
    manager.create_or_update_template(template_name)

@cli.command()
@click.argument('template_name')
def delete_template(template_name):
    """Delete an SES template"""
    manager = SESTemplateManager()
    manager.delete_template(template_name)

if __name__ == '__main__':
    cli() 