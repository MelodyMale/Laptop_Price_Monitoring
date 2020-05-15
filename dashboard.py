import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dbm

# Set up the app
app = dash.Dash(__name__)
server = app.server

global product_df
global dict_products

def create_dict_list_of_product():
    dictlist = []
    unique_list = product_df.product_name.unique()
    for product_name in unique_list:
        dictlist.append({'value': product_name, 'label': product_name})
    return dictlist

def dict_product_list(dict_list):
    product_list = []
    for dict in dict_list:
        product_list.append(dict.get('value'))
    return product_list

product_df = dbm.read()
dict_products = create_dict_list_of_product()

app.layout = html.Div([
    html.Div([
        html.H1('Laptop Price Optimization Dashboard'),
        html.H2('Choose a product name'),
        dcc.Dropdown(
            id='product-dropdown',
            options=dict_products,
            multi=True,
            value = [dict_products[index]['value'] for index in range(2)]
        )
    ], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.H2('All product info'),
        html.Table(id='my-table'),
        html.P('')
    ], style={'width': '55%', 'float': 'right', 'display': 'inline-block', 'overflowY': 'auto'})
], style={'width': '90%', 'height': '100vh',  'display': 'inline-block'})


# for the table
@app.callback(Output('my-table', 'children'), [Input('product-dropdown', 'value')])
def generate_table(selected_dropdown_value, max_rows=6):
    product_df_filter = product_df[(product_df['product_name'].isin(selected_dropdown_value))]
    product_df_filter = product_df_filter.sort_values(['product_name','datetime'], ascending=True)

    return [html.Tr([html.Th(col) for col in product_df_filter  .columns])] + [html.Tr([
        html.Td(product_df_filter.iloc[i][col]) for col in product_df_filter  .columns
    ]) for i in range(min(len(product_df_filter  ), max_rows))]

if __name__ == '__main__':
    app.run_server(debug=True)
