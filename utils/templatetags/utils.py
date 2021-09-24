from django.template import Library, Node, loader, TemplateSyntaxError, resolve_variable
from django.template.context import Context

register = Library()


class RenderPartialNode(Node):
    def __init__(self, params):
        self.params = params
        self.controller = self.params.pop("controller")
        self.view = self.params.pop("view")
        self.name = self.controller + "/_" + self.view + ".html"

    def render(self, context):
        print self.params
        for k, v in self.params.items():
            print "Resolve " + str(v)
            # self.params[k] = resolve_variable(v, context)
            self.params[k] = v
        context.update(self.params)
        template = loader.get_template(self.name)
        return template.render(context)


@register.tag
def render_partial(parser, token):
    """
    render_partial template tag.
    Two parameters are needed to correctly display the right partial template:
      * controller:controller_name
      * view:view_name
    The final path for the view will be controller/templates/_view_name.html
    Only HTML partial are authorized, until partials into xml templates are totally useless.
    """
    items = token.split_contents()
    if len(items) < 3:
        raise TemplateSyntaxError("Missing template tag parameters")
    params = {}
    for item in items[1:]:
        k, v = item.split(":")
        params[k] = v
    for k in ["controller", "view"]:
        if k not in params.keys():
            raise TemplateSyntaxError(
                'Parameters "controller" and "view" are required.'
            )
    return RenderPartialNode(params)


@register.filter
def truncate(value, arg):
    """
    Truncates a string after a given number of chars
    Argument: Number of chars to truncate after
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    if not isinstance(value, basestring):
        value = str(value)
    if len(value) > length:
        return value[:length] + "..."
    else:
        return value
