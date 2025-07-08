from typing import NewType, TypedDict, Dict, Union, Any, NamedTuple, List


class SXData(str):
    def __new__(cls, value: str):
        # Aqui você pode adicionar lógica de validação em tempo de execução
        # if not value.startswith("SX_"):
        # Exemplo de validação: todos os SX_aData devem começar com "SX_"
        # raise ValueError(f"SXaData must start with 'SX_'. Got: {value}")
        return super().__new__(cls, value)


class SrtData(str):
    def __new__(cls, value: str):
        # Aqui você pode adicionar lógica de validação em tempo de execução
        # if not value.startswith("SX_"):
        # Exemplo de validação: todos os SX_aData devem começar com "SX_"
        # raise ValueError(f"SXaData must start with 'SX_'. Got: {value}")
        return super().__new__(cls, value)


class IdData(str):
    def __new__(cls, value: str):
        # Aqui você pode adicionar lógica de validação em tempo de execução
        # if not value.startswith("SX_"):
        # Exemplo de validação: todos os SX_aData devem começar com "SX_"
        # raise ValueError(f"SXaData must start with 'SX_'. Got: {value}")
        return super().__new__(cls, value)

    # def get_prefix(self) -> str:
    #     """Retorna o prefixo 'SX_' se presente."""
    #     if self.startswith("SX_"):
    #         return "SX_"
    #     return ""


SX_aData = SXData
SX_bData = SXData
RN1Data = IdData
RotaSumData = SrtData
FormatSumData = SrtData
EncamTypeData = NewType('EncamTypeData', str)
RotaData = SrtData
# FormatData = SrtData
IdSupCod_CNL_aIdTipoOrigIdEncamData = SrtData
IdTipoOrigData = IdData
IdTipoDestData = IdData
Idtipo_servData = IdData
IdtarifacaoData = IdData
IdabrangenciaData = IdData
Idtrunk_typeData = IdData
Idtech_classData = IdData
Idencam_typeData = IdData
IdcenarioData = IdData
IdcenData = IdData
IdorigemData = IdData
IdportadoData = IdData
IdsentidoData = IdData
IdacbData = IdData
IderrorData = IdData


class EncamHeaderData(TypedDict):
    dc: str
    dt_ger: str
    dt_upd: str
    idUser: int
    Matricula: str
    Colaborador: str


class EncamDataData(TypedDict):
    sup: dict
    rn1: dict
    cnl: dict
    al: dict
    grp_encam: dict
    encam: dict
    orig: dict
    sx: dict
    grafo: dict
    cgi: dict


class EncamDict_tipo_orig_Data(TypedDict):
    TipoOrig: str
    SMP: int
    STFC: int
    VoLTE: int
    TrType: str
    Traducao: str
    idTarifacao: str
    TipoServ: str


class EncamDict_tipo_dest_Data(TypedDict):
    TipoDest: str
    isOrgin: int
    SMP: int
    STFC: int


class EncamDict_tipo_serv_Data(TypedDict):
    TipoSrv: str
    TipoServico: str
    Tarifa: str
    idTarifacao: int
    erPrefixo: str


class EncamDict_tarifacao_Data(TypedDict):
    Tarif: str
    Tarifacao: str


class EncamDict_abrangencia_Data(TypedDict):
        Abrangencia: str
        Abrg: str
        Ativo: int
        Ord: int


class EncamDict_tech_class_Data(TypedDict):
    idTech: int
    Tech: str
    Class: str
    ACC: int
    GTW: int
    CL4: int
    CL5: int
    PABX: int


class EncamDict_encam_type_Data(TypedDict):
    Quando: str
    Transbordo: int


class EncamDict_cenario_Data(TypedDict):
    Cenario: str
    idCen: int
    TipoCen: str
    EntregaTim: int
    ACB: int
    idACB: int
    idCenarioRed: int


class EncamDict_cen_Data(TypedDict):
    Cen: str
    Ativo: int
    LD: int
    idOpeOrig: int
    idOpeDest: int
    idTipoOrig: str
    idTipoDest: str
    Descr: str
    DtUpdate: str


class EncamDict_origem_Data(TypedDict):
    Origem: str
    OLO: int
    ROAM: str
    OrdSMP: int
    OrdSTFC: int
    Ord: int
    idGrp: str
    idTipoOrig: int
    idTechClass: int
    idSX: int
    Descr: str
    DtUpdate: str


class EncamDict_portado_Data(TypedDict):
    ...


class EncamDict_sentido_Data(TypedDict):
    ...


class EncamDict_acb_Data(TypedDict):
    ...


class EncamDict_error_Data(TypedDict):
    ...


class EncamDictData(TypedDict):
    tipo_orig: Dict[IdTipoOrigData, EncamDict_tipo_orig_Data]
    tipo_dest: List[EncamDict_tipo_dest_Data]
    tipo_serv: Dict[Idtipo_servData, EncamDict_tipo_serv_Data]
    tarifacao: Dict[IdtarifacaoData, EncamDict_tarifacao_Data]
    abrangencia: Dict[IdabrangenciaData, EncamDict_abrangencia_Data]
    trunk_type: Dict[Idtrunk_typeData, str]
    tech_class: Dict[Idtech_classData, EncamDict_tech_class_Data]
    encam_type: Dict[Idencam_typeData, EncamDict_encam_type_Data]
    cenario: Dict[IdcenarioData, EncamDict_cenario_Data]
    cen: Dict[IdcenData, EncamDict_cen_Data]
    origem: Dict[IdorigemData, EncamDict_origem_Data]
    tr_types: Dict[str, str]
    portado: Dict[IdportadoData, EncamDict_portado_Data]
    sentido: Dict[IdsentidoData, EncamDict_sentido_Data]
    acb: Dict[IdacbData, EncamDict_acb_Data]
    error: Dict[IderrorData, EncamDict_error_Data]


