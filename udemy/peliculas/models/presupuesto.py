# -*- coding:utf-8 -*-

import logging

from odoo.exceptions import UserError

from odoo import fields, models, api

logger = logging.getLogger(__name__)


class Presupuesto(models.Model):
    _name = "presupuesto"
    _description = "Presupuesto de las películas"
    _inherit = ["image.mixin", "mail.activity.mixin", "mail.thread"]

    @api.depends("detalle_ids")
    def _compute_total(self):
        for record in self:
            total = 0
            for linea in record.detalle_ids:
                total += linea.importe
            record.base = total
            record.impuestos = total * 0.16
            record.total = record.base + record.impuestos

    name = fields.Char(string="Película")
    clasificacion = fields.Selection(
        selection=[
            ("G", "G"),  # Público en general
            ("PG", "PG"),  # Se recomienda la compañía de un adulto
            ("PG-13", "PG-13"),  # Mayores de 13
            ("R", "R"),  # En compañía de un adulto obligatorio
            ("NC-17", "NC-17"),  # Mayores de 18
        ],
        string="Clasificación",
    )
    dsc_clasificacion = fields.Char(string="Descripción clasificación")
    fecha_estreno = fields.Date(string="Fecha de estreno")
    puntuacion = fields.Integer(string="Puntuacion", related="puntuacion2")
    puntuacion2 = fields.Integer(string="Puntuacion2")
    active = fields.Boolean(string="Activo", default=True)
    director_id = fields.Many2one(comodel_name="res.partner", string="Director")
    categoria_director_id = fields.Many2one(
        comodel_name="res.partner.category",
        string="Categoría director",
        default=lambda self: self.env.ref("peliculas.category_director"),
    )
    actor_ids = fields.Many2many(comodel_name="res.partner", string="Actores")
    categoria_actor_id = fields.Many2one(
        comodel_name="res.partner.category",
        string="Categoría actor",
        default=lambda self: self.env.ref("peliculas.category_actor"),
    )
    genero_ids = fields.Many2many(comodel_name="genero", string="Género(s)")
    vista_general = fields.Text(string="Descripción")
    link_trailer = fields.Char(string="Trailer")
    es_libro = fields.Boolean(string="Version libro")
    libro = fields.Binary(string="Libro")
    libro_filename = fields.Char(string="Nombre del libro")

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

    fecha_aprobado = fields.Datetime(string="Fecha aprobado", copy=False)

    num_presupuesto = fields.Char(string="Número presupuesto", copy=False)

    opinion = fields.Html(String="Opinion")

    fecha_creacion = fields.Datetime(
        string="Fecha de creación",
        copy=False,
        default=lambda self: fields.Datetime.now(),
    )

    detalle_ids = fields.One2many(
        comodel_name="presupuesto.detalle",
        inverse_name="presupuesto_id",
        string="Detalles",
    )

    campos_ocultos = fields.Boolean(string="Campos ocultos")

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Moneda",
        default=lambda self: self.env.company.currency_id.id,
    )

    terminos = fields.Text(string="Términos")
    base = fields.Monetary(string="Base imponible", compute="_compute_total")
    impuestos = fields.Monetary(string="Impuestos", compute="_compute_total")
    total = fields.Monetary(string="Total", compute="_compute_total")

    def aprobar_presupuesto(self):
        logger.info("Se cambió el state a aprobado")
        self.state = "aprobado"
        self.fecha_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        logger.info("Se cambió el state a cancelado")
        self.state = "cancelado"

    def unlink(self):
        logger.info("Se ejecuta la función unlink")
        for record in self:
            if record.state != "cancelado":
                raise UserError(
                    "No se puede eliminar un registro que no está cancelado"
                )
            super(Presupuesto, record).unlink()

    @api.model
    def create(self, variables):
        logger.info("Variables: {0}".format(variables))
        sequence_obj = self.env["ir.sequence"]
        correlativo = sequence_obj.next_by_code("secuencia.presupuesto.pelicula")
        variables["num_presupuesto"] = correlativo
        return super(Presupuesto, self).create(variables)

    def write(self, variables):
        logger.info("Variables: {0}".format(variables))
        if "clasificacion" in variables:
            raise UserError("La clasificación no se puede editar.")
        return super(Presupuesto, self).write(variables)

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = self.name + " (Copia)"
        default["puntuacion2"] = 1
        return super(Presupuesto, self).copy(default)

    @api.onchange("clasificacion")
    def _onchange_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == "G":
                self.dsc_clasificacion = "Público en general"

            if self.clasificacion == "PG":
                self.dsc_clasificacion = "Se recomienda la compañía de un adulto"

            if self.clasificacion == "PG-13":
                self.dsc_clasificacion = "Mayores de 13"

            if self.clasificacion == "R":
                self.dsc_clasificacion = "En compañía de un adulto obligatorio"

            if self.clasificacion == "NC-17":
                self.dsc_clasificacion = "Mayores de 18"

        else:
            self.dsc_clasificacion = False


class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"

    presupuesto_id = fields.Many2one(
        comodel_name="presupuesto",
        string="Presupuesto",
    )

    name = fields.Many2one(comodel_name="recurso.cinematografico", string="Recurso")

    descripcion = fields.Char(string="Descripción", related="name.descripcion")
    precio = fields
    contacto_id = fields.Many2one(
        comodel_name="res.partner", string="Contacto", related="name.contacto_id"
    )
    imagen = fields.Binary(string="Imagen", related="name.imagen")
    cantidad = fields.Float(string="Cantidad", default=1.0, digits=(16, 4))
    precio = fields.Float(string="Precio", digits="Product Price")
    importe = fields.Monetary(string="Importe")

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Moneda",
        related="presupuesto_id.currency_id",
    )

    @api.onchange("name")
    def _onchange_name(self):
        if self.name:
            self.precio = self.name.precio

    @api.onchange("cantidad", "precio")
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio
