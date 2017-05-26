# App Imports
import model_utils.fields as model_util_fields

# Package Imports
import time
import calendar
import pytz
import json

# Django Imports
import django.db.models.fields as model_fields
import django.db.models.fields.related as related_fields
from django.template.loader import render_to_string


class MaterialForm(object):
    DROPDOWN_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/dropdown-input.html'
    SIMPLE_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/simple-input.html'
    INTEGER_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/integer-input.html'
    HIDDEN_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/hidden-input.html'
    TEXT_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/text-input.html'
    JSON_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/json-input.html'
    DATETIME_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/datetime-input.html'
    BOOL_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/bool-input.html'
    MULTISELECT_FORM_GROUP_TEMPLATE = 'material-forms/form-groups/multiselect-input.html'

    FORM_GROUP_VALIDATION_TEMPLATE = 'material-forms/form-groups/validation.html'
    MATERIAL_FORM_TEMPLATE = 'material-forms/form.html'

    IGNORE_FIELD_NAMES = [
        'created_by',
        'modified_by',
        'is_active',
        'meta'
    ]

    IGNORE_FIELD_TYPES = [
        model_util_fields.AutoCreatedField,
        model_util_fields.AutoLastModifiedField,
    ]

    DISPLAY_MAP = dict()

    def __init__(self, request, model, action=None, instance=None, parent=None, display_fields=None):
        self.model = model
        self.request = request
        self.instance = instance
        self.parent = parent
        self.action = action
        self._meta = self.model._meta
        self.validation_html = render_to_string(self.FORM_GROUP_VALIDATION_TEMPLATE, request=self.request)

        self.display_ignore = lambda f: type(f) in self.IGNORE_FIELD_TYPES or f.name in self.IGNORE_FIELD_NAMES

        self.get_field_choices = lambda df: [{'name': choice[0], 'verbose': choice[1]} for choice in df.choices]

        self.get_fk_choices = lambda df: [{'name': choice.pk, 'verbose': choice.name}
                                          for choice in df.related_model.objects.filter()]

        self.meta_fields = self._meta.fields + self._meta.many_to_many
        self.display_fields = display_fields or [field.name for field in self.meta_fields
                                                 if not self.display_ignore(field)]

        self._get_template_data = {
            related_fields.ForeignKey: lambda df, dfm: {
                'template_path': self.DROPDOWN_FORM_GROUP_TEMPLATE,
                'template_type': 'dropdown',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name, ''),
                    'options': self.get_fk_choices(df),
                    'validation': self.validation_html,
                    'col_class': dfm['col_class']
                }
            },
            related_fields.OneToOneField: lambda df, dfm: {
                'template_path': self.DROPDOWN_FORM_GROUP_TEMPLATE,
                'template_type': 'dropdown',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name, ''),
                    'options': df.related_model.objects.filter(),
                    'validation': self.validation_html,
                    'col_class': dfm['col_class']
                }
            },
            related_fields.ManyToManyField: lambda df, dfm: {
                'template_path': self.MULTISELECT_FORM_GROUP_TEMPLATE,
                'template_type': 'multiselect',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name).all().values_list('id', flat=True) if self.instance else [],
                    'options': [{'name': o.pk, 'verbose': str(o)} for o in df.related_model.objects.filter()],
                    'validation': self.validation_html,
                    'col_class': dfm['col_class']
                }
            },
            model_fields.IntegerField: lambda df, dfm: {
                'template_path': self.SIMPLE_FORM_GROUP_TEMPLATE if not df.choices else self.DROPDOWN_FORM_GROUP_TEMPLATE,
                'template_type': 'simple',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name, ''),
                    'validation': self.validation_html,
                    'options': self.get_field_choices,
                    'col_class': dfm['col_class']
                }
            },
            model_fields.PositiveSmallIntegerField: lambda df, dfm: {
                'template_path': self.SIMPLE_FORM_GROUP_TEMPLATE if not df.choices else self.DROPDOWN_FORM_GROUP_TEMPLATE,
                'template_type': 'simple',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name, ''),
                    'validation': self.validation_html,
                    'options': self.get_field_choices,
                    'col_class': dfm['col_class']
                }
            },
            model_fields.AutoField: lambda df, dfm: {
                'template_path': self.HIDDEN_FORM_GROUP_TEMPLATE,
                'template_type': 'hidden',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name, ''),
                    'validation': self.validation_html,
                    'col_class': dfm['col_class']
                }
            },
            model_fields.DateTimeField: lambda df, dfm: {
                'template_path': self.DATETIME_FORM_GROUP_TEMPLATE,
                'template_type': 'datetime',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name).astimezone(
                        pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%dT%H:%M') if getattr(
                        self.instance, df.name, None) else '',
                    'validation': self.validation_html,
                    'col_class': dfm['col_class']
                }
            },
            model_fields.BooleanField: lambda df, dfm: {
                'template_path': self.BOOL_FORM_GROUP_TEMPLATE,
                'template_type': 'datetime',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name, None),
                    'validation': self.validation_html,
                    'col_class': dfm['col_class']
                }
            },
            model_fields.CharField: lambda df, dfm: {
                'template_path': self.SIMPLE_FORM_GROUP_TEMPLATE if not df.choices else self.DROPDOWN_FORM_GROUP_TEMPLATE,
                'template_type': 'simple',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name, ''),
                    'validation': self.validation_html,
                    'options': self.get_field_choices(df),
                    'section': df.model._meta.label_lower.split('.')[-1],
                    'col_class': dfm['col_class']
                }
            },
            model_fields.TextField: lambda df, dfm: {
                'template_path': self.JSON_FORM_GROUP_TEMPLATE if df.name == 'doc_json' else self.TEXT_FORM_GROUP_TEMPLATE ,
                'template_type': 'text',
                'context': {
                    'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                    'input_placeholder': getattr(self.instance, df.name, ''),
                    'validation': self.validation_html,
                    'col_class': dfm['col_class']
                }
            },
        }
        self._default_template_data = lambda df, dfm: {
            'template_path': self.SIMPLE_FORM_GROUP_TEMPLATE,
            'template_type': 'simple',
            'context': {
                'label': df.verbose_name, 'input_name': df.name, 'is_null': df.null,
                'input_placeholder': getattr(self.instance, df.name, ''),
                'validation': self.validation_html,
                'col_class': dfm['col_class']
            }
        }
        self._extra_field_template_data = lambda f, dfm: {
            'template_path': self.SIMPLE_FORM_GROUP_TEMPLATE,
            'template_type': 'simple',
            'context': {
                'label': f, 'input_name': f,
                'input_placeholder': (json.loads(self.instance.meta or '{}')
                                      if self.instance else dict()).get(f) or '',
                'validation': self.validation_html,
                'col_class': dfm['col_class']
            }
        }

    @property
    def _field_groups(self):
        field_groups = dict()
        for field in self.display_fields:
            display_field_map = self.DISPLAY_MAP.get(field) or {'group_name': 'Others', 'pos': 1}
            if not display_field_map['group_name'] in field_groups:
                field_groups.update({display_field_map['group_name']: list()})
            form_groups = field_groups[display_field_map['group_name']]
            form_groups.append((field, display_field_map))

        other_fields = field_groups['Others']
        blocks = 12
        fields = len(other_fields)
        for other_field in other_fields:
            assigned_blocks = blocks / fields
            other_field[1].update({'col_class': 'col-sm-%s' % assigned_blocks})
            blocks -= assigned_blocks
            fields -= 1

        return {group_name: sorted(field_group, key=lambda k: k[1]['pos'])
                for group_name, field_group in field_groups.items()}

    @property
    def form_data(self):
        return self._render_form(self._field_groups)

    def _get_model_field(self, field):
        for df in self.meta_fields:
            if df.name == field:
                return df

    def _render_form(self, groups):
        form_id = '%s-%s-form' % (
            self._meta.label_lower.split('.')[-1],
            self.instance.id if self.instance else calendar.timegm(time.gmtime())
        )
        return render_to_string(self.MATERIAL_FORM_TEMPLATE, {
            'form_id': form_id,
            'action': self.action,
            'groups': self._render_field_group(groups),
            'parent_id': self.parent.pk if self.parent else None,
            'parent_key': self.parent._meta.label_lower.split('.')[-1] if self.parent else None,
        }, request=self.request), form_id

    def _render_field_group(self, groups):
        return {name: [self._render_form_field(fg[0], fg[1]) for fg in form_groups] for name, form_groups in groups.items()}

    def _render_form_field(self, field, display_field_map):
        model_field = self._get_model_field(field)
        default_data = self._default_template_data
        if model_field:
            template_data = self._get_template_data.get(type(model_field), default_data)(model_field, display_field_map)
        else:
            template_data = self._extra_field_template_data(field, display_field_map)
        return render_to_string(template_data['template_path'], template_data['context'], request=self.request)
