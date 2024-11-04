import sys, os
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import openpyxl
import pandas as pd
import numpy
import matplotlib.pyplot as plt
# import seaborn as sns -> 그래프생성시 err떠서 안씀
# 그래프, 폰트 설정
plt.rcParams.update({'figure.dpi' : '150',
                     'figure.figsize' : [10,10],
                     'font.size' : '10',
                     'font.family' : 'Malgun Gothic'})
plt.rc('xtick', labelsize=5)
plt.rc('ytick', labelsize=20)

class GUI:  # 참고로 csv파일로 read_csv하면 df 처리과정에서 err뜬다. 그래서 xlsx, xls로 read_excel 함수 사용한 것이다.
    def us_stock_balance_input(self, str_count):
        str_title = '해외주식잔고(' + str_count + ') 엑셀을 선택해주세요'
        us_stock_balance = filedialog.askopenfilename(initialdir='C:/Users/peras/바탕화면', title=str_title, filetypes=(('*.xlsx','*xlsx'),('*.xls','*xls')))
        if us_stock_balance == '':
            messagebox.showwarning('경고', '해외주식잔고 엑셀파일이 선택되지 않았습니다. 재시도해주세요.')
            sys.exit()
        print('--해외주식잔고(',str_count,')  엑셀파일 : ', us_stock_balance)

        return us_stock_balance

    def deal_detail_input(self, str_count):
        str_title = '거래내역(' + str_count + ') 엑셀을 선택해주세요'
        deal_detail = filedialog.askopenfilename(initialdir='C:/Users/peras/바탕화면', title=str_title, filetypes=(('*.xlsx','*xlsx'),('*.xls','*xls')))
        if deal_detail == '':
            messagebox.showwarning('경고', '거래내역 엑셀파일이 선택되지 않았습니다. 재시도해주세요.')
            sys.exit()
        print('--거래내역(',str_count,') 엑셀파일 : ', deal_detail)

        return deal_detail


def stock_balance_sorting(us_file_999162, us_file_388339):
    df_us_999162 = pd.read_excel(us_file_999162, engine='openpyxl')
    df_us_388339 = pd.read_excel(us_file_388339, engine='openpyxl')
    df_us_388339.drop([0], axis=0, inplace=True)
    df_us = pd.concat([df_us_999162, df_us_388339], axis=0, ignore_index=True)

    # 수정포인트 : 농협엑셀양식의 dataframe.keys 값이 이상한게 많으므로, 이걸로 확인후 아래 for문 수정 필요
    print('--농협 해외주식잔고 엑셀의 DataFrame key값 리스트--\n', df_us.keys(), end='\n\n')

    len_df_us_row = len(df_us['종목명'])     # 농협엑셀형식상 df['종목명']의 첫번째 row의 값은 '종목코드'이므로 이를 제외하고 counting해야한다.
    df_us_result = pd.DataFrame(data=None, index=range(0,int(len_df_us_row/2)),
                             columns=['종목명', '잔고수량', '매입가', '현재가', '외화수익', '외화수익률(%)', '원화수익', '보유비중(%)', '누적배당금',
                                      '1월_입금일자', '1월_외화입금액', '1월_환율', '1월_원화입금액', '2월_입금일자', '2월_외화입금액', '2월_환율', '2월_원화입금액',
                                      '3월_입금일자', '3월_외화입금액', '3월_환율', '3월_원화입금액', '4월_입금일자', '4월_외화입금액', '4월_환율', '4월_원화입금액',
                                      '5월_입금일자', '5월_외화입금액', '5월_환율', '5월_원화입금액', '6월_입금일자', '6월_외화입금액', '6월_환율', '6월_원화입금액',
                                      '7월_입금일자', '7월_외화입금액', '7월_환율', '7월_원화입금액', '8월_입금일자', '8월_외화입금액', '8월_환율', '8월_원화입금액',
                                      '9월_입금일자', '9월_외화입금액', '9월_환율', '9월_원화입금액', '10월_입금일자', '10월_외화입금액', '10월_환율', '10월_원화입금액',
                                      '11월_입금일자', '11월_외화입금액', '11월_환율', '11월_원화입금액', '12월_입금일자', '12월_외화입금액', '12월_환율', '12월_원화입금액'])

    row=0   # df_us_result 행 index용
    for i in range(0,len_df_us_row):
        if i == 0:
            pass
        elif i%2 == 1:  # row index값이 홀수이면
            df_us_result['종목명'][row] = df_us['종목명'][i]
            df_us_result['잔고수량'][row] = df_us['잔고수량'][i]
            try:
                df_us_result['매입가'][row] = df_us['매입가\n(외화)'][i]
            except:
                df_us_result['매입가'][row] = df_us['매입가_x000D_\n(외화)'][i]
            try:
                df_us_result['외화수익'][row] = df_us['평가손익\n(외화)'][i]
            except:
                df_us_result['외화수익'][row] = df_us['평가손익_x000D_\n(외화)'][i]
            try:
                df_us_result['원화수익'][row] = df_us['평가손익\n(원화)'][i]
            except:
                df_us_result['원화수익'][row] = df_us['평가손익_x000D_\n(원화)'][i]
            df_us_result['보유비중(%)'][row] = df_us['보유비중'][i] * 100
        else:           # row index값이 짝수이면
            try:
                df_us_result['현재가'][row] = df_us['매입가\n(외화)'][i]
            except:
                df_us_result['현재가'][row] = df_us['매입가_x000D_\n(외화)'][i]
            try:
                df_us_result['외화수익률(%)'][row] = df_us['평가손익\n(외화)'][i]
            except:
                df_us_result['외화수익률(%)'][row] = df_us['평가손익_x000D_\n(외화)'][i]
            row += 1

    df_us_result.sort_values(by=['외화수익률(%)'], ascending=False, inplace=True)
    df_us_result.reset_index(drop=True, inplace=True)

    return df_us_result

