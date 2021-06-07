import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash_table
import plotly.express as px
from sklearn.metrics import mean_squared_error
from math import sqrt


estilos = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app=dash.Dash(__name__,external_stylesheets=estilos)

encabezado=html.H1('Evaluación de Métodos de Pronósticos Naive y Promedio Móvil',style={'color': 'black', 'text-align':'center'})
autor=html.H3('Andrés Felipe Salazar',style={'color': 'black', 'text-align':'center'})

df=pd.read_csv('/home/biusc/mysite/datasetventascompleto.csv',sep=";")
df['Fecha_Pedido']=pd.to_datetime(df['Fecha_Pedido'],dayfirst=True)
clientes=df.groupby('Cliente')['Total'].sum().reset_index().sort_values(by='Total',ascending=False,axis=0)
tabla=dash_table.DataTable(columns=[{"name": i, "id": i} for i in clientes.columns], data=clientes.to_dict('records'))

#Se crea una nueva columna sin tener en cuenta el día de la fecha
df['Año_mes']=df['Fecha_Pedido'].dt.strftime('%Y-%m')
historico=df.groupby('Año_mes')['Cantidad'].sum().reset_index()
grafico=dcc.Graph(figure=px.line(historico, x="Año_mes", y="Cantidad", title='Cantidad Histórica de Ventas'))
torta=dcc.Graph(figure=px.pie(clientes, values='Total', names='Cliente', title='Participación de las ventas por clientes'))

#Método de Pronóstico del último dato: "Naive"
historico['naive']=historico['Cantidad'][5:].shift()
RMSE_naive=sqrt(mean_squared_error(historico.Cantidad[6:],historico.naive[6:]))
res1=html.H3('Resultado método Naive',style={'color': 'blue', 'text-align':'center'})

error_naive=html.H3(round(RMSE_naive,2),style={'color': 'red', 'text-align':'center'})

#Método de Pronóstico de Promedio Móvil
historico['PM_3']=historico['Cantidad'][3:].shift().rolling(3).mean()
RMSE_PM3=sqrt(mean_squared_error(historico.Cantidad[6:],historico.PM_3[6:]))
res2=html.H3('Resultado método Promedio Móvil',style={'color': 'blue', 'text-align':'center'})
error_MP3=html.H3(round(RMSE_PM3,2),style={'color': 'red', 'text-align':'center'})


app.layout=html.Div([encabezado,autor,grafico,res1,error_naive,res2,error_MP3,torta,tabla])


if __name__=='__main__':
    app.run_server(debug=True)