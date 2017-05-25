import glob
import datetime
import apache_log_parser

def main():
    # パーサーを作成. Logの書式を指定。
    parser = apache_log_parser.make_parser('%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"')
    # 読込ファイル名リスト
    readfile = glob.glob("target/*.txt")
    # 解析用元データ
    list = []
    for file in readfile:
        # ファイル読み込み
        f = open(file, "r")
        # 解析用データ作成
        line = f.readline()           # 1行読む
        while line:
            log_data = parser(line)   # 解析してdictionaryにする
            log_data = {'remote_host':log_data['remote_host'],
                        'time_received_datetimeobj':log_data['time_received_datetimeobj']}
            list.append(log_data)     # リストに追加
            line = f.readline()       # 1行読む
    # この時点でlistに全データが入っている
    # モードセレクト用変数
    mode_num = 0
    while(mode_num != '4'):
        print('select mode (only input number)')
        print('1. output access num depend on time')
        print('2. output access num depend on host')
        print('3. specify a time period')
        print('4. program termination')
        # mode_numに入力
        mode_num = input()
        if(mode_num == '1'):
            output_by_time(list)
        elif(mode_num == '2'):
            output_by_host(list)
        elif(mode_num == '3'):
            # 指定期間の入力
            print('input start time')
            start_time = datetime.datetime.strptime(input(), '%Y/%m/%d %H:%M:%S')
            print('input last time')
            last_time = datetime.datetime.strptime(input(), '%Y/%m/%d %H:%M:%S')
            specify_time(list,start_time,last_time)
        elif(mode_num == '4'):
            print('This program will terminate. Thank you for using.')
        else:
            print('You input wrong number.Input Again.')

def output_by_time(list):
    # アクセス件数用配列
    access_num = [0] * 24
    # 時間ごとにソート
    sorted(list, key = lambda x: x['time_received_datetimeobj'].strftime('%H'))
    # access_numを生成
    for i in list:
        access_num[int(i['time_received_datetimeobj'].strftime('%H'))] += 1
    # 出力
    for i in range(24):
        print(str(i) + ' : ' + str(access_num[i]))

def output_by_host(list):
    # 一つ前のホスト名
    before_host = ""
    # アクセス件数用リスト
    access_num = []
    # 予めホスト名でソート
    sorted(list, key = lambda x: x['remote_host'])
    # access_numを生成
    for i in list:
        if(i['remote_host'] == before_host):
            access_num[len(access_num)-1]['sum'] += 1
        else:
            access_num.append({"remote_host":i['remote_host'],"sum":1})
            before_host = i['remote_host']
    # アクセス件数でソート
    sorted(access_num, key = lambda x: x['sum'], reverse = True)
    # 出力
    for i in access_num:
        print(i['remote_host'] + ' : ' + str(i['sum']))

def specify_time(list,start_time,last_time):
    # 時間でソート
    sorted(list, key = lambda x: x['time_received_datetimeobj'])
    # 開始時間前の削除
    for i,time in enumerate(list):
        if(time['time_received_datetimeobj'] < start_time):
            del list[i]
        else:
            break
    # 終了時間後の削除
    for i,time in enumerate(list):
        if(time['time_received_datetimeobj'] > last_time):
            del list[i:]
            break
# 最後に実行
main()
