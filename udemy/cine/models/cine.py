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
    peliculas_ids = fields.Many2many(
        comodel_name="presupuesto",
        relation="cine_peliculas_relation",
        column1="cine_id",
        column2="peliculas_id",
        string="Películas",
        copy=False
    )
    def aprobar_cine(self):
        logger.info("Se cambió el state a aprobado")
        self.state = "aprobado"
        self.fecha_aprobado = fields.Datetime.now()

    def cancelar_cine(self):
        logger.info("Se cambió el state a cancelado")
        self.state = "cancelado"