# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class Presupuesto(models.Model):

    _inherit = "presupuesto"

    cines_ids = fields.Many2many(
        comodel_name="cine",
        relation="pelicuas_cine_relation",
        column1="peliculas_id",
        column2="cines_id",
        string="Cines",
        copy=False
    )
    def write(self,variables):
        logger.info("Soy variables de la clase heredada: {0}".format(variables))
        if "name" in variables and self.state == "aprobado":
            raise UserError("El nombre no se puede editar.")
        return super(Presupuesto, self).write(variables)
