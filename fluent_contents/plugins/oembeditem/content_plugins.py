"""
Definition of the plugin.
"""
from django.utils.translation import ugettext_lazy as _
from fluent_contents.extensions import ContentPlugin, plugin_pool
from fluent_contents.plugins.oembeditem.forms import OEmbedItemForm
from fluent_contents.plugins.oembeditem.models import OEmbedItem
import re

re_safe = re.compile(r'[^\w_-]')


@plugin_pool.register
class OEmbedPlugin(ContentPlugin):
    model = OEmbedItem
    category = _('Online content')
    admin_form_template = "admin/fluent_contents/plugins/oembeditem/admin_form.html"
    render_template = "fluent_contents/plugins/oembed/default.html"

    form = OEmbedItemForm
    fieldsets = (
        (None, {
            'fields': (
                'embed_url',
                ('embed_max_width', 'embed_max_height'),
            ),
        }),
    )

    class Media:
        css = {
            'screen': (
                'fluent_contents/plugins/oembed/oembed_admin.css',
            )
        }


    def get_render_template(self, request, instance, **kwargs):
        """
        Allow to style the item based on the type.
        """
        safe_filename = re_safe.sub('', instance.type or 'default')
        return [
            "fluent_contents/plugins/oembed/{type}.html".format(type=safe_filename),
            self.render_template
        ]
