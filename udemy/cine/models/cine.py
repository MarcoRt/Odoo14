# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)

class Cine(models.Model):
    _name = "cine"

    _description = "Cine"

    name = fields.Char(string="Nombre del cine")
    salas = fields.Integer(string="Número de salas")
    fecha_creacion = fields.Datetime(
        string="Fecha de creación",
        copy=False,
        default=lambda self: fields.Datetime.now(),
    )
    fecha_aprobado = fields.Datetime(string="Fecha aprobado", copy=False)
    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection(
        selection=[
            ("borrador", "Borrador"),
            ("aprobado", "Aprobado"),
            ("cancelado", "Cancelado"),
        ],
        default="borrador",
        string="Estados",
        copy=False,
    )