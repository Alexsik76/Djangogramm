from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
import logging
import json

logger = logging.getLogger(__name__)
register = template.Library()


def get_field_attr(field_type: str, attr_name: str) -> str:
    """
    Gets placeholder or fas-icon depending on field type from dict.
    FIELD_ATTR: Dict(key(str): field type;
                     value(dataclass.object): contains object of the class FieldAttrs:
                                                                                 placeholder: str
                                                                                 icon: str
    )
    Provided types of te fields: [
                                unknown
                                email
                                username
                                first_name
                                last_name
                                avatar
                                bio
                                password
                                password1
                                password2
                                new_password1
                                new_password2
                                title
                                image]
        For existing types of the fields returns placeholder "field" and icon "fas fa-question-circle"
        For existing names of the attribute (not placeholder or icon) returns empty string
     """
    obj = settings.FIELDS_ATTR.get(field_type, 'unknown')
    attr = getattr(obj, attr_name, '')
    return attr


def add_error_class(field):
    """Creates is-danger for the field with errors."""
    if not field.errors:
        return ''
    return ' is-danger'


def add_placeholder(field):
    """Creates a specific placeholder for the field depending on its type."""
    placeholder = get_field_attr(field.name, 'placeholder')
    return placeholder


def add_alert_icon(field):
    """Adds alert icon to the field with errors"""
    if not field.errors:
        return ''
    return mark_safe('<span class="icon is-small is-right"><i class="fas fa-exclamation-triangle"></i></span>')


def add_field_icon(field):
    """
    Creates a specific icon for the field depending on its type.
    See the list of supported classes in the docstring fot the get_field_attrs()
    """
    icon = get_field_attr(field.name, 'icon')
    return '' if not icon else mark_safe(f'<span class="icon is-small is-left"><i class="{icon}"></i></span>')


def update_widget_attrs(field, widget):
    """Adds extra attributes for the widget"""
    attrs = {'class': f"input{add_error_class(field)}",
             'id': field.auto_id,
             'placeholder': add_placeholder(field),
             }
    widget.attrs.update(attrs)


@register.inclusion_tag('auth_by_email/bulma_templates/field.html', takes_context=True)
def bulma_field(context):
    """Creates field with bulma's markup."""
    field = context['field']
    widget = field.field.widget
    update_widget_attrs(field, widget)
    return {
        'field': field,
        'left_icon': add_field_icon(field),
        'right_icon': add_alert_icon(field)
    }


@register.inclusion_tag('auth_by_email/bulma_templates/form_content.html', takes_context=True)
def form_bulma(context):
    """Creates form with bulma's markup"""
    form = context['form']
    return {
        'form': form,
    }


@register.inclusion_tag('auth_by_email/bulma_templates/button.html')
def button_bulma(btn_class='is-success', name='Submit'):
    """Creates button with bulma classes"""
    return {'btn_class': btn_class,
            'btn_name': name.capitalize()
            }


@register.filter
def get_file_name(value):
    """Cuts filename from full path to file."""
    try:
        items_value = value.url.split('/')
        return items_value[-1]
    except AttributeError as e:
        logger.info(e)
        return 'File not set'


@register.filter
def by_rows(page):
    """
    Splits posts in the page to rows by 3 post in the row.
    Return list of rows.
    """
    rows = []
    page_like_list = list(page.object_list)
    while page_like_list:
        row = []
        for i in range(3):
            if page_like_list:
                row.append(page_like_list.pop())
            else:
                break
        rows.append(row)
    return rows


@register.filter
def is_liked(post, user):
    return json.dumps(post.is_liked(user))

