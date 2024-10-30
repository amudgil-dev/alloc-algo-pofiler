from datetime import datetime
import json
import numpy as np
import logging
import numpy as np
import scipy.stats as stats
from scipy.stats import erlang

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Util:
    @staticmethod
    def generate_filename(prefix, extension):
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"


# encodr to avoid the "TypeError: Object of type int64 is not JSON serializable"
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class FileUtil:
    # logger = logging.getLogger(__name__)

    @staticmethod
    def save_as_json(data, filename):
        def is_serializable(obj):
            try:
                json.dumps(obj, cls=NumpyEncoder)
                return True
            except (TypeError, ValueError):
                return False

        def clean_for_serialization(obj):
            if isinstance(obj, dict):
                return {
                    k: clean_for_serialization(v)
                    for k, v in obj.items()
                    if is_serializable(k)
                }
            elif isinstance(obj, list):
                return [
                    clean_for_serialization(item)
                    for item in obj
                    if is_serializable(item)
                ]
            elif is_serializable(obj):
                return obj
            else:
                FileUtil.logger.warning(f"Removed non-serializable item: {type(obj)}")
                return None

        cleaned_data = clean_for_serialization(data)

        if cleaned_data != data:
            FileUtil.logger.warning(
                "Some data was removed due to serialization issues."
            )

        with open(filename, "w") as f:
            json.dump(cleaned_data, f, indent=4, cls=NumpyEncoder)

        return cleaned_data