def deal_detail_sorting(file_999162, file_388339):
    df_999162 = pd.read_excel(file_999162, engine='openpyxl')
    df_388339 = pd.read_excel(file_388339, engine='openpyxl')
    df_388339.drop([0], axis=0, inplace=True)
    df = pd.concat([df_999162, df_388339], axis=0, ignore_index=True)

    # 수정포인트 : 농협엑셀양식의 dataframe.keys 값은 Unnamed(공란)인게 많으므로, 이걸로 확인후 아래 for문 수정 필요
    print('--농협 해외거래내역 엑셀의 DataFrame key값 리스트--\n', df.keys(), end='\n\n')

    len_df_row = len(df['거래일자'])  # 수정포인트 : 농협_해외거래내역 엑셀에서 첫번째 열의 총 길이 측정하는 것. 필요시 ''사이 값 수정필요.
    df_result = pd.DataFrame(data=None, index=range(0, len_df_row), columns=['입금일자', '종목명', '외화입금액', '환율', '원화입금액'])

    row = 0  # df_result 행 index용
    for i in range(0, len_df_row):
        if df['거래구분'][i] == '외화배당금입금':
            date = str(df['거래일자'][i-1])
            date = date.replace('/', '-')
            df_result['입금일자'][row] = date
            try:
                df_result['종목명'][row] = df['주문종목코드'][i]
            except:
                dividend_krw = float(df['외화정산금액'][i-1]) * float(df['통화'][i])   # 잔고에 미등록된 주식종목의 배당금액(원화환산액)
                print('* [잔고 미등록 배당금]', date, '에', df['주문종목코드'][i], '로부터', dividend_krw ,'원 이 입금됬습니다.')
                df_result['종목명'][row] = df['주문종목코드'][i]

            df_result['외화입금액'][row] = float(df['외화정산금액'][i-1])
            df_result['환율'][row] = float(df['통화'][i])
            dividend_krw = df_result['외화입금액'][row] * df_result['환율'][row]
            df_result['원화입금액'][row] = dividend_krw
            row += 1
        elif df['거래구분'][i] == '배당금':
            date = str(df['거래일자'][i - 1])
            date = date.replace('/', '-')
            df_result['입금일자'][row] = date
            df_result['외화입금액'][row] = 'N/A'
            df_result['환율'][row] = 'N/A'

            # 수정포인트 : 농협_해외거래내역 엑셀에선 한국 배당금 입금액이 '100.' 이런식으로 써져서, 아래와같이 편집한 것임. 농협형식이 달라졌으면, 아래내용도 수정필요.
            dividend_krw = float(df['외화정산금액'][i])
            df_result['원화입금액'][row] = dividend_krw

            try:
                df_result['종목명'][row] = df['주문종목코드'][i]
            except:
                print('* [잔고 미등록 배당금]', date, '에', df['주문종목코드'][i], '로부터', dividend_krw, '원 이 입금됬습니다.')   # 잔고에 미등록된 주식종목의 배당금액(원화환산액)
                df_result['종목명'][row] = df['주문종목코드'][i]

            row += 1
        elif '분배금입금' in df['거래구분'][i]:
            date = str(df['거래일자'][i - 1])
            date = date.replace('/', '-')
            df_result['입금일자'][row] = date
            df_result['외화입금액'][row] = 'N/A'
            df_result['환율'][row] = 'N/A'

            # 수정포인트 : 농협_해외거래내역 엑셀에선 한국 배당금 입금액이 '100.00' 이런식으로 써져서, 아래와같이 편집한 것임. 농협형식이 달라졌으면, 아래내용도 수정필요.
            dividend_krw = float(df['외화정산금액'][i])
            df_result['원화입금액'][row] = dividend_krw

            try:
                df_result['종목명'][row] = df['주문종목코드'][i]
            except:
                print('* ', date, '에', df['주문종목코드'][i], '로부터', dividend_krw, '원 이 입금됬습니다.')  # 잔고에 미등록된 주식종목의 배당금액(원화환산액)
                df_result['종목명'][row] = df['주문종목코드'][i]

            row += 1
        else:
            pass

    print('\n')
    df_result.dropna(inplace=True)
    df_result.sort_values(by=['입금일자'], ascending=False, inplace=True)
    df_result.reset_index(drop=True, inplace=True)
    # print(df_result)

    return df_result

