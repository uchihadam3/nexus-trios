"""
Famílias novas de efeitos (100+), desenhadas em Python como as primeiras.

Cada módulo temático tem uma lista REGISTRO de (nome, função, tela,
descrição, laço). generate_families.py registra todas junto das originais;
saem na mesma pasta (public/assets/vfx/familias), no mesmo formato.
"""
from . import apoio, assinaturas, corpo, cortes, elementos, energia, especiais, invocacoes, jeitos, magia, projeteis
from . import cloud_e_dk, madara, naruto_ikki_luffy, ninjas_e_detetives, aang_sakura, aiolia_arthas, ciclope_shaka_mummra, sasuke_aranha_trunks_kuririn, omniman_guts_rick, rodada01, rodada02, rodada03, rodada04, rodada05, rodada06, rodada07, rodada08, rodada09, rodada10, rodada11, rodada12, rodada13, rodada14, rodada15, rodada16, rodada17, rodada18, rodada19, rodada20, unicas_a, unicas_b, unicas_c, rodada06, renascer_proprio, reviver_proprio, charizard_megaman, hulk, piccolo, superman_hyoga, toph_e_gon, viagens
from . import basicos_a, basicos_b, basicos_c, basicos_d, basicos_e, basicos_f, basicos_g, basicos_h, basicos_i, basicos_j, basicos_k, basicos_l, basicos_m, basicos_n, basicos_o, basicos_p, basicos_q, basicos_r, basicos_s, basicos_t


def registra_todas(registra):
    for modulo in (corpo, cortes, projeteis, energia, elementos, magia, apoio, especiais, invocacoes, assinaturas, jeitos,
                   basicos_a, basicos_b, basicos_c, basicos_d, basicos_e, basicos_f, basicos_g, basicos_h, basicos_i, basicos_j, basicos_k, basicos_l, basicos_m, basicos_n, basicos_o, basicos_p, basicos_q, basicos_r, basicos_s, basicos_t, madara, viagens, ninjas_e_detetives, cloud_e_dk, naruto_ikki_luffy, toph_e_gon, piccolo, charizard_megaman, superman_hyoga, hulk, aiolia_arthas, aang_sakura, ciclope_shaka_mummra, sasuke_aranha_trunks_kuririn, omniman_guts_rick, rodada01, rodada02, rodada03, rodada04, rodada05, rodada06, rodada07, rodada08, rodada09, rodada10, rodada11, rodada12, rodada13, rodada14, rodada15, rodada16, rodada17, rodada18, rodada19, rodada20, unicas_a, unicas_b, unicas_c, rodada06, renascer_proprio, reviver_proprio):
        for nome, fn, tela, descricao, laco in modulo.REGISTRO:
            registra(nome, fn, tela, descricao, laco=laco)
