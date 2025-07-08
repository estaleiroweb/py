
from typing import TypedDict, Union, Any
from dc_tiping import EncamData
# Nível mais interno ou tipos de valor final


class ValueSubparamA(TypedDict):
    value1: str
    value2: int


class ValueSubparamB(TypedDict):
    another_value: bool


class FinalConfig(TypedDict):
    url: str
    timeout: int

# Níveis intermediários


class Subparam(TypedDict):
    subparamA: ValueSubparamA
    subparamB: ValueSubparamB


class AnotherLevel(TypedDict):
    final_config: FinalConfig

# Nível mais externo


class CGIData(TypedDict):
    param1: Subparam
    param2: AnotherLevel
    # Adicione mais chaves e tipos conforme a sua estrutura real


class MyClass:
    # Assumindo que self.data é um dict genérico inicialmente
    data: EncamData

    def __init__(self, data: dict[str, Any]):
        self.data = data
        
    def get_timeout(self):
        return self.data['dict']


glossary = {
    "<idSup>": "integer id do SUP (Serviço de Utilização Pública)",
    "<Cod_CNL>": "integer código da localidade/cidade",
    "<Sigla_CNL>": "string sigla da localidade/cidade (CNL) [A-Z]{3,4}",
    "<idAL>": "integer id da área local",
    "<RN1>": "integer código da prestadora na Anatel",
    "<OLO>": "string que pode ser OI, CLARO, TIM, VIVO,",
    "<ROP>": "integer código de encaminhamento de área local dentro da empresa",
    "<CN>": "integer Código Nacional (DDD) [1-9]{2}",
    "<UF>": "string sigla do estado (UF) Unidade Federativa [A-Z]{2}",
    "<REG>": "string sigla do Regiões (Reg) [A-Z]{3}",
    "<idREG>": "integer id da região (idReg) [1-5] (dict contexto regiao)",
    "<idTrunkType>": "integer id do tipo de rota interna (dict contexto trunk_type)",
    "<idTipoOrig>": "integer id que pode ter apenas os valores 1,2,3,4,5 (dict contexto tipo_orig)",
    "<TipoOrig>": "string relativo ao idTipoOrig SMP, STFC, VoLTE, ....",
    "<idTipoDest>": "integer id que pode ter apenas os valores 0,1,2,3,4 (dict contexto tipo_dest)",
    "<idPortado>": "integer id que pode ser 1,2,3 (dict contexto portado) se é portado ou não ou ambos",
    "<idSentido>": "integer id que pode ser 1,2,3 (dict contexto sentido) se o sentido é IN ou OUT ou ambos",
    "<idCenario>": "integer id do cenário (dict contexto cenario)",
    "<idOrigem>": "integer id da origem do encaminhamento (dict contexto origem)",
    "<idTechClass>": "integer id do Sub Tecnologia do SX (dict contexto tech_class) que esse relaciona com idTech",
    "<idTech>": "integer id da Tecnologia do SX que esse relaciona com o idTechClass",
    "<id_encam_type>": "integer id do tipo de encaminhamento (dict contexto encam_type) >10 é transbordo <=10 sem transbordo, 1 é o Ativo demais são tipos diferentes de redundância",
    "<idACB>": "integer que pode ser 1,2,3 se a (dict contexto acb) se é a cobra ou não ou ambos",
    "<traducao>": "string numérico de tradução do número de telefone, pode ser vazio",
    "<idEncam>": "integer id do encaminhamento",
    "<SX>": "string equipamento que pode ser ZSNE09, ZSPO09, VSC1S, VSC2S...",
    "<idSX>": "integer id do equipamento SX relacionado com Roboc",
    "<idDevice>": "integer id do dispositivo relação com eVoice",
    "<list_SX>": "array lista de equipamentos que podem ser [ZSNE09, ZSPO09, VSC1S, VSC2S...] ou []",
    "<rota>": "string rota de encaminhamento, pode ser vazio",
    "<formato>": "string formato de encaminhamento, pode ser vazio",
    "<carga>": "integer carga de encaminhamento, pode ser vazio",
    "<AbrCN>": "integer que pode ser 0,1 se a abrangencia é por CN ou não",
    "<grp>": "string composição de '<AbrCN>,<idTipoOrig>,<idTipoDest>,<idACB>,<RN1>' para agrupar encaminhamentos",
    "<error>": "integer código de erro, se houver, 0 se não houver erro (dict contexto error) definido com pesos em binário"
}
my_config_data = {
    "version": "^\\d+\\.\\d+\\.\\d+$",
    "type": "SUP,IND,DIR",
    "header": {
        "dc": "string",
        "dt_ger": "string",
        "dt_upd": "string",
        "idUser": "integer",
        "Matricula": "^[FT]\\d{7}$",
        "Colaborador": "string"
    },
    "data": {
        "sup": {
            "<idSup>": {
                "Servico": "integer",
                "Emerg": "integer",
                "Servico_Descricao": "string",
                "idTipoSrv": "integer",
                "RN1": "integer",
                "OLO": "string",
                "Prestadora": "string",
                "TrType_Mov": "string",
                "TrType_Fixa": "string",
                "TrType_VoLTE": "string",
                "Traducao_Mov": "string",
                "Traducao_Fixa": "string",
                "Traducao_VoLTE": "string",
                "idAbrangencia": "integer",
                "id": "integer",
                "idTarifacao_Movel": "integer",
                "idTarifacao_Fixa": "integer",
                "idTarifacao_VoLTE": "integer",
                "Remuneracao": "integer",
                "Cobertura": "integer",
                "Intelig": "integer",
                "Data_ConfCall": "date",
                "Check_ConfCall": "integer",
                "Data_Solicitacao": "date",
                "Data_Meta_Implantacao": "date",
                "Data_Envio": "date",
                "Doc_Prestadora": "string",
                "ValidacaoData": "date",
                "ValidacaoObs": "string",
                "Obs": "string",
                "idUser": "integer",
                "Matricula": "string",
                "Colaborador": "string",
                "DtUpdate": "datetime",
                "AbrCN": "integer",
                "cnl": {
                    "<Cod_CNL>": {
                        "<idTipoOrig>": [
                            "<CN_b>",
                            "<idAL_b>",
                            "<idPortado>",
                            "<AbrCN>,<idTipoOrig>,<idTipoDest>,<idACB>,<RN1_b>",
                            "<traducao>"
                        ]
                    }
                }
            }
        },
        "rn1": {
            "<RN1>": {
                "RNH": "string",
                "RN1_Grp": "integer",
                "Prestadora": "string",
                "OLO": "string",
                "CNPJ": "string"
            }
        },
        "cnl": {
            "<Cod_CNL>": {
                "Sigla_CNL": "string",
                "Municipio": "string",
                "isCoverSMP": "0,1",
                "idAL": "<idAL>"
            }
        },
        "al": {
            "<idAL>": {
                "AL": "<AL>",
                "ROP": "<ROP>",
                "CN": "<CN>",
                "UF": "<UF>",
                "Reg": "<REG>",
                "Regiao": "integer",
                "isCoverSTFC": "0,1"
            }
        },
        "grp_encam": {
            "<CN>": {
                "<idAL>": {
                    "<idPortado>": {
                        "<AbrCN>,<idTipoOrig>,<idTipoDest>,<idACB>,<RN1>": {
                            "AbrCN": "<AbrCN>",
                            "idTipoOrig": "<idTipoOrig>",
                            "idTipoDest": "<idTipoDest>",
                            "idACB": "<idACB>",
                            "RN1": "<RN1>",
                            "hop": "integer",
                            "encam": {
                                "<idEncam>": [
                                    "<idOrigem>",
                                    "<idCenario>",
                                    "<idTrunkType>"
                                ]
                            }
                        }
                    }
                }
            }
        },
        "encam": {
            "<idEncam>": {
                "summary": {
                    "Rota": "<rota_summary>",
                    "Carga": "<carga_summary>",
                    "Formato": "<formato_summary>"
                },
                "rotas": {
                    "<SX>": {
                        "<id_encam_type>": {
                            "<rota>": [
                                "<carga>",
                                "<formato>"
                            ]
                        }
                    }
                }
            }
        },
        "orig": {
            "<idTipoOrig>": {
                "ids": [
                    "<idTechClass_sx_main>,<idTechClass_sx_main>,...",
                    "<idTechClass_delivery>,<idTechClass_delivery>,..."
                ],
                "delivery": [
                    "<SX>"
                ],
                "sx": {
                    "<CN>": {
                        "<idOrigem>": [
                            "<SX>"
                        ]
                    }
                }
            }
        },
        "sx": {
            "<SX>": [
                "<idSX>",
                "<idDevice>",
                "<idTech>",
                "<idTechClass>"
            ]
        },
        "grafo": {
            "<SX_A>": {
                "<SX_B>": {
                    "<idTrunkType>": {
                        "<idSentido>": {
                            "<id_encam_type>": {
                                "<Rota>": None
                            }
                        }
                    }
                }
            }
        },
        "cgi": {
            "<Reg>": {
                "<Sigla_CNL>": {
                    "<Cod_CNL>": {
                        "<ERN>": {
                            "<G>": {
                                "<EA>": {
                                    "<EndId>": {
                                        "<SiteId>": {
                                            "<CGI>": {
                                                "<Celula>": {
                                                    "<EC>": {
                                                        "<ERIND>": {
                                                            "<idDevice>": "<Device>"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "dict_dc":{},
    "forwarding": {
        "<SX_A>": {
            "<SX_B>": {
                "<RN1>": {
                    "<rota_summary>": {
                        "<formato_summary>": {
                            "detail": {
                                "<encam_type>": {
                                    "<rota>": [
                                        "<carga>",
                                        "<Formato>"
                                    ]
                                }
                            },
                            "sup_encam": {
                                "<idSup>,<Cod_CNL_a>,<idTipoOrig>,<idEncam>": [
                                    "<error>",
                                    "<ord>"
                                ]
                            }
                        }
                    }
                }
            }
        }
    }
}

obj = MyClass(my_config_data)
print(obj.data)
