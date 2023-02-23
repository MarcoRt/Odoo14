# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Genero(models.Model):
    _name = "genero"

    _description = "Generos de las películas"

    name = fields.Char()
