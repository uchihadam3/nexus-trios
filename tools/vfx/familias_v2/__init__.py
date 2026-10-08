"""
Famílias novas de efeitos (100+), desenhadas em Python como as primeiras.

Cada módulo temático tem uma lista REGISTRO de (nome, função, tela,
descrição, laço). generate_families.py registra todas junto das originais;
saem na mesma pasta (public/assets/vfx/familias), no mesmo formato.
"""
from . import apoio, corpo, cortes, elementos, energia, especiais, magia, projeteis


def registra_todas(registra):
    for modulo in (corpo, cortes, projeteis, energia, elementos, magia, apoio, especiais):
        for nome, fn, tela, descricao, laco in modulo.REGISTRO:
            registra(nome, fn, tela, descricao, laco=laco)
