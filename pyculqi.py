#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'

import json
import sys
import logging

from requests import request

if sys.version_info >= (3, 0):
    import culqi_aes_py3 as culqi_aes
else:
    import culqi_aes_py2 as culqi_aes

codigo_comercio = None
llave_secreta = None

param_codigo_comercio = 'codigo_comercio'
param_informacion_venta = 'informacion_venta'
param_ticket = 'ticket'
param_extra = 'extra'

servidor_base = 'https://integ-pago.culqi.com'
url_api_base = '/api/v1'
url_api_crear_venta = '/crear'
url_api_devolver_venta = '/devolver'
url_api_consultar_venta = '/consultar'


def cifrar(str):
    log = logging.getLogger('pyculqi::cifrar')
    try:
        return culqi_aes.encrypt(str, llave_secreta)
    except Exception as e:
        log.debug("", exc_info=True)
        return str


def decifrar(str):
    log = logging.getLogger('pyculqi::decifrar')
    try:
        return culqi_aes.decrypt(str, llave_secreta)
    except Exception as e:
        log.debug("", exc_info=True)
        return str


def do_request(method, url, data):
    return request('POST', url, data=json.dumps(data),
        headers= {
            'Content-Type': 'application/json'
        }
    )


def crear_venta(datos, canal = 'web', extra=None):
    log = logging.getLogger('pyculqi::crear_venta')
    added_params = {
        param_codigo_comercio: codigo_comercio,
    }
    if extra:
        added_params[param_extra] = extra
    raw_info_venta = dict(datos, **added_params)
    encrypted_info_venta = cifrar(json.dumps(raw_info_venta))
    data = {
        param_codigo_comercio: codigo_comercio,
        param_informacion_venta: encrypted_info_venta
    }
    final_url = '%s%s/%s%s' % (servidor_base, url_api_base, canal, url_api_crear_venta)
    response = do_request('POST', final_url, data)
    log.debug("Respuesta: " + response.text)
    return json.loads(decifrar(response.text))


def devolver_venta(ticket):
    log = logging.getLogger('pyculqi::devolver_venta')
    raw_info_venta = {
        param_ticket: ticket
    }
    encrypted_info_venta = cifrar(json.dumps(raw_info_venta))
    data = {
        param_codigo_comercio: codigo_comercio,
        param_informacion_venta: encrypted_info_venta
    }
    final_url = servidor_base + url_api_base + url_api_devolver_venta
    response = do_request('POST', final_url, data)
    log.debug("Respuesta: " + response.text)
    return json.loads(decifrar(response.text))


def consultar_venta(ticket):
    log = logging.getLogger('pyculqi::consultar_venta')
    raw_info_venta = {
        param_ticket: ticket
    }
    encrypted_info_venta = cifrar(json.dumps(raw_info_venta))
    data = {
        param_codigo_comercio: codigo_comercio,
        param_informacion_venta: encrypted_info_venta
    }
    final_url = servidor_base  + url_api_base + url_api_consultar_venta
    response = do_request('POST', final_url, data)
    log.debug("Respuesta: " + response.text)
    return json.loads(decifrar(response.text))
