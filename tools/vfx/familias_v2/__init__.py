"""
Famílias novas de efeitos (100+), desenhadas em Python como as primeiras.

Cada módulo temático tem uma lista REGISTRO de (nome, função, tela,
descrição, laço). generate_families.py registra todas junto das originais;
saem na mesma pasta (public/assets/vfx/familias), no mesmo formato.
"""
from . import apoio, assinaturas, corpo, cortes, elementos, energia, especiais, invocacoes, jeitos, magia, projeteis
from . import cloud_e_dk, madara, naruto_ikki_luffy, ninjas_e_detetives, aang_sakura, aiolia_arthas, ciclope_shaka_mummra, sasuke_aranha_trunks_kuririn, omniman_guts_rick, rodada01, charizard_megaman, hulk, piccolo, superman_hyoga, toph_e_gon, viagens
from . import basicos_a, basicos_b, basicos_c, basicos_d, basicos_e, basicos_f, basicos_g, basicos_h, basicos_i, basicos_j


def registra_todas(registra):
    for modulo in (corpo, cortes, projeteis, energia, elementos, magia, apoio, especiais, invocacoes, assinaturas, jeitos,
                   basicos_a, basicos_b, basicos_c, basicos_d, basicos_e, basicos_f, basicos_g, basicos_h, basicos_i, basicos_j, madara, viagens, ninjas_e_detetives, cloud_e_dk, naruto_ikki_luffy, toph_e_gon, piccolo, charizard_megaman, superman_hyoga, hulk, aiolia_arthas, aang_sakura, ciclope_shaka_mummra, sasuke_aranha_trunks_kuririn, omniman_guts_rick, rodada01):
        for nome, fn, tela, descricao, laco in modulo.REGISTRO:
            registra(nome, fn, tela, descricao, laco=laco)
