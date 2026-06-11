"""
Format a DiagnosisReply for each platform's markdown dialect.
WhatsApp uses *bold*, Telegram uses **bold** (MarkdownV2).
"""

from .api_client import DiagnosisReply

_CROP_MENU = {
    "fr": "Choisissez votre culture:\n1. Manioc\n2. Maïs\n3. Plantain\n4. Tomate\n5. Cacao",
    "en": "Choose your crop:\n1. Cassava\n2. Maize\n3. Plantain\n4. Tomato\n5. Cocoa",
}

_GREETING = {
    "fr": "Bonjour ! Je suis Ankara. Envoyez-moi une photo de votre plante malade.",
    "en": "Hello! I am Ankara. Send me a photo of your sick plant.",
}

_SEND_PHOTO = {
    "fr": "Bien reçu. Envoyez maintenant une photo de la plante.",
    "en": "Got it. Now send a photo of the plant.",
}

_CONSENT_REQUEST = {
    "fr": (
        "Avant de continuer : vos photos sont supprimées après 90 jours. "
        "Répondez OUI pour conserver vos photos plus longtemps et améliorer le service."
    ),
    "en": (
        "Before we continue: your photos are deleted after 90 days. "
        "Reply YES to keep photos longer and help improve the service."
    ),
}


def greeting(language: str) -> str:
    return _GREETING.get(language, _GREETING["fr"])


def crop_menu(language: str) -> str:
    return _CROP_MENU.get(language, _CROP_MENU["fr"])


def send_photo_prompt(language: str) -> str:
    return _SEND_PHOTO.get(language, _SEND_PHOTO["fr"])


def consent_request(language: str) -> str:
    return _CONSENT_REQUEST.get(language, _CONSENT_REQUEST["fr"])


def format_whatsapp(reply: DiagnosisReply, language: str) -> str:
    steps = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(reply.steps))
    escalation = f"\n\n⚠️ {reply.consult_message}" if reply.escalate else ""
    return (
        f"*{reply.label}* (confiance : {reply.confidence})\n\n"
        f"{reply.opening}\n\n"
        f"{steps}"
        f"{escalation}"
    )


def format_telegram(reply: DiagnosisReply, language: str) -> str:
    steps = "\n".join(f"{i + 1}\\. {s}" for i, s in enumerate(reply.steps))
    escalation = f"\n\n⚠️ {reply.consult_message}" if reply.escalate else ""
    return (
        f"**{reply.label}** \\(confiance : {reply.confidence}\\)\n\n"
        f"{reply.opening}\n\n"
        f"{steps}"
        f"{escalation}"
    )
