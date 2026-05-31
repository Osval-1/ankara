from ..models.enums import ConfidenceLevel, Crop

# Temperature scaling parameters per crop. Tuned on the held-out validation set
# and stored here so calibration can be retuned without retraining the model.
_TEMPERATURE: dict[Crop, float] = {
    Crop.cassava: 1.0,
    Crop.maize: 1.0,
    Crop.plantain: 1.0,
    Crop.tomato: 1.0,
    Crop.cocoa: 1.0,
}

_LOW_THRESHOLD = 0.5
_HIGH_THRESHOLD = 0.85


class ConfidenceCalibrator:
    def calibrate(self, raw_softmax: float, crop: Crop) -> ConfidenceLevel:
        temperature = _TEMPERATURE.get(crop, 1.0)
        calibrated = raw_softmax / temperature
        if calibrated >= _HIGH_THRESHOLD:
            return ConfidenceLevel.high
        if calibrated >= _LOW_THRESHOLD:
            return ConfidenceLevel.medium
        return ConfidenceLevel.low
