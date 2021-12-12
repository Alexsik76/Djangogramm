from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
import logging


logger = logging.getLogger(__name__)
register = template.Library()


def get_field_attr(field: str, attr_name: str) -> str:
    obj = settings.FIELDS_ATTR.get(field, 'unknown')
    attr = getattr(obj, attr_name, '')
    return attr


def add_error_class(field):
    if not field.errors:
        return ''
    return ' is-danger'


def add_placeholder(field):
    placeholder = get_field_attr(field.name, 'placeholder')
    return placeholder


def add_alert_icon(field):
    if not field.errors:
        return ''
    return mark_safe('<span class="icon is-small is-right"><i class="fas fa-exclamation-triangle"></i></span>')


def add_field_icon(field):
    icon = get_field_attr(field.name, 'icon')
    return '' if not icon else mark_safe(f'<span class="icon is-small is-left"><i class="{icon}"></i></span>')


def update_widget_attrs(field, widget):
    attrs = {'class': f"input{add_error_class(field)}",
             'id': field.auto_id,
             'placeholder': add_placeholder(field),
             }
    widget.attrs.update(attrs)


@register.inclusion_tag('auth_by_email/bulma_templates/field.html', takes_context=True)
def bulma_field(context):
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
    form = context['form']
    return {
        'form': form,
    }


@register.inclusion_tag('auth_by_email/bulma_templates/button.html')
def button_bulma(btn_class='is-success', name='Submit'):
    return {'btn_class': btn_class,
            'btn_name': name.capitalize()
            }


@register.filter
def get_file_name(value):
    try:
        items_value = value.url.split('/')
        return items_value[-1]
    except AttributeError as e:
        logger.info(e)
        return 'File not set'


@register.filter
def by_rows(page):
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


@register.inclusion_tag('gramm_app/bulma_templates/like_for_post.html', takes_context=True)
def like_icon(context):
    post = context['post']
    user = context.request.user
    if post.likes.filter(liker_id=user.id):
        icon_class = 'fas fa-heart'
    else:
        icon_class = 'far fa-heart'
    return {
        'post': post,
        'icon_class': icon_class
    }
