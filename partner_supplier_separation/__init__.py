from . import models

def mark_contacts_as_customer_and_supplier(env):
    env.cr.execute("UPDATE res_partner SET supplier = True WHERE supplier_rank > 0")
    env.cr.execute("UPDATE res_partner SET customer = True WHERE customer_rank > 0")
