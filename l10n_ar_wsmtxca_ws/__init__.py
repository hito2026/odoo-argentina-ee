##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from . import models
from . import wizards

# Monkey patch: permitir XML de respuesta de AFIP con profundidad > 256 niveles
# Soluciona: "Excessive depth in document: 256 use XML_PARSE_HUGE option"
from lxml import etree
from odoo.addons.l10n_ar_edi.models.l10n_ar_afipws_connection import ARTransport

_original_ar_transport_post = ARTransport.post


def _patched_ar_transport_post(self, address, message, headers):
    response = _original_ar_transport_post(self, address, message, headers)
    # Re-parsear la respuesta con huge_tree=True para soportar XML profundo
    parser = etree.XMLParser(huge_tree=True)
    self.xml_response = etree.tostring(
        etree.fromstring(response.content, parser=parser),
        pretty_print=True,
    ).decode("utf-8")
    return response


ARTransport.post = _patched_ar_transport_post
