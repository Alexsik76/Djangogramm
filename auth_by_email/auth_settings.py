# Contains placeholders anf icons for the used in the project templatetags
from dataclasses import dataclass


@dataclass
class FieldAttrs:
    placeholder: str
    icon: str


FIELDS_ATTR = {'unknown': FieldAttrs('field', 'fas fa-question-circle'),
               'email': FieldAttrs('user@example.com', 'fas fa-envelope'),
               'username': FieldAttrs('user@example.com', 'fas fa-user-alt'),
               'first_name': FieldAttrs('Jon', 'fas fa-user-alt'),
               'last_name': FieldAttrs('Snow', 'fas fa-user'),
               'avatar': FieldAttrs('valid image file', ''),
               'bio': FieldAttrs('gender', ''),
               'password': FieldAttrs('enter your password', 'fas fa-lock'),
               'password1': FieldAttrs('password', 'fas fa-lock'),
               'password2': FieldAttrs('the same password', 'fas fa-lock'),
               'new_password1': FieldAttrs('password', 'fas fa-lock'),
               'new_password2': FieldAttrs('the same password', 'fas fa-lock'),
               'title': FieldAttrs('post title', 'fas fa-heading'),
               'image': FieldAttrs('valid image file', '')
               }
