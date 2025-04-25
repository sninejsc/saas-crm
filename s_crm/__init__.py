# -*- coding: utf-8 -*-

from . import controllers
from . import pyarmor_runtime_000000
from . import models

def post_init_hook_remove_rule_core_crm(env):
    env.ref('crm.crm_lead_company_rule').write({
        'active': False,
    })
    env.ref('base.res_partner_rule').write({
        'active': False,
    })
    env.ref('sale.sale_order_comp_rule').write({
        'active': False,
    })

def uninstall_hook_setup_rule_core_crm(env):
    env.ref('crm.crm_lead_company_rule').write({
        'active': True,
    })
    env.ref('base.res_partner_rule').write({
        'active': True,
    })
    env.ref('sale.sale_order_comp_rule').write({
        'active': True,
    })
