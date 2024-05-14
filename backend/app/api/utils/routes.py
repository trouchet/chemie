from fastapi.responses import JSONResponse
from fastapi import UploadFile
import shutil


def make_json_response(status_: int, content_: dict) -> JSONResponse:
    """
    Descrição: Retorna uma resposta JSON com o código de status e conteúdo especificados.
    Parâmetros:
        status_ (int): O código de status da resposta.
        content_ (dict): O conteúdo da resposta em formato de dicionário.
    Retorna:
        JSONResponse: Uma resposta JSON com o código de status e conteúdo especificados.
    """
    return JSONResponse(status_code=status_, content=content_)


def make_error_response(content_: dict):
    """
    Descrição: Retorna uma resposta de erro com o conteúdo especificado.

    Parâmetros:
        content_ (dict): O conteúdo da resposta em formato de dicionário.

    Retorna:
        JSONResponse: Uma resposta de erro com o conteúdo especificado.
    """
    return make_json_response(400, content_)
