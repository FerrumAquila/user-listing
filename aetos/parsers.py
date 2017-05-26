# Package Imports
import yaml
from aetos_serialiser.serialisers import Serializer
from aetos_serialiser.helpers import dict_reducer


class YAMLParser(Serializer):
    BODY_MAP = {
        'type': ('__default__object', str),
        'properties': ('__self___get_properties', dict),
        'required': ('__self___get_required_properties', list),
    }
    REDUCER = dict_reducer

    def __init__(self, yaml_data):
        self.yaml_data = yaml_data
        super(YAMLParser, self).__init__(yaml.load(self._lines(1)))

    def _lines(self, start=None, end=None):
        lines = self.yaml_data.split('\n')
        if not start:
            start = 0
        if not end:
            end = len(lines)
        return '\n'.join(lines[start:end])

    def _get_parameter_values(self, attr):
        return [param[attr] for param in self.instance['parameters']]

    @property
    def _get_properties(self):
        return {name: {'type': 'string'} for name in self._get_parameter_values('name')}

    @property
    def _get_required_properties(self):
        return [param['name'] for param in self.instance['parameters'] if param['required']]
