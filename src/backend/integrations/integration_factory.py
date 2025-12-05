from . import Integration, DiscordIntegration, SlackIntegration, TelegramIntegration, WhatsAppIntegration, WebhookIntegration


# DESIGN PATTERN: Simple Factory
class IntegrationFactory:
    @staticmethod
    def create_integration(type: str) -> Integration:
        match type.lower():
            case "discord":
                return DiscordIntegration()
            case "slack":
                return SlackIntegration()
            case "telegram":
                return TelegramIntegration()
            case "whatsapp":
                return WhatsAppIntegration()
            case "webhook":
                return WebhookIntegration()
            case _:
                raise ValueError(f"The provided feature type is not supported: {type}")
