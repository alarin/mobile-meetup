from django.template import Library, TemplateSyntaxError
from django.template.base import getargspec, Node, Variable


class DevLibrary(Library):
    """Some cool stuff from django-dev version"""
    def assignment_tag(self, func=None, takes_context=None, name=None):
        def dec(func):
            params, xx, xxx, defaults = getargspec(func)
            if takes_context:
                if params[0] == 'context':
                    params = params[1:]
                else:
                    raise TemplateSyntaxError("Any tag function decorated with takes_context=True must have a first argument of 'context'")

            class AssignmentNode(Node):
                def __init__(self, params_vars, target_var):
                    self.params_vars = map(Variable, params_vars)
                    self.target_var = target_var

                def render(self, context):
                    resolved_vars = [var.resolve(context) for var in self.params_vars]
                    if takes_context:
                        func_args = [context] + resolved_vars
                    else:
                        func_args = resolved_vars
                    context[self.target_var] = func(*func_args)
                    return ''

            def compile_func(parser, token):
                bits = token.split_contents()
                tag_name = bits[0]
                bits = bits[1:]
                params_max = len(params)
                defaults_length = defaults and len(defaults) or 0
                params_min = params_max - defaults_length - 1 #my fix for no extra params
                if (len(bits) < 2 or bits[-2] != 'as'):
                    raise TemplateSyntaxError(
                        "'%s' tag takes at least 2 arguments and the "
                        "second last argument must be 'as'" % tag_name)
                params_vars = bits[:-2]
                target_var = bits[-1]
                if (len(params_vars) < params_min or
                        len(params_vars) > params_max):
                    if params_min == params_max:
                        raise TemplateSyntaxError(
                            "%s takes %s arguments" % (tag_name, params_min))
                    else:
                        raise TemplateSyntaxError(
                            "%s takes between %s and %s arguments"
                            % (tag_name, params_min, params_max))
                return AssignmentNode(params_vars, target_var)

            function_name = name or getattr(func, '_decorated_function', func).__name__
            compile_func.__doc__ = func.__doc__
            self.tag(function_name, compile_func)
            return func

        if func is None:
            # @register.assignment_tag(...)
            return dec
        elif callable(func):
            # @register.assignment_tag
            return dec(func)
        else:
            raise TemplateSyntaxError("Invalid arguments provided to assignment_tag")
