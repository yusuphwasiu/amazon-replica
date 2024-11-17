class MockSESEmailService:
    async def send_password_reset(
        self,
        email: str,
        reset_token: str,
        username: str
    ) -> bool:
        # Simulate successful email sending
        return True

    async def send_email(
        self,
        to_email: str,
        subject: str,
        template: dict
    ) -> bool:
        # Simulate successful email sending
        return True 