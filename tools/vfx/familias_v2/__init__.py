"""
Famílias novas de efeitos (100+), desenhadas em Python como as primeiras.

Cada módulo temático tem uma lista REGISTRO de (nome, função, tela,
descrição, laço). generate_families.py registra todas junto das originais;
saem na mesma pasta (public/assets/vfx/familias), no mesmo formato.
"""
from . import apoio, assinaturas, corpo, cortes, elementos, energia, especiais, invocacoes, jeitos, magia, projeteis
from . import madara, viagens
from . import basicos_a, basicos_b, basicos_c, basicos_d, basicos_e, basicos_f, basicos_g, basicos_h, basicos_i, basicos_j


def registra_todas(registra):
    for modulo in (corpo, cortes, projeteis, energia, elementos, magia, apoio, especiais, invocacoes, assinaturas, jeitos,
                   basicos_a, basicos_b, basicos_c, basicos_d, basicos_e, basicos_f, basicos_g, basicos_h, basicos_i, basicos_j, madara, viagens):
        for nome, fn, tela, descricao, laco in modulo.REGISTRO:
            registra(nome, fn, tela, descricao, laco=laco)
