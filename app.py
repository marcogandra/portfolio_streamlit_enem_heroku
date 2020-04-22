# -*- coding: utf-8 -*-
"""Prevendo_nota_de_matematica_do_ENEM_2016.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1beela9VdVWEcLPEDXUoo7LmFzrmpYxdz

# Prevendo as notas de matemática do ENEM do ano de **2016**
"""

# importando as bibliotecas

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import pickle

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

sns.set(style='darkgrid')


# Fazendo cache dos dados para acelerar as próximas pesquisas.
@st.cache(allow_output_mutation=True)
def load_train():
    train = pd.read_csv('https://www.dropbox.com/s/7vexlzohz7j3qem/train.csv?raw=1', index_col=0)
    return train


# Fazendo cache dos dados para acelerar as próximas pesquisas.
@st.cache(allow_output_mutation=True)
def load_test():
    test = pd.read_csv('https://www.dropbox.com/s/dsgzaemaau9g5z0/test.csv?raw=1')
    return test


def main():
    def correlacao(data):
        plt.figure(figsize=(23, 8))
        sns.heatmap(train_df.corr(), annot=True, fmt='.2f')

    option = st.sidebar.selectbox("Menu: ",
                                  ['Análise', 'Predição', 'Sobre'])

    if option == 'Análise':
        train = load_train()
        test = load_test()

        st.image('https://raw.githubusercontent.com/nilsoncunha/portfolioweb/master/assets/img/posts/enem.jpg', use_column_width=True)
        st.title('Prevendo as notas de matemática do ENEM do ano de **2016**')

        # Minha apresentação
        st.markdown('>*Análise baseada em uma das atividades propostas pelo programa de aceleração da **Codenation** que participei no final de 2019, **Acelera Dev - Data Science**, em Belo Horizonte.*')
        st.markdown('>*Iniciei novamente a aceleração, que agora está sendo online, através do convite da própria **Codenation** com o intuito de auxiliar os participantes nos desafios, códigos e também '
                    'passar para eles a experiência que tive no presencial. Dessa vez vou apenas refazer a análise já feita anteriormente (se quiser verificar é só [clicar aqui](https://nilsoncunha.github.io/portfolioweb/prevendo-nota-de-matematica-do-enem-2016/)) '
                    'utilizando uma ferramenta apresentada pelo [Túlio Vieira](https://www.linkedin.com/in/tuliovieira/) (instrutor da aceleração), que é o [Streamlit](https://docs.streamlit.io/index.html)*.')

        # Apresentação da biblioteca
        st.markdown('>*Vou fazer aqui uma breve apresentação dessa biblioteca, que merece muitos aplaudos, antes de iniciar. Trazendo a definição do próprio Stramlit que se apresenta assim: '
                    '"O Streamlit é uma biblioteca Python de código aberto que **facilita** (e muito, esse por minha conta) a criação de aplicativos da Web personalizados e bonitos para aprendizado de máquina e ciência de dados...". '
                    'Com essa facilidade não precisamos ficar preocupado em utilizar html, css, javascript, etc., para montar uma interface ou ter que utilizar PowerPoit, ou outra coisa para apresentarmos ao negócio nossa análise. '
                    'Se antes realizávamos toda a documentação no próprio notebook, com o [Streamlit](https://docs.streamlit.io/index.html) conseguiremos fazer a documentação e deixar muito mais apresentável para as outras pessoas*')
        st.markdown('> *Podemos ver a diferença no qual fiz o [deploy](https://portfolio-enem.herokuapp.com/) no Heroku utilizando html e css.*')

        st.markdown('Então, fazendo o resumo da análise e demonstrando um pouco da ferramenta, Vamos lá! '
                    'Bases utilizadas de [treino](https://dl.dropbox.com/s/7vexlzohz7j3qem/train.csv?dl=0) e de [teste](https://dl.dropbox.com/s/dsgzaemaau9g5z0/test.csv?dl=0).')

        st.markdown('Com essa ferramenta conseguimos definir quantas linhas queremos visualizar em nosso dataframe, '
                    'podemos definir um *"slider"* e passar como parâmetro do "*head()*"')
        number_df = st.slider('Quantidade de linhas a serem exibidas:', min_value=5, max_value=15)
        st.dataframe(train.head(number_df))

        st.markdown('Tipo de dados da base (exibindo com o *"table"*): ')
        base = pd.DataFrame({'treino': train.dtypes.value_counts(),
                         'teste': test.dtypes.value_counts()})
        st.table(base)

        # Copiando o dataframe de treino e adicionando somente as colunas do dataframe de teste
        train_df = train.copy()
        train_df = train_df[test.columns]

        # salvando o index dos dados
        train_idx = train_df.shape[0]
        test_idx = test.shape[0]

        # Criando o dataframe com as features da variável train
        features_train = pd.DataFrame({'TP_PRESENCA_MT': train['TP_PRESENCA_MT'],
                                       'NU_NOTA_MT': train['NU_NOTA_MT']})

        train_df = pd.concat([train_df, features_train], axis=1)

        train_df = pd.concat(objs=[train_df, test], axis=0, sort=False).reset_index(drop=True)

        # Excluindo algumas features que não utilizaremos.
        train_df.drop(['NU_INSCRICAO','CO_PROVA_CN','CO_PROVA_CH','CO_PROVA_LC','CO_PROVA_MT',
                       'IN_BAIXA_VISAO','IN_CEGUEIRA','IN_DISCALCULIA','IN_DISLEXIA','IN_GESTANTE',
                       'IN_IDOSO','IN_SABATISTA','IN_SURDEZ','Q024','Q026','Q027'], axis=1, inplace=True)

        base = pd.DataFrame({'tipo': train_df.dtypes,
                             'nulos': train_df.isnull().mean(),
                             'size': (train_df.shape[0] - train_df.isnull().sum()),
                             'unicos': train_df.nunique()})

        base.index.name = 'coluna'
        base = base.reset_index()

        train_df.drop(['TP_DEPENDENCIA_ADM_ESC', 'TP_ENSINO'], axis=1, inplace=True)
        base.drop([10, 12], inplace=True)

        st.header('Analisando a base')
        st.markdown("Conseguimos ver que o estado de São Paulo teve o maior número de candidados, seguido por Ceará e Minas Gerais "
                    "*e também podemos utilizar o plotly facilmente*")

        data = [go.Bar(x=train_df['SG_UF_RESIDENCIA'].value_counts().index,
                       y=train_df['SG_UF_RESIDENCIA'].value_counts())]
        layout = go.Layout(title='Candidatos por estado')
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)

        st.markdown("Fazendo a verificação por sexo, conseguimos observar que as mulheres tiveram uma maior participação na prova. "
                    "*Nos gráficos, imagens, etc., o [Streamlit](https://docs.streamlit.io/index.html) nos dá a opção de expandi-lo, "
                    "colocando o ponteiro do mouse em cima é exibido uma seta no canto superior direito*")
        sns.catplot(x='SG_UF_RESIDENCIA', col='TP_SEXO', kind='count', height=6, aspect=1.2, data=train)
        st.pyplot()

        st.markdown("Observamos abaixo a distribuição de idade dos participantes. *Apenas adicionamos 'st.pyplot()' depois de montarmos o gráfico*")
        sns.distplot(train['NU_IDADE'])
        plt.xlabel('')
        plt.title("Distribuição por idade",
                  {'fontsize': 20})
        st.pyplot()

        train['NU_NOTA_PROVAS'] = (train['NU_NOTA_CH'] + train['NU_NOTA_CN'] + train['NU_NOTA_LC'] + train['NU_NOTA_MT']) / 4

        st.markdown('Na redação temos alguns pontos que são observados no caso de fugir ao tema, for anulada, entre outros. '
                    '*Tabela gerada com o "st.table()"*')

        redacao_index = train_df['TP_STATUS_REDACAO'].value_counts().index
        redacao_values = train_df['TP_STATUS_REDACAO'].value_counts().values
        redacao = pd.DataFrame({'tipo': redacao_index.astype(int), 'valores': redacao_values})
        redacao['descricao'] = redacao['tipo'].map({1: 'Sem problemas',
                                                2: 'Anulada',
                                                3: 'Cópia texto motivador',
                                                4: 'Em branco',
                                                5: 'Fere direitos autorais',
                                                6: 'Fuga ao tema',
                                                7: 'Não atendimento ao tipo',
                                                8: 'Texto insuficiente',
                                                9: 'Parte desconectada'})

        st.table(redacao[['valores', 'descricao']])
        data = [go.Bar(y=redacao['valores'],
                       x=redacao['descricao'])]

        layout = go.Layout(title='Situação da Redação')
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)

        st.markdown('Visualizando agora as notas das provas por estado. *Utilizando o plotly novamente que fica muito mais fácil para '
                    'identificar os valores.*')

        data = [go.Box(x=train['SG_UF_RESIDENCIA'],
                       y=train['NU_NOTA_PROVAS'])]

        layout = go.Layout(title='Nota das provas por estado')
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)

        data = go.Box(x=train_df['SG_UF_RESIDENCIA'],
                      y=train_df['NU_NOTA_REDACAO'])

        layout = go.Layout(title='Nota de redação por estado')
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig)


        st.markdown("Descrevendo agora o questionário socioeconômico. O título do gráfico corresponde as perguntas realizadas. "
                    "*Colocamos o 'plt.figure(figsize=(x, y))' antes de iniciar a construção do gráfico, com isso conseguimos "
                    "alterar o tamanho da imagem*")
        plt.figure(figsize=(18, 10))
        sns.boxplot(data=train, y='Q001', x='NU_NOTA_PROVAS', order='ABCDEFGH')
        plt.title('Até que série seu pai, ou o homem responsável por você, estudou?',
                  {'fontsize':15})
        plt.yticks(ticks=[0,1,2,3,4,5,6,7],
                   labels=['Nunca Estudou', 'Não Completou 4ª/5ª série', 'Não completou 8ª série',
                           'Não completou Ensino Médio', 'Completou Ensino Médio',
                           'Completou Faculdade', 'Completou Pós-Graduação', 'Não sei'])
        plt.xlabel("NOTA PROVA")
        plt.ylabel('')
        st.pyplot()

        sns.boxplot(data=train, y='Q002', x='NU_NOTA_PROVAS', order='ABCDEFGH')
        plt.title('Até que série sua mãe, ou a mulher responsável por você, estudou?',
                  {'fontsize':15})
        plt.yticks(ticks=[0,1,2,3,4,5,6,7],
                   labels=['Nunca Estudou', 'Não Completou 4ª/5ª série', 'Não completou 8ª série',
                           'Não completou Ensino Médio', 'Completou Ensino Médio',
                           'Completou Faculdade', 'Completou Pós-Graduação', 'Não sei'])
        plt.xlabel("NOTA PROVA")
        plt.ylabel('')
        st.pyplot()

        st.subheader("Tratando os dados e realizando a previsão")
        st.markdown("Depois dessas análises, chegou a hora de prepar os dados para a previsão. "
                    "Primeiro realizei o tratamento imputando o valor 0 (zero) na prova daqueles "
                    "candidatos que estavam com com status diferente de “1 = Presente na prova”. *Para exibir o código "
                    "que escrevi eu usei o st.echo() que insere uma notação e ao mesmo tempo executa o código. Bem "
                    "simples né!? (Exibindo apenas algumas linhas)*")

        with st.echo():
            train_df.loc[train_df['TP_PRESENCA_CH'] != 1, 'NU_NOTA_CH'] = train_df.loc[train_df['TP_PRESENCA_CH'] != 1, 'NU_NOTA_CH'].fillna(0)
            train_df.loc[train_df['TP_PRESENCA_CN'] != 1, 'NU_NOTA_CN'] = train_df.loc[train_df['TP_PRESENCA_CN'] != 1, 'NU_NOTA_CN'].fillna(0)
            train_df.loc[train_df['TP_PRESENCA_MT'] != 1, 'NU_NOTA_MT'] = train_df.loc[train_df['TP_PRESENCA_MT'] != 1, 'NU_NOTA_MT'].fillna(0)

        base[base.nulos > 0].sort_values(['nulos', 'coluna'])

        # Passando a lista de colunas para a variável
        colunas_base = base[base.nulos > 0].sort_values(['nulos', 'coluna'])['coluna'].tolist()

        # imputando o valor 0 para os candidatos que estão com o status diferente de "1 = Presente na prova"
        train_df.loc[train_df['TP_PRESENCA_CH'] != 1, 'NU_NOTA_CH'] = train_df.loc[train_df['TP_PRESENCA_CH'] != 1, 'NU_NOTA_CH'].fillna(0)
        train_df.loc[train_df['TP_PRESENCA_CN'] != 1, 'NU_NOTA_CN'] = train_df.loc[train_df['TP_PRESENCA_CN'] != 1, 'NU_NOTA_CN'].fillna(0)
        train_df.loc[train_df['TP_PRESENCA_MT'] != 1, 'NU_NOTA_MT'] = train_df.loc[train_df['TP_PRESENCA_MT'] != 1, 'NU_NOTA_MT'].fillna(0)
        train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_LC'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_LC'].fillna(0)

        train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_REDACAO'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_REDACAO'].fillna(0)
        train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP1'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP1'].fillna(0)
        train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP2'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP2'].fillna(0)
        train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP3'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP3'].fillna(0)
        train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP4'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP4'].fillna(0)
        train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP5'] = train_df.loc[train_df['TP_PRESENCA_LC'] != 1, 'NU_NOTA_COMP5'].fillna(0)

        # alterando o variável TP_SEXO
        train_df['TP_SEXO'] = train_df['TP_SEXO'].map({'M': 1, 'F': 0})

        label_encoder = LabelEncoder()
        train_df['Q001'] = label_encoder.fit_transform(train_df['Q001'])
        train_df['Q002'] = label_encoder.fit_transform(train_df['Q002'])
        train_df['Q006'] = label_encoder.fit_transform(train_df['Q006'])
        train_df['Q025'] = label_encoder.fit_transform(train_df['Q025'])
        train_df['Q047'] = label_encoder.fit_transform(train_df['Q047'])

        st.markdown("Exibindo o mapa de correlação novamente, temos agora novas _features_ com forte correlação.")

        st.pyplot(fig=correlacao(train_df))

        #train_df.drop(['SG_UF_RESIDENCIA', 'TP_SEXO', 'TP_COR_RACA', 'TP_NACIONALIDADE', 'TP_ST_CONCLUSAO', 'TP_ANO_CONCLUIU',
        #               'TP_LINGUA', 'TP_STATUS_REDACAO'],
        #              axis=1, inplace=True)


        ## Features que foram removidas para utilizar no modelo de deploy
        train_df.drop(['SG_UF_RESIDENCIA', 'TP_SEXO', 'TP_COR_RACA', 'TP_NACIONALIDADE', 'TP_ST_CONCLUSAO', 'TP_ANO_CONCLUIU',
                       'TP_LINGUA', 'TP_STATUS_REDACAO', 'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4',
                       'NU_NOTA_COMP5', 'Q001', 'Q002', 'Q006', 'Q025', 'Q047'],
                      axis=1, inplace=True)

        # Recuperando nosso dataset
        train = train_df.iloc[:train_idx]
        test = train_df.iloc[train_idx:]

        st.markdown('No desafio tinhamos que submeter um arquivo csv com a resposta do modelo treinado. '
                    'Nesse caso criei o pŕopio dataset de validação baseado nos dados de treino '
                    'e verifiquei como está a performance do modelo. *Utilizei st.echo() para exibir o código '
                    'e já executa-lo*')

        # Salvando a variável para realizar o treino futuramente e dividindo o dado de treino para validação
        with st.echo():
            target = train['NU_NOTA_MT']
            train.drop(['NU_NOTA_MT', 'TP_PRESENCA_MT'], axis=1, inplace=True)
            X_train, X_test, y_train, y_test = train_test_split(train, target, test_size=0.25, random_state=42)

        test.drop(['NU_NOTA_MT', 'TP_PRESENCA_MT'], axis=1, inplace=True)

        # Trabalhando com os modelos de Machine Learning
        st.subheader("Utilizando *Linear Regression* e *Random Forest Regressor*.")

        st.markdown("___Linear Regression___")
        lr = LinearRegression()
        lr_model = lr.fit(X_train, y_train)
        y_pred = lr_model.predict(X_test)
        st.write(f'Acurácia do modelo: {round(lr_model.score(X_test, y_test), 3)}%')

        st.markdown("___Random Forest Regressor___")
        rf = RandomForestRegressor(n_jobs=-1)
        rf_model = rf.fit(X_train, y_train)
        y_pred_rf = rf_model.predict(X_test)
        st.write(f'Acurácia do modelo: {round(rf_model.score(X_test, y_test), 3)}%')

        # Salvando o modelo do Random Forest
        # pickle.dump(rf_model, open('rf_model.pkl', 'wb'))

    elif option == 'Predição':
        # Carregando o modelo para fazer a predição
        rf_model = pickle.load(open('rf_model.pkl', 'rb'))

        st.header('Realizando a predição da nota:')
        st.subheader('Como o melhor modelo foi o *Random Forest* vou utilizar ele para fazer a predição')

        # Gerando um dicionário dos estados e cada um com seu respectivo número do dataframe
        estados_op = {
            0: '---',
            12: 'Acre',
            27: "Alagoas",
            16: "Amapá",
            13: "Amazonas",
            29: "Bahia",
            23: "Ceará",
            53: "Distrito Federal",
            32: "Espirito Santo",
            52: "Goiás",
            21: "Maranhão",
            51: "Mato Grosso",
            50: "Mato Grosso do Sul",
            31: "Minas Gerais",
            15: "Pará",
            25: "Paraíba",
            41: "Paraná",
            26: "Pernambuco",
            22: "Piauí",
            33: "Rio de Janeiro",
            24: "Rio Grande do Norte",
            43: "Rio Grande do Sul",
            11: "Rondônia",
            14: "Roraima",
            42: "Santa Catarina",
            35: "São Paulo",
            28: "Sergipe",
            17: "Tocantins",
        }

        # options -> É a chave/valor/código que está sendo retornado.
        # format_func -> lambda que retorna na página o nome da opção selecionada.

        estados = st.selectbox(
            'Estado', options=list(estados_op.keys()), format_func=lambda x: estados_op[x]
        )

        idade = st.number_input('Idade', min_value=13, max_value=80, step=1, value=18, key='idade')

        # Em 'options' estamos informando que queremos as chaves do dicionário
        escola_op = {1: 'Não respondeu', 2: 'Pública', 3: 'Privada', 4: 'Exterior'}
        escola = st.selectbox(
            'Escola', index=1, key='escola', options=list(escola_op.keys()), format_func=lambda x: escola_op[x]
        )

        # Não é necessário ser apenas dicionário, podemos ter uma lista e pegar os valores dela.
        treino_op = ('Não', 'Sim')
        treino = st.selectbox(
            'Fez somente para treino?', index=0, key='treino', options=list(range(len(treino_op))), format_func=lambda x: treino_op[x]
        )

        st.subheader('Presença nas provas')
        pr_prova_cn_op = ('Não', 'Sim')
        pr_prova_cn = st.selectbox(
            'Ciências da Natureza', index=1, key='pr_prova_cn', options=list(range(len(pr_prova_cn_op))), format_func=lambda x: pr_prova_cn_op[x]
        )

        pr_prova_ch_op = ('Não', 'Sim')
        pr_prova_ch = st.selectbox(
            'Ciências Humanas', index=1, key='pr_prova_ch', options=list(range(len(pr_prova_ch_op))), format_func=lambda x: pr_prova_ch_op[x]
        )

        pr_prova_lc_op = ('Não', 'Sim')
        pr_prova_lc = st.selectbox(
            'Ciências Humanas', index=1, key='pr_prova_lc', options=list(range(len(pr_prova_lc_op))), format_func=lambda x: pr_prova_lc_op[x]
        )

        st.subheader('Notas')
        nt_cn = st.number_input('Ciências da Natureza', min_value=0.0, max_value=1000.0, value=0.0, step=5.0, key='nt_cn')
        nt_ch = st.number_input('Ciências Humanas', min_value=0.0, max_value=1000.0, value=0.0, step=5.0, key='nt_ch')
        nt_lc = st.number_input('Linguagens e Códigos', min_value=0.0, max_value=1000.0, value=0.0, step=5.0, key='nt_lc')
        nt_redacao = st.number_input('Redação', min_value=0.0, max_value=1000.0, value=0.0, step=5.0, key='nt_redacao')

        if st.button('Fazer previsão:'):
            int_features = [estados, idade, escola, treino, pr_prova_cn, pr_prova_ch, pr_prova_lc, nt_cn, nt_ch, nt_lc, nt_redacao]
            final_features = [np.array(int_features)]
            prediction = rf_model.predict(final_features)
            output = round(prediction[0], 2)
            st.write('Nota prevista: ', output)

    else:
        st.subheader('Sobre mim:')
        st.markdown('Uma pessoa que gostou de trabalhar com dados e viu que pode ser gerado muito valor através deles. Foi com esse intuito que comecei a fazer cursos e iniciar a pós-graduação em Ciência de Dados e Big Data.')
        st.markdown('* Pós-Graduando em Ciência de Dados e Big Data pela PUC Minas. _(10/2020)_ \n'
                    '* Acelera Dev Data Science - Codenation _(12/2019)_ \n'
                    '* Data Science de A a Z - Udemy _(07/2019)_ \n'
                    '* Graduação em Sistemas de informação pela Faculdades Promove. _(12/2016)_ *trancado* \n'
                    '* Graduação Tecnológica em Redes de computadores pela Faculdades Promove. _(06/2014)_')

        st.subheader('Contatos:')
        st.markdown('* e-mail - nilson.cunhan@gmail.com \n'
                    '* LinkedIn - https://www.linkedin.com/in/nilsoncunhan/ \n'
                    '* Portfólio web - https://nilsoncunha.github.io/portfolioweb/')


if __name__ == '__main__':
    main()
