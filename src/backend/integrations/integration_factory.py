from . import Integration, DiscordIntegration, SlackIntegration, TelegramIntegration, WhatsAppIntegration, WebhookIntegration


# DESIGN PATTERN: Simple Factory
class _IntegrationFactory:
    def __init__(self):
        self._creators = {
            "discord": DiscordIntegration,
            "slack": SlackIntegration,
            "telegram": TelegramIntegration,
            "whatsapp": WhatsAppIntegration,
            "webhook": WebhookIntegration,
        }

    def create_integration(self, type: str) -> Integration:
        creator = self._creators.get(type.lower())
        if not creator:
            raise ValueError(f"The provided feature type is not supported: {type}")
        return creator()

    def get_supported_integrations(self) -> list[str]:
        return list(self._creators.keys())


# Singleton instance of the factory
IntegrationFactory = _IntegrationFactory()
