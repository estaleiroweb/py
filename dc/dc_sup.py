#!/bin/env python
# /c/AppData/Code/venv/py/dc/dc.py
import json
import pandas as pd
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo
from typing import Callable
import os

class DC_SUP:
    def __init__(self):
        self.path=os.path.dirname(os.path.abspath(__file__))
        self.dc_dict = self.get_json_file(f"{self.path}/data/dict-1.0.0.json")
        self.df:dict[str,dict[str,pd.DataFrame]]={} # Reg,[header,encam,cgi],pd.DataFrame

        self.data_extract_encam(self.get_json_file(f"{self.path}/data/encam.json"))
        self.data_extract_cgi(self.get_json_file(f"{self.path}/data/cgi.json"))
        
        sheets={
            'header':{
                'title':'CAPA',
                'fn_format':self.excel_format_capa,
                },
            'encam':{
                'title':'SERVICOS',
                'fn_format':self.excel_insert_table,
                },
            'cgi':{
                'title':'CELLS CS',
                'fn_format':self.excel_insert_table,
                },
        }
        
        for reg in self.df:
            self.wb = self.excel_create_workbook()
            for sheet in self.df[reg]:
                df_item=self.df[reg][sheet]
                if not len(df_item):
                    print(f"{reg}:{sheet}: Nenhum dado encontrado")
                    continue

                conf=sheets[sheet]
                title=sheets[sheet]['title']
                fn_format=sheets[sheet]['fn_format']
                
                ws=self.convert_to_excel(title,df_item)
                fn_format(title,ws, df_item)
                self.show_done(title,df_item)

            self.excel_save(f"{self.path}/xlsx/dc_{reg}.xlsx")

    def data_extract_encam(self,json_dict:dict[str,dict[str,dict[str,dict[str,dict[str,dict]]]]]):
        # dict[str,dict]
        # Origem,Abrangencia,Servico,Tipo Serv,Traducao,Formato OLO,Tipo TR,Tarifacao,RN2,ROP,AL,Central Origem,Central Destino,Rota Destino,Formato Envio,CN_a,Cod_CNL_a,CNL_a,AL_a,UF_a,Municipio_a,Obs
        if not json_dict: return
        
        data:dict[str,list] = {}
        arr_error:dict=self.dc_dict['error']
        
        for sx_a, sx_b_data in json_dict['forwarding'].items():
            print(f'{"":<{2}}- sx_a: {sx_a}')
            for sx_b, rn1_data in sx_b_data.items():
                print(f'{"":<{4}}- sx_b: {sx_b}')
                for rn1, rota_summary_data in rn1_data.items():
                    print(f'{"":<{5}}- rn1: {rn1}')
                    for rota_summary, formato_summary_data in rota_summary_data.items():
                        print(f'{"":<{8}}- rota_summary: {rota_summary}')
                        for formato_summary, traducao_data in formato_summary_data.items():
                            print(f'{"":<{10}}- formato_summary: {formato_summary}')
                            for traducao, encam_data in traducao_data.items():
                                print(f'{"":<{12}}- traducao: {traducao} (ord: {encam_data['ord']})')

                                if encam_data['ord']==0: tipo_ord='Acesso'
                                elif encam_data['ord']==-1: tipo_ord='OLO'
                                else:
                                    tipo_ord='Rotas Internas'
                                    continue
                                
                                # print(encam_data.keys()); print('-'*80)
                                arr_obs=[]
                                arr_obs.append(f'# {encam_data['ord']} {tipo_ord}')
                                
                                error=encam_data['error']
                                mark=''
                                if error: 
                                    mark='*'
                                    error_str=arr_error[f'{error}']['desc']
                                    arr_obs.append('ERROR: '+ error_str)
                                    print(f'{"":<{14}}ERROR: {error}-{error_str}')
                                obs:str=' \n'.join(arr_obs)
                                    
                                sup_data:dict=encam_data['sup']
                                orig_data:dict=encam_data['orig']
                                # trunk_type_data:dict=encam_data['trunk_type']
                                rotas_data:dict[str,dict]=encam_data['rotas']
                                local_data:dict[str,dict]=encam_data['local']
                                
                                if rotas_data:
                                    for id_encam_type, rotas_data_det in rotas_data.items():
                                        print(f'{"":<{14}}- id_encam_type: {id_encam_type}')
                                        
                                        arr_rota,arr_carga,arr_formato=[],[],[]
                                        for rota, arr_rota_det in rotas_data_det.items():
                                            print(f'{"":<{16}}- rota: {rota}')
                                            if not rota: continue
                                            carga=arr_rota_det[0]
                                            formato=arr_rota_det[1]
                                            arr_rota.append(rota)
                                            arr_carga.append(f'{carga}' if carga else '-')
                                            arr_formato.append(f'{formato}' if formato else '-')
                                        
                                        arr_encam_type:dict=self.dc_dict['encam_type'][id_encam_type]
                                        encam_type:str=arr_encam_type['Quando']+(' Transbordo' if arr_encam_type['Transbordo'] else ' Atual')
                                        print([arr_rota,arr_carga,arr_formato])
                                        arr_obs.append(f'- {encam_type}: {'/'.join(arr_rota)}({'/'.join(arr_carga)})[{';'.join(arr_formato)}]')
                                    
                                for idSup, servico in sup_data.items():
                                    print(f'{"":<{14}}- idSup[{idSup}]: servico {servico}')
                                    sup:dict=json_dict['data']['sup'][idSup]
                                    idAbrangencia:int=sup['idAbrangencia']
                                    idTipoSrv:int=sup['idTipoSrv']
                                    abrangencia:str=self.dc_dict['abrangencia'][f'{idAbrangencia}']['Abrangencia']
                                    tipo_serv:str=self.dc_dict['tipo_serv'][f'{idTipoSrv}']['TipoSrv']
                                    
                                    print(f'{"":<{16}}idAbrangencia: {idAbrangencia}-{abrangencia}')
                                    print(f'{"":<{16}}idTipoSrv....: {idTipoSrv}-{tipo_serv}')
                                    
                                    for idTipoOrig, tipoOrig in orig_data.items():
                                        print(f'{"":<{16}}- tipoOrig[{idTipoOrig}]: {tipoOrig}')
                                        arr_tipoOrig:dict=self.dc_dict['tipo_orig'][idTipoOrig]
                                        TrType:str=sup[arr_tipoOrig['TrType']]
                                        idTarifacao:int=sup[arr_tipoOrig['idTarifacao']]
                                        tarifacao=self.dc_dict['tarifacao'][f'{idTarifacao}']['Tarif']
                                        tipo_tr:str=self.dc_dict['tr_types'][TrType]
                                        print(f'{"":<{18}}idTarifacao: {idTarifacao}-{tarifacao}')
                                        print(f'{"":<{18}}TrType.....: {TrType}-{tipo_tr}')
                                        
                                        arr_uf,arr_cn,arr_al,arr_cnl,arr_rop=[],[],[],[],[]
                                        for reg, uf_data in local_data.items():
                                            print(f'{"":<{18}}- reg: {reg}')
                                            # for uf, cn_data in uf_data.items():
                                            #     print(f'{"":<{18}}- uf: {uf}')
                                                # for cn, al_data in cn_data.items():
                                                #     print(f'{"":<{18}}- idAL: {idAL}')
                                                    # for idAL, idAL_data in al_data.items():
                                                    #     print(f'{"":<{18}}- idAL: {idAL}')
                                                        # for cod_cnl, Sigla_CNL in idAL_data.items():
                                                        #     print(f'{"":<{18}}- cod_cnl: {cod_cnl}')
                                            data_item={
                                                'Origem': mark+tipoOrig,
                                                'Abrangencia': abrangencia, # arr_abrangencia
                                                'Servico': servico,
                                                'Tipo Serv': tipo_serv,
                                                'Traducao': traducao,
                                                'Formato OLO': TrType,
                                                'Tipo TR': tipo_tr,
                                                'Tarifacao': tarifacao,
                                                'RN1': rn1,
                                                'ROP': [],
                                                'AL': [],
                                                'Central Origem': sx_a,
                                                'Central Destino': sx_b,
                                                'Rota Destino': rota_summary,
                                                'Formato Envio': formato_summary,
                                                'CN_a': [],
                                                'Cod_CNL_a': [],
                                                'CNL_a': [],
                                                'AL_a': [],
                                                'UF_a': [],
                                                'Municipio_a': [],
                                                'Obs': obs,
                                            }
                                            if not data.get(reg): data[reg]=[]
                                            data[reg].append(data_item)
        for reg in data:
            if not self.df.get(reg): self.df[reg]={}
            self.df[reg]['encam']=self.group_encam_data(pd.DataFrame(data[reg]))

    def data_extract_cgi(self,json_dict:dict[str,dict[str,dict[str,dict[str,dict[str,dict[str,dict[str,dict[str,dict[str,dict[str,dict[str,dict[str,dict]]]]]]]]]]]]):
        """
        Extrai dados do JSON CGI em formato tabular
        
        - from: Sigla_CNL,Cod_CNL,ERN,G,EA,EndId,SiteId,CGI,Celula,EC,ERIND,idDevice=Device
        - to: CGI,RAT=G,Sigla_CNL,EC,ERN,Devices order(RAT, Sigla_CNL) 
        """
        
        if not json_dict: return
        
        for reg, sigla_cnl_data in json_dict.items():
            data = []
            for sigla_cnl, cnl_data in sigla_cnl_data.items():
                # print(f'{"":<{2}}- sigla_cnl: {sigla_cnl}')
                for cod_cnl_erb, ea_data in cnl_data.items():
                    # print(f'{"":<{4}}- cod_cnl_erb: {cod_cnl_erb}')
                    for ern, endid_data in ea_data.items():
                        # print(f'{"":<{6}}- ern: {ern}')
                        for g, cnl_data in endid_data.items():
                            # print(f'{"":<{8}}- g: {g}')
                            for ea, endid_data in cnl_data.items():
                                # print(f'{"":<{10}}- ea: {ea}')
                                for endid, siteid_data in endid_data.items():
                                    # print(f'{"":<{12}}- endid: {endid}')
                                    for siteid, cgi_data in siteid_data.items():
                                        # print(f'{"":<{14}}- siteid: {siteid}')
                                        for cgi, celula_data in cgi_data.items():
                                            # print(f'{"":<{16}}- cgi: {cgi}')
                                            for celula, ec_data in celula_data.items():
                                                # print(f'{"":<{18}}- celula: {celula}')
                                                for ec, erind_data in ec_data.items():
                                                    # print(f'{"":<{20}}- ec: {ec}')
                                                    for erind, device_data in erind_data.items():
                                                        # print(f'{"":<{22}}- erind: {erind}')
                                                        for device_id, device_name in device_data.items():
                                                            # print(f'{"":<{24}}- device_id: {device_id}={device_name}')
                                                            data.append({
                                                                'Sigla_CNL': sigla_cnl,
                                                                'Cod_cnl_ERB': cod_cnl_erb,
                                                                'ERN': ern,
                                                                'G': g,
                                                                'EA': ea,
                                                                'EndId': endid,
                                                                'SiteId': siteid,
                                                                'CGI': cgi,
                                                                'Celula': celula,
                                                                'EC': ec,
                                                                'ERIND': erind,
                                                                'idDevice': device_id,
                                                                'Device': device_name
                                                            })
            if not self.df.get(reg): self.df[reg]={}
            self.df[reg]['cgi']=self.group_cgi_data(pd.DataFrame(data))

    def group_cgi_data(self,df:pd.DataFrame):
        """
        Agrupa dados por CGI, G, Sigla_CNL, EC, ERN
        Concatena os dispositivos em uma única coluna
        Ordena por G + Sigla_CNL
        """
        
        # Agrupar por CGI, G, Sigla_CNL, EC, ERN e concatenar os dispositivos
        grouped = df.groupby(['CGI', 'G', 'Sigla_CNL', 'EC', 'ERN']).agg({
            'Device': lambda x: ', '.join(sorted(set(x)))  # Remove duplicatas e ordena
        }).reset_index()
        grouped = grouped.rename(columns={'Device': 'Devices'})

        grouped['sort_key'] = grouped['G'].astype(str) + grouped['Sigla_CNL'].astype(str)
        grouped = grouped.sort_values('sort_key').drop('sort_key', axis=1)
        
        grouped = grouped[['CGI', 'G', 'Sigla_CNL', 'EC', 'ERN', 'Devices']]
        
        return grouped

    def group_encam_data(self,df:pd.DataFrame):
        return df

    def excel_format_capa(self,title:str, ws: Worksheet, df: pd.DataFrame):
        ...
    
    def excel_create_workbook(self,)->Workbook:
        wb = Workbook()
        
        # Remover sheet padrão
        wb.remove(wb.active)
        return wb
        
    def excel_save(self,excel_file):
        try:
            print(f"Salvar arquivo Excel: {excel_file}")
            self.wb.save(excel_file)
            print(f"- Criado com sucesso")
        except Exception as e:
            print('- '+str(e))

    def excel_insert_table(self,title:str, ws: Worksheet, df: pd.DataFrame):
        """
        Applies formatting to the Excel worksheet and converts the data range into an Excel Table.

        Args:
            ws (str): name of table.
            ws (Worksheet): The openpyxl worksheet object.
            df (pd.DataFrame): The pandas DataFrame containing the data.
        """
        table_range = f"A1:{chr(ord('A') + len(df.columns) - 1)}{len(df) + 1}"
        title=f"tbl_{title.replace(' ','_')}"
        # print(f'RANGE {title}: {table_range}')
        tab = Table(displayName=title, ref=table_range)

        # Define a style for the table (similar to Excel's built-in styles)
        # This style includes header row, total row (if needed), and banded rows/columns
        style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,showLastColumn=False, showRowStripes=True, showColumnStripes=False)
        tab.tableStyleInfo = style

        ws.add_table(tab)
        self.excel_worksheet_auto_size(ws)

    def excel_worksheet_format(self,ws:Worksheet, df:pd.DataFrame):
        """
        Aplica formatação ao worksheet Excel
        """
        # Cores para formatação
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        odd_row_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
        
        # Fonte para cabeçalho
        header_font = Font(color="FFFFFF", bold=True, size=12)
        
        # Fonte para dados
        data_font = Font(size=10)
        
        # Alinhamento
        center_alignment = Alignment(horizontal="center", vertical="center")
        
        # Formatação do cabeçalho
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = center_alignment
        
        self.excel_worksheet_auto_size(ws)
        
    def excel_worksheet_auto_size(self,ws:Worksheet):
        # Ajustar largura das colunas
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 20)  # Máximo de 20 caracteres
            ws.column_dimensions[column_letter].width = adjusted_width

    def convert_to_excel(self,title:str,df:pd.DataFrame)->Worksheet|None:
        """
        Função para converter dict list[dict] para Excel
        """
        
        ws_data:Worksheet = self.wb.create_sheet(title=title)
        for r in dataframe_to_rows(df, index=False, header=True):
            ws_data.append(r)
        return ws_data

    def show_done(self,title:str,df:pd.DataFrame):
        print(f"### {title}")
        # print(f"Colunas incluídas: {list(df.columns)}")
        # print("Preview dos primeiros 5 registros:")
        print(df.head().to_string(index=False))
        c=len(df)
        if c>5: print(f"...\nTotal de registros processados: {c}")
        print()

    def get_json_file(self,file)->dict:
        try:
            # Carregar dados JSON
            with open(file, 'r', encoding='utf-8') as file:
                cgi_data = json.load(file)
            return cgi_data
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {file}")
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON. Verifique se o arquivo está no formato correto.")
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
        return {}
                

if __name__ == "__main__":
    DC_SUP()