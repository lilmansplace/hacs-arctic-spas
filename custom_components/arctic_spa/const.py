"""Constants for the Arctic Spa integration."""

DOMAIN = "arctic_spa"

API_BASE_URL = "https://api.myarcticspa.com/v2"
DEFAULT_SCAN_INTERVAL = 60
API_TIMEOUT = 15

CONF_API_KEY = "api_key"

ATTR_TEMPERATURE_F = "temperatureF"
ATTR_SETPOINT_F = "setpointF"
ATTR_PH = "ph"
ATTR_PH_STATUS = "ph_status"
ATTR_ORP = "orp"
ATTR_ORP_STATUS = "orp_status"
ATTR_FILTER_STATUS = "filter_status"
ATTR_FILTER_DURATION = "filter_duration"
ATTR_FILTER_FREQUENCY = "filter_frequency"
ATTR_FILTER_SUSPENSION = "filter_suspension"
ATTR_LIGHTS = "lights"
ATTR_PUMP1 = "pump1"
ATTR_PUMP2 = "pump2"
ATTR_PUMP3 = "pump3"
ATTR_CONNECTED = "connected"

MIN_TEMP_F = 60
MAX_TEMP_F = 104
