import pandas as pd

def futures_adjustment(df, selected_product, adjustment_algo):
    tmp_df = df.copy()
    reqd_cols = ['date',  'expiration_date', 'daily_settle_price']

    # extract price series for front month and back month contracts
    tmp_c1 =\
        tmp_df[
            (tmp_df['contract_month']==1)
            & (tmp_df['exch_code']==selected_product)
            ][reqd_cols].copy()
    
    tmp_c2 =\
        tmp_df[
            (tmp_df['contract_month']==2)
            & (tmp_df['exch_code']==selected_product)
            ][reqd_cols].copy()

    # extract simple unadjusted futures price
    c1 = tmp_c1[['date', 'daily_settle_price']].copy()
    c1['label'] = 'Unadjusted Price'

    if adjustment_algo:
        tmp_roll_spread =\
            tmp_c1[
                tmp_c1['date'] == tmp_c1['expiration_date']
            ].copy()
        
        tmp_roll_spread =\
            tmp_roll_spread.merge(
                tmp_c2[['date','daily_settle_price']],
                on = 'date',
                how = 'left'
            )
        
        tmp_roll_spread.rename(
            columns = {'daily_settle_price_x' : 'c1',
                    'daily_settle_price_y' : 'c2'},
            inplace = True
        )

        tmp_roll_spread['roll_spread'] =\
            tmp_roll_spread['c2']\
            - tmp_roll_spread['c1'] 
        
        tmp_c1 =\
            tmp_c1.merge(
                tmp_roll_spread[['date', 'roll_spread']],
                on = ['date'],
                how = 'left'
            )
        
        tmp_c1['roll_spread'].fillna(0, inplace=True)

        tmp_adj = tmp_c1.copy()
        if adjustment_algo == 'Forward Adjustment':
            tmp_adj['adjustment'] = tmp_adj['roll_spread'].cumsum()
            tmp_adj['adjustment'] *= -1

        elif adjustment_algo == 'Backward Adjustment':
            tmp_adj['adjustment'] = tmp_adj['roll_spread'][::-1].cumsum()[::-1]

        tmp_adj['daily_settle_price'] += tmp_adj['adjustment']
        tmp_adj['label'] = adjustment_algo

        c1 = pd.concat([c1, tmp_adj])

    c1.reset_index(drop = True, inplace=True)

    return c1


def get_performance_metrics(df, label):
    price_series = df.loc[df['label'] == label, 'daily_settle_price'].copy()
    initial_price = price_series.iloc[0]
    final_price = price_series.iloc[-1]

    total_return = final_price / initial_price - 1
    return_series = price_series.pct_change()
    volatility = return_series.std() * np.sqrt(252)
    sharpe_ratio = np.mean(return_series) / volatility

    watermark = price_series.cummax()
    drawdowns = watermark - price_series
    maxdrawdown = drawdowns.max()

    return total_return, volatility, sharpe_ratio, maxdrawdown
