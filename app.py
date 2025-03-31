from flask import Flask, request, render_template, url_for
import pandas as pd
import invest



app = Flask(__name__)

# 유저가 어떤 종목 투자기간, 투자 전략 방식을 입력할 수 있는
# 페이지를 보여주는 api 생성
@app.route('/invest')
def invest():
    return render_template('invest.html')


# table_cols (표에서 컬럼의 이름들) list
# table_data (표에서 벨류의 값들) dict
# x_data (차트에서 x축 데이터) list
# y_data (차트에서 y축 데이터) list 
@app.route('/dashboard')
def dashboard():
    # 유저가 보낸 데이터를 변수에 저장
    # get 방식으로 보내온 데이터는 request.args에 존재
    # 종목코드
    input_code = request.args['code']
    # 시작시간
    input_year = request.args['year']
    input_month = request.args['month']
    input_day = request.args['day']
    input_time = f'{input_year}-{input_month}-{input_day}'
    input_type = request.args['type']


    df = invest.load_data(input_code, input_time)
    invest_class = invest.Invest(df, _col='Close', _start = input_time)

    if input_type == 'bnh':
        result = invest_class.buyandhold()
    elif input_type == 'boll':
        result = invest_class.bollinger()
    elif input_type =='mmt':
        result = invest_class.momentum() 

    result.reset_index(inplace=True)

    result = result[['Date', 'Close', 'trade', 'rtn', 'acc_rtn']]
    
    result.columns = ['시간', '종가', '보유내역', '일별수익률', '누적수익률']

    cols_list = list(result.columns)

    dict_data = result.to_dict(orient='records')

    x_data = list(result['시간'])
    y_data = list(result['일별수익률'])
    y2_data = list(result['누적수익률'])
    
    return render_template('dashboard.html')



app.run(debug=True)