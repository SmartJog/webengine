'''
{% sjversion %} tag for webengine templates.

Will be replace by the current version of the server.
'''
from django import template
register = template.Library()

class sjversionNode(template.Node):
    def render(self, context):
        try:
            version = open("/etc/sjversion").read().strip().split('+')[0].split('_')[0]
        except:
            version = ""
            pass

        return version

@register.tag(name="sjversion")
def do_sjversion(parser, token):
    return sjversionNode()