def stock_balance_add_dividend_info(df_stock_balance, df_dividend_detail):
    def year_balance_init(df_stock_balance):
        df_stock_balance['1월_외화입금액'] = float(0)
        df_stock_balance['1월_원화입금액'] = float(0)
        df_stock_balance['2월_외화입금액'] = float(0)
        df_stock_balance['2월_원화입금액'] = float(0)
        df_stock_balance['3월_외화입금액'] = float(0)
        df_stock_balance['3월_원화입금액'] = float(0)
        df_stock_balance['4월_외화입금액'] = float(0)
        df_stock_balance['4월_원화입금액'] = float(0)
        df_stock_balance['5월_외화입금액'] = float(0)
        df_stock_balance['5월_원화입금액'] = float(0)
        df_stock_balance['6월_외화입금액'] = float(0)
        df_stock_balance['6월_원화입금액'] = float(0)
        df_stock_balance['7월_외화입금액'] = float(0)
        df_stock_balance['7월_원화입금액'] = float(0)
        df_stock_balance['8월_외화입금액'] = float(0)
        df_stock_balance['8월_원화입금액'] = float(0)
        df_stock_balance['9월_외화입금액'] = float(0)
        df_stock_balance['9월_원화입금액'] = float(0)
        df_stock_balance['10월_외화입금액'] = float(0)
        df_stock_balance['10월_원화입금액'] = float(0)
        df_stock_balance['11월_외화입금액'] = float(0)
        df_stock_balance['11월_원화입금액'] = float(0)
        df_stock_balance['12월_외화입금액'] = float(0)
        df_stock_balance['12월_원화입금액'] = float(0)

    def year_balance_sorting(df_dividend_detail, df_stock_balance):
        if '-01-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 1월인 경우
            df_stock_balance['1월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['1월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['1월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['1월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-02-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 2월인 경우
            df_stock_balance['2월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['2월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['2월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['2월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-03-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 3월인 경우
            df_stock_balance['3월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['3월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['3월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['3월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-04-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 4월인 경우
            df_stock_balance['4월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['4월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['4월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['4월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-05-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 5월인 경우
            df_stock_balance['5월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['5월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['5월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['5월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-06-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 6월인 경우
            df_stock_balance['6월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['6월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['6월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['6월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-07-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 7월인 경우
            df_stock_balance['7월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['7월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['7월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['7월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-08-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 8월인 경우
            df_stock_balance['8월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['8월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['8월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['8월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-09-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 9월인 경우
            df_stock_balance['9월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['9월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['9월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['9월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-10-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 10월인 경우
            df_stock_balance['10월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['10월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['10월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['10월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-11-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 11월인 경우
            df_stock_balance['11월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['11월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['11월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['11월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])
        elif '-12-' in df_dividend_detail['입금일자'][row]:  # 배당금 입금일자가 12월인 경우
            df_stock_balance['12월_입금일자'][searched_row] = df_dividend_detail['입금일자'][row]
            df_stock_balance['12월_외화입금액'][searched_row] += float(df_dividend_detail['외화입금액'][row])
            df_stock_balance['12월_환율'][searched_row] = df_dividend_detail['환율'][row]
            df_stock_balance['12월_원화입금액'][searched_row] += float(df_dividend_detail['원화입금액'][row])

    def sum_monthly_dividend(df, len_df):
        for row in range(0, len_df):
            list_monthly_dividend = [float(df['1월_원화입금액'][row]), float(df['2월_원화입금액'][row]),
                                     float(df['3월_원화입금액'][row]), float(df['4월_원화입금액'][row]),
                                     float(df['5월_원화입금액'][row]), float(df['6월_원화입금액'][row]),
                                     float(df['7월_원화입금액'][row]), float(df['8월_원화입금액'][row]),
                                     float(df['9월_원화입금액'][row]), float(df['10월_원화입금액'][row]),
                                     float(df['11월_원화입금액'][row]), float(df['12월_원화입금액'][row])]
            list_monthly_dividend = [x for x in list_monthly_dividend if numpy.isnan(x) == False]  # list_monthly_dividend에서 NaN 값을 제거하는 구문
            df['누적배당금'][row] = sum(list_monthly_dividend)  # sum 구문에선 NaN값이 input list에 하나라도 포함되있으면 합 결과값이 NaN으로 뜬다.

        return df


    list_ticker = df_stock_balance['종목명'].to_list()
    len_df_dividend_detail = len(df_dividend_detail['종목명'])
    df_other_dividend_detail = pd.DataFrame(data=None, index=range(0, int(len(df_dividend_detail['종목명']))), columns=['입금일자', '종목명', '외화입금액', '환율', '원화입금액'])    # 농협_잔고에 없는 종목들의 배당금내역 저장용 dataframe

    # 아래는 df_stock_balance를 연도별로 복붙하는 것이다. '잔고별 배당금입금내역.xlsx'에서 연도별을 sheet로 분리하기위함.
    df_stock_balance_2020 = df_stock_balance.copy()
    df_stock_balance_2021 = df_stock_balance.copy()
    df_stock_balance_2022 = df_stock_balance.copy()
    df_stock_balance_2023 = df_stock_balance.copy()
    df_stock_balance_2024 = df_stock_balance.copy()
    df_stock_balance_2025 = df_stock_balance.copy()

    # 각 월별 외화입금액, 원화입금액 column 0으로 숫자 초기화&기입
    year_balance_init(df_stock_balance_2020)
    year_balance_init(df_stock_balance_2021)
    year_balance_init(df_stock_balance_2022)
    year_balance_init(df_stock_balance_2023)
    year_balance_init(df_stock_balance_2024)
    year_balance_init(df_stock_balance_2025)

    row_2 = 0   # df_other_dividend_detail 용 행 index 선언
    for row in range(0,len_df_dividend_detail):
        if df_dividend_detail['종목명'][row] in list_ticker:
            searched_row = ticker_row_search(df_stock_balance, df_dividend_detail['종목명'][row])
            if '2020' in df_dividend_detail['입금일자'][row]:
                year_balance_sorting(df_dividend_detail, df_stock_balance_2020)
            elif '2021' in df_dividend_detail['입금일자'][row]:
                year_balance_sorting(df_dividend_detail, df_stock_balance_2021)
            elif '2022' in df_dividend_detail['입금일자'][row]:
                year_balance_sorting(df_dividend_detail, df_stock_balance_2022)
            elif '2023' in df_dividend_detail['입금일자'][row]:
                year_balance_sorting(df_dividend_detail, df_stock_balance_2023)
            elif '2024' in df_dividend_detail['입금일자'][row]:
                year_balance_sorting(df_dividend_detail, df_stock_balance_2024)
            elif '2025' in df_dividend_detail['입금일자'][row]:
                year_balance_sorting(df_dividend_detail, df_stock_balance_2025)
        else:
            df_other_dividend_detail['입금일자'][row_2] = df_dividend_detail['입금일자'][row]
            df_other_dividend_detail['종목명'][row_2] = df_dividend_detail['종목명'][row]
            df_other_dividend_detail['외화입금액'][row_2] = df_dividend_detail['외화입금액'][row]
            df_other_dividend_detail['환율'][row_2] = df_dividend_detail['환율'][row]
            df_other_dividend_detail['원화입금액'][row_2] = df_dividend_detail['원화입금액'][row]
            row_2 += 1

    df_stock_balance_2020 = sum_monthly_dividend(df_stock_balance_2020, len(df_stock_balance_2020['종목명']))
    df_stock_balance_2021 = sum_monthly_dividend(df_stock_balance_2021, len(df_stock_balance_2021['종목명']))
    df_stock_balance_2022 = sum_monthly_dividend(df_stock_balance_2022, len(df_stock_balance_2022['종목명']))
    df_stock_balance_2023 = sum_monthly_dividend(df_stock_balance_2023, len(df_stock_balance_2023['종목명']))
    df_stock_balance_2024 = sum_monthly_dividend(df_stock_balance_2024, len(df_stock_balance_2024['종목명']))
    df_stock_balance_2025 = sum_monthly_dividend(df_stock_balance_2025, len(df_stock_balance_2025['종목명']))

    df_other_dividend_detail.dropna(inplace=True)
    # print(df_stock_balance)
    # print(df_other_dividend_detail)

    return df_other_dividend_detail, df_stock_balance_2020, df_stock_balance_2021, df_stock_balance_2022, df_stock_balance_2023, df_stock_balance_2024, df_stock_balance_2025

def ticker_row_search(df, ticker):
    len_df = len(df['종목명'])

    for row in range(0,len_df):
        if df['종목명'][row] == ticker:
            searched_row = row
        else:
            pass

    return searched_row

def bar_graph_create(df, year, flag):
    if flag == '월별배당금':
        plt.bar(df['월'], df['월별배당금'])
        plt.xlabel('월별')
        plt.ylabel('월별배당금(백만원)')
        plt.xticks(rotation=0)
        fig_title = str(year) + '년 월별배당금'
        plt.title(fig_title)

        for i in range(len(df['월'])):
            height = df['월별배당금'][i]
            plt.text(df['월'][i], height + 1, int(height), ha='center', va='bottom', size=9, rotation=0)

        fig_name = 'C:/Users/peras/바탕화면/' + str(year) + '년_월별_배당금.png'
        plt.savefig(fig_name)
        plt.cla()

    elif flag == '종목별배당금':
        df_graph = df.sort_values('누적배당금', ascending=False)

        # sns.barplot(df, x='종목명', y='누적배당금').tick_params(axis='x', labelrotation=90)
        plt.bar(df_graph['종목명'], df_graph['누적배당금'])
        plt.xlabel('종목별')
        plt.ylabel('종목별 연간배당금(백만원)')
        plt.xticks(rotation=90)
        fig_title = str(year) + '년 종목별배당금'
        plt.title(fig_title)

        for i in range(len(df_graph['종목명'])):
            height = df_graph['누적배당금'][i]
            plt.text(df_graph['종목명'][i], height + 1, int(height), ha='center', va='bottom', size=9, rotation=90)

        fig_name = 'C:/Users/peras/바탕화면/' + str(year) + '년_종목별_배당금.png'
        plt.savefig(fig_name)
        plt.cla()

def query_monthly_dividend(df):
    # df에서 2020, 2021, 2022... 연별로 df를 query한뒤, 각각 월별 수령배당금 그래프 생성.

    # print(df['입금일자'].dtype)
    df['연도'] = df['입금일자'].str[:4]
    df['월'] = df['입금일자'].str[5:7]

    df_graph_2020 = df.query('연도 == "2020"').reset_index(drop=True)\
                      .groupby('월', as_index=False).agg(월별배당금=('원화입금액', 'sum'))
    df_graph_2021 = df.query('연도 == "2021"').reset_index(drop=True)\
                      .groupby('월', as_index=False).agg(월별배당금=('원화입금액', 'sum'))
    df_graph_2022 = df.query('연도 == "2022"').reset_index(drop=True)\
                      .groupby('월', as_index=False).agg(월별배당금=('원화입금액', 'sum'))
    df_graph_2023 = df.query('연도 == "2023"').reset_index(drop=True)\
                      .groupby('월', as_index=False).agg(월별배당금=('원화입금액', 'sum'))
    df_graph_2024 = df.query('연도 == "2024"').reset_index(drop=True) \
                      .groupby('월', as_index=False).agg(월별배당금=('원화입금액', 'sum'))

    bar_graph_create(df_graph_2020, 2020, '월별배당금')
    bar_graph_create(df_graph_2021, 2021, '월별배당금')
    bar_graph_create(df_graph_2022, 2022, '월별배당금')
    bar_graph_create(df_graph_2023, 2023, '월별배당금')
    bar_graph_create(df_graph_2024, 2024, '월별배당금')

def main():
    gui = GUI()
    us_stock_balance_999162 = gui.us_stock_balance_input('999162')
    us_stock_balance_388339 = gui.us_stock_balance_input('388339')
    deal_detail_999162 = gui.deal_detail_input('999162')
    deal_detail_388339 = gui.deal_detail_input('388339')

    df_stock_balance = stock_balance_sorting(us_stock_balance_999162, us_stock_balance_388339)
    df_dividend_detail = deal_detail_sorting(deal_detail_999162, deal_detail_388339)

    df_other_dividend_detail, df_2020, df_2021, df_2022, df_2023, df_2024, df_2025 = stock_balance_add_dividend_info(df_stock_balance, df_dividend_detail)

    df_dividend_detail.to_excel('C:/Users/peras/바탕화면/일자별 배당금입금내역.xlsx')
    # df_other_dividend_detail.to_excel('C:/Users/peras/바탕화면/잔고외 배당금입금내역.xlsx')

    df_stock_balance_writer = pd.ExcelWriter('C:/Users/peras/바탕화면/잔고내 배당금입금내역.xlsx')
    df_2020.to_excel(df_stock_balance_writer, sheet_name='2020')
    df_2021.to_excel(df_stock_balance_writer, sheet_name='2021')
    df_2022.to_excel(df_stock_balance_writer, sheet_name='2022')
    df_2023.to_excel(df_stock_balance_writer, sheet_name='2023')
    df_2024.to_excel(df_stock_balance_writer, sheet_name='2024')
    df_2025.to_excel(df_stock_balance_writer, sheet_name='2025')
    df_stock_balance_writer.save()

    # 연도, 월별 배당금수령액 bar그래프 생성
    query_monthly_dividend(df_dividend_detail)

    # 연도, 잔고종목별 배당금수령액 bar그래프 생성
    # bar_graph_create(df_2020, 2020, '종목별배당금')
    # bar_graph_create(df_2021, 2021, '종목별배당금')
    # bar_graph_create(df_2022, 2022, '종목별배당금')
    # bar_graph_create(df_2023, 2023, '종목별배당금')
    bar_graph_create(df_2024, 2024, '종목별배당금')
    # bar_graph_create(df_2025, 2025, '종목별배당금')


if __name__ == '__main__':
    main()