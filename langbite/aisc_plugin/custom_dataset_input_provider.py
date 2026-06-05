import csv
import io
import json

from aisc_plugin_interface.input_providers.base_input_provider import BaseInputProvider


class CustomDatasetInputProvider(BaseInputProvider):
    def _read_data(self, file_content) -> str:
        file_stream = io.BytesIO(file_content)
        wrapper = io.TextIOWrapper(file_stream, encoding='utf-8')
        reader = csv.DictReader(wrapper, delimiter="\t")
        data_list = list(reader)
        file_stream.close()
        return json.dumps(data_list)
