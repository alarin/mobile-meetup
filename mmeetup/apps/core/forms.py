#encoding=utf-8
from django import forms
from django.forms.forms import BoundField
from django.utils.encoding import force_unicode, StrAndUnicode
from django.utils.html import conditional_escape
from django.forms.util import ErrorList

from supercaptcha import CaptchaField
from django.utils.safestring import mark_safe
from django.forms.fields import Field


class SportbetCaptchaField(CaptchaField):
    """ A CaptchaField with default empty label and understandable internal error message """
    def __init__(self, *args, **kwargs):
        defaults = {'label': u'',
                    'error_messages': {'internal': u'Превышено время ожидания. Введите новый код.'}
        }
        defaults.update(kwargs)
        super(SportbetCaptchaField, self).__init__(self, *args, **defaults)


class CoreFormMixin(object):
    """
    Ads classes for all form fields
    Removes : (semicolon) after labels
    Adds classes for errors
    """
#    def __init__(self, *args, **kwargs):
#        kwargs.update({
#            'error_class': ErrorListEx,
#            'label_suffix': ''})
#        super(BaseForm, self).__init__(*args, **kwargs)

    def as_div(self):
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
            normal_row = u'<div%(html_class_attr)s>%(errors)s %(label)s %(field)s%(help_text)s</div>',
            error_row = u'%s',
            row_ender = '</div>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        # -------- CHANGED ------------------
        # can't use __init__ in mixin :(
        self.error_class = ErrorListEx
        self.label_suffix = ''
        # -------- CHANGED ------------------
        
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = BoundField(self, field, name)
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.

                # -------- CHANGED ------------------
                classes = 'row f_%s' % bf.name
                if bf_errors:
                    classes += ' invalid'
                css_classes = bf.css_classes()
                if css_classes:
                    classes += ' ' + bf.css_classes()
                html_class_attr = ' class="%s"' % classes
                # -------- CHANGED ------------------

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))

                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''

                output.append(normal_row % {
                    'errors': force_unicode(bf_errors),
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr
                })

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text':'',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe(u'\n'.join(output))


class ErrorListEx(ErrorList):
    """
    Override default errors list, try to determine errors kind and add css classes
    """
    def as_ul(self):
        if not self: return u''
        errors = []
        for error in self:
            css_class = None
            css = ''
            if error == Field.default_error_messages['required']:
                css_class = 'required'
            if css_class:
                css = ' class="%s"' % css_class
            errors.append(u'<li%s>%s</li>' % (css, conditional_escape(force_unicode(error))))
        return mark_safe(u'<ul class="errorlist">%s</ul>' % ''.join(errors))


#coding=utf-8
import urlparse

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from dbtemplates.admin import CodeMirrorTextArea


class CodeMirrorTextAreaWithUpload(CodeMirrorTextArea):
    class Media:
        js = (urlparse.urljoin(settings.MEDIA_URL, 'js/jquery-1.6.1.min.js'),
              urlparse.urljoin(settings.MEDIA_URL, 'js/ajaxupload.js'))

    def render(self, name, value, attrs=None):
        result = []
        result.append(u"""
            <a id='upload_button_id_%(name)s' href="javascript: void(0)">Загрузить изображение</a>
            <div id='upload_response_id_%(name)s'></div>
            """ % {'name': name})
        result.append(u"""
            <script type="text/javascript">
            $(document).ready(function() {
                new AjaxUpload('upload_button_id_%(name)s', {
                    action: '%(href_upload)s',
                    name: 'userfile',
                    onComplete: function(file, response) {
                        $('#upload_response_id_%(name)s').text(response);
                    }
                });
            });
            </script>
            """ % {'href_upload': reverse('admin_upload_file_code_mirror'),
                   'name': name})
        result.append(
            super(CodeMirrorTextAreaWithUpload, self).render(name, value, attrs))
        return mark_safe(u"".join(result))


class UploadFileForm(forms.Form):
    userfile  = forms.ImageField()
