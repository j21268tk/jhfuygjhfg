#必要な関数のインポート
#wavファイルの書き出しにはwave
#jupyter notebookで音を確認するためにはsounddeviceライブラリを使う
import numpy as np
import scipy.signal as sp
import wave as wave
import sounddevice as sd # type: ignore
#波形やスペクトログラムを見るためにmatplotlibも使う
import matplotlib.pyplot as plt # type: ignore
#%matplotlib inline
#基本となるデータや空の行列の用意
#作る音の秒数、サンプリング周波数を決める
duration = 1.0 #時間、秒
fs = 44100 #サンプリング周波数
#時間をサンプリング周波数で割り、時刻を時点に変えておく
t = np.arange(0,fs*duration)/fs #時間を時点数に変換
#ベースとなる振幅、基本周波数を用意
amplitude = 1.0 #振幅
f0 = 440.0 #周波数 基本周波数
#音のデータを格納していくための空のnumpy行列を作る。要素同士を足し算するので、numpy行列の方が便利。
#x=周波数,y=振幅の2乗（パワー）のグラフを後で描くので、こちらは空のリストを用意しておく
z = np.zeros(len(t))
x = []
pow_y = []
#乱数によるピンクノイズの作成
#「パワー（＝振幅の2乗）が、周波数に反比例する」がピンクノイズの定義。
import random

for i in np.arange(1,44):
   j = random.randint(1,44)
   z = z + np.array((pow(amplitude*(1/(f0*j)),1/2))*np.cos(2*np.pi*f0*j*t))
   pow_y.append(pow(pow(amplitude*(1/(f0*j)),1/2),2))
   x.append(f0*j)
   #音の確認
   #sounddeviceライブラリで再生する
   sd.play(z,fs)
print("再生中")
status=sd.wait()
#WAVEファイルへの書き出し
#Pythonの整数値には上限があるので、上限の範囲に収まるようにスケーリングする。16bitで量子化するのでint16の上限値以内に収まるようにし、整数値にする。
z2 = (z/z.max())*np.iinfo(np.int16).max #スケールを整数のマックスに
z2 = z2.astype(np.int16) #2バイトデータ化
#書き出し。
wave_out = wave.open("./sin_220319_008.wav","w")
wave_out.setnchannels(1)
wave_out.setsampwidth(2) #16bitなので2byte
wave_out.setframerate(fs)
wave_out.writeframes(z2)
wave_out.close()
#波形をグラフ化する。時刻毎の振幅
fig,ax = plt.subplots(1,1,figsize=(8,3))
ax.plot(t,z) #z2でも同じ
ax.set_xlim(0,0.01)
plt.savefig("sin_220319_008.png")
plt.show()
#横軸を周波数に縦軸を振幅にするが、ピンクノイズであることがわかりやすいように、x,y軸ともに対数軸にし、yの値は振幅ではなくパワーにしておく
fig,ax = plt.subplots(1,1,figsize=(8,3))
ax.scatter(x,pow_y)
ax.set_yscale('log')
ax.set_xscale("log")
plt.savefig("spectr_220319_008.png")
plt.show()