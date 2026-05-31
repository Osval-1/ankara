import enum


class Crop(str, enum.Enum):
    cassava = "cassava"
    maize = "maize"
    plantain = "plantain"
    tomato = "tomato"
    cocoa = "cocoa"


class CropClass(str, enum.Enum):
    # cassava
    cassava_healthy = "cassava_healthy"
    cassava_cmd = "cassava_cmd"
    cassava_cbsd = "cassava_cbsd"
    cassava_pest = "cassava_pest"
    cassava_unknown = "cassava_unknown"
    # maize
    maize_healthy = "maize_healthy"
    maize_streak = "maize_streak"
    maize_blight = "maize_blight"
    maize_rust = "maize_rust"
    maize_unknown = "maize_unknown"
    # plantain
    plantain_healthy = "plantain_healthy"
    plantain_bbs = "plantain_bbs"
    plantain_fusarium = "plantain_fusarium"
    plantain_weevil = "plantain_weevil"
    plantain_unknown = "plantain_unknown"
    # tomato
    tomato_healthy = "tomato_healthy"
    tomato_blight = "tomato_blight"
    tomato_leaf_curl = "tomato_leaf_curl"
    tomato_mosaic = "tomato_mosaic"
    tomato_unknown = "tomato_unknown"
    # cocoa
    cocoa_healthy = "cocoa_healthy"
    cocoa_blackpod = "cocoa_blackpod"
    cocoa_swollen_shoot = "cocoa_swollen_shoot"
    cocoa_mirids = "cocoa_mirids"
    cocoa_unknown = "cocoa_unknown"


class Channel(str, enum.Enum):
    whatsapp = "whatsapp"
    telegram = "telegram"
    mobile = "mobile"
    web = "web"


class Language(str, enum.Enum):
    fr = "fr"
    en = "en"


class ConfidenceLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class UserRole(str, enum.Enum):
    admin = "admin"
    agronomist = "agronomist"
    extension_worker = "extension_worker"
    labeler = "labeler"
