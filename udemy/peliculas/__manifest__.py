# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Modulo de peliculas',
    'version': '1.0',
    'category': 'Pelicula',
    'depends': ['contacts','mail'],
    'author': 'Marco Rodriguez',
    'summary': 'Modulo de presupuestos para peliculas',
    'website': 'google.com',
    'description': """
Modulo para hacer presupuestos de películas.
======================================

Este es un módulo de prueba de un curso de udemy.
    """,
    'data': ['security/security.xml',
            'security/ir.model.access.csv',
            'report/reporte_pelicula.xml',
            'data/secuencia.xml',
            'data/categoria.xml',
            'wizard/update_wizard_views.xml',
            'views/menu.xml',
            'views/presupuesto_views.xml'],
}