class EncamForwardingEncamTData(List):
    carga: str
    formato: str


class EncamForwardingEncamSupData(List):
    error: int
    ord_encam: int


class EncamForwardingEncamData(TypedDict):
    detail: Dict[
        EncamTypeData, Dict[
            RotaData, EncamForwardingEncamTData
        ]
    ]
    sup_encam: Dict[
        IdSupCod_CNL_aIdTipoOrigIdEncamData, EncamForwardingEncamSupData
    ]


class EncamData(TypedDict):
    version: str
    type: str
    header: EncamHeaderData
    data: EncamDataData
    dict_dc: EncamDictData
    forwarding: Dict[
        SX_aData, Dict[
            SX_bData, Dict[
                RN1Data, Dict[
                    RotaSumData, Dict[
                        FormatSumData, EncamForwardingEncamData
                    ]
                ]
            ]
        ]
    ]
    # Dict[SX_aData,EncamForwardingSXaData]


c: EncamData = {
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
            "idSup": {
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
                    "Cod_CNL": {
                        "idTipoOrig": [
                            "CN_b",
                            "idAL_b",
                            "idPortado",
                            "AbrCN,idTipoOrig,idTipoDest,idACB,RN1_b",
                            "traducao"
                        ]
                    }
                }
            }
        },
        "rn1": {
            "RN1": {
                "RNH": "string",
                "RN1_Grp": "integer",
                "Prestadora": "string",
                "OLO": "string",
                "CNPJ": "string"
            }
        },
        "cnl": {
            "Cod_CNL": {
                "Sigla_CNL": "string",
                "Municipio": "string",
                "isCoverSMP": "0,1",
                "idAL": "idAL"
            }
        },
        "al": {
            "idAL": {
                "AL": "AL",
                "ROP": "ROP",
                "CN": "CN",
                "UF": "UF",
                "Reg": "REG",
                "Regiao": "integer",
                "isCoverSTFC": "0,1"
            }
        },
        "grp_encam": {
            "CN": {
                "idAL": {
                    "idPortado": {
                        "AbrCN,idTipoOrig,idTipoDest,idACB,RN1": {
                            "AbrCN": "AbrCN",
                            "idTipoOrig": "idTipoOrig",
                            "idTipoDest": "idTipoDest",
                            "idACB": "idACB",
                            "RN1": "RN1",
                            "hop": "integer",
                            "encam": {
                                "idEncam": [
                                    "idOrigem",
                                    "idCenario",
                                    "idTrunkType"
                                ]
                            }
                        }
                    }
                }
            }
        },
        "encam": {
            "idEncam": {
                "summary": {
                    "Rota": "rota_summary",
                    "Carga": "carga_summary",
                    "Formato": "formato_summary"
                },
                "rotas": {
                    "SX": {
                        "id_encam_type": {
                            "rota": [
                                "carga",
                                "formato"
                            ]
                        }
                    }
                }
            }
        },
        "orig": {
            "idTipoOrig": {
                "ids": [
                    "idTechClass_sx_main,idTechClass_sx_main,...",
                    "idTechClass_delivery,idTechClass_delivery,..."
                ],
                "delivery": [
                    "SX"
                ],
                "sx": {
                    "CN": {
                        "idOrigem": [
                            "SX"
                        ]
                    }
                }
            }
        },
        "sx": {
            "SX": [
                "idSX",
                "idDevice",
                "idTech",
                "idTechClass"
            ]
        },
        "grafo": {
            "SX_A": {
                "SX_B": {
                    "idTrunkType": {
                        "idSentido": {
                            "id_encam_type": {
                                "Rota": None
                            }
                        }
                    }
                }
            }
        },
        "cgi": {
            "Reg": {
                "Sigla_CNL": {
                    "Cod_CNL": {
                        "ERN": {
                            "G": {
                                "EA": {
                                    "EndId": {
                                        "SiteId": {
                                            "CGI": {
                                                "Celula": {
                                                    "EC": {
                                                        "ERIND": {
                                                            "idDevice": "Device"
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
    "dict_dc": {},
    "forwarding": {
        "SX_A": {
            "SX_B": {
                "RN1": {
                    "rota_summary": {
                        "formato_summary": {
                            "detail": {
                                "encam_type": {
                                    "rota": [
                                        "carga",
                                        "Formato"
                                    ]
                                }
                            },
                            "sup_encam": {
                                "idSup,Cod_CNL_a,idTipoOrig,idEncam": [
                                    "error",
                                    "ord"
                                ]
                            }
                        }
                    }
                }
            }
        }
    }
}

print(c["forwarding"]['SX_A']['SX_B']['RN1']['rota_summary']
      ['formato_summary']["detail"]['encam_type']['rota'])
