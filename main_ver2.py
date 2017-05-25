import sys, glob, datetime
import apache_log_parser

# グローバル変数
# パーサー。Logの書式を指定。
parser = apache_log_parser.make_parser('%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"')

def main():
    # 読込ファイル名リスト
    readfile = glob.glob("target/*.txt")
    # モードセレクト用変数
    mode_num = 0
    # 時間指定
    start_time = datetime.datetime.strptime('1900/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')
    last_time = datetime.datetime.strptime('2099/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
    while(mode_num != '4'):
        print('select mode (only input number)')
        print('1. output access num depend on time')
        print('2. output access num depend on host')
        print('3. specify a time period')
        print('4. program termination')
        # mode_numに入力
        mode_num = input()
        if(mode_num == '1'):
            output_by_time(readfile,start_time,last_time)
        elif(mode_num == '2'):
            output_by_host(readfile,start_time,last_time)
        elif(mode_num == '3'):
            # 指定期間の入力
            print('input start time')
            start_time = datetime.datetime.strptime(input(), '%Y/%m/%d %H:%M:%S')
            print('input last time')
            last_time = datetime.datetime.strptime(input(), '%Y/%m/%d %H:%M:%S')
        elif(mode_num == '4'):
            print('This program will terminate. Thank you for using.')
        else:
            print('You input wrong number.Input Again.')

def output_by_time(readfile,start_time,last_time):
    # アクセス件数用配列
    access_num = [0] * 24
    for file in readfile:
        # ファイル読み込み
        f = open(file, "r")
        # 解析用データ作成
        line = f.readline()           # 1行読む
        # ループ回数
        counter = 0
        while line:
            log_data = parser(line)   # 解析してdictionaryにする
            if(log_data['time_received_datetimeobj'] < start_time):
                continue
            elif(log_data['time_received_datetimeobj'] > last_time):
                break
            else:
                access_num[int(log_data['time_received_datetimeobj'].strftime('%H'))] += 1
            counter += 1
            if(counter % 10000 == 0):
            	sys.stdout.write("\r読み込み数：%d" % counter)
            	sys.stdout.flush()
            line = f.readline()       # 1行読む
    # 出力
    for i in range(24):
        print(str(i) + ' : ' + str(access_num[i]))

def output_by_host(readfile,start_time,last_time):
    # 既出ホストリスト
    hostname = []
    # アクセス件数用リスト
    access_num = []
    for file in readfile:
        # ファイル読み込み
        f = open(file, "r")
        # 解析用データ作成
        line = f.readline()           # 1行読む
        # ループ回数
        counter = 0
        while line:
            log_data = parser(line)   # 解析してdictionaryにする
            if(log_data['time_received_datetimeobj'] < start_time):
                continue
            elif(log_data['time_received_datetimeobj'] > last_time):
                break
            elif(log_data['remote_host'] in hostname):
                access_num[hostname.index(log_data['remote_host'])]['sum'] += 1
            else:
                access_num.append({"remote_host":log_data['remote_host'],"sum":1})
                hostname.append(log_data['remote_host'])
            counter += 1
            if(counter % 10000 == 0):
            	sys.stdout.write("\r読み込み数：%d" % counter)
            	sys.stdout.flush()
            line = f.readline()       # 1行読む
    # アクセス件数でソート
    new_list = sorted(access_num, key = lambda x: x['sum'], reverse = True)
    # 出力
    for i in new_list:
        print(i['remote_host'] + ' : ' + str(i['sum']))
# 最後に実行
main()
