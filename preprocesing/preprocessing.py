# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import math
import sys

n=len(sys.argv)
argv=sys.argv

path=argv[1];

def isFloat(str):
    try: 
        float(str)
    except ValueError: 
        return False
    return True

def readData(path):
  df=pd.read_csv(path);
  data=dict();
  for column in df.columns:
    data[column]=np.array(df[column]);
  return data,len(data[list(data.keys())[0]]), len(data.keys())

data,nr,nc=readData(path);

def lietKeCotThieuDuLieu(data):
  rs=[]
  for i in data:
    for j in data[i]:
      if(isFloat(j) and math.isnan(j)):
        rs.append(i)
        break;
  return rs;

def demSoDongThieuDuLieu(data):
  headers=list(data.keys());
  max=0;
  rows=dict();
  for i in headers:
    count=0;
    for j in data[i]:
      if(isFloat(j) and math.isnan(j)):
        count=count+1;
    rows[i]=count;
    if (max<count):
      max=count;
  return rows,max

def timMean(data):
  count=0;
  sum=0;
  for j in data:
    if(isFloat(j) and not math.isnan(j)):
      count=count+1;
      sum=sum+j;
  if(count==0):
    return 0
  return sum/count

def timMedian(lst):
  lst = lst[~np.isnan(lst)]
  n = len(lst)
  s = sorted(lst)
  return (sum(s[n//2-1:n//2+1])/2.0, s[n//2])[n % 2] if n else None

def timMode(L):
  L=[ i for i in L if not isFloat(i) ]
  from collections import Counter
  counter = Counter(L)
  max_count = max(counter.values())
  return [item for item, count in counter.items() if count == max_count]

def dienThongTinThieu(data,type=0):
  cotThieuDuLieu=lietKeCotThieuDuLieu(data)
  for i in cotThieuDuLieu:
    if(data[i].dtype=='object'):
      mode=timMode(data[i])
      for index,j in enumerate(data[i]):
        if(str(j)=='nan'):
          data[i][index]=mode[0];
    elif(type==0):
      mean=timMean(data[i])
      for index,j in enumerate(data[i]):
        if(str(j)=='nan'):
          data[i][index]=mean;
    else:
      median=timMedian(data[i])
      for index,j in enumerate(data[i]):
        if(str(j)=='nan'):
          data[i][index]=median;
  return data;

def getDataRow(data,i):
  headers=list(data.keys());
  rs=list();
  for header in headers:
    rs.append(data[header][i])
  return np.array(rs)

#Số dữ liệu bị thiếu
def missingFromThreshold(data,threshold):
  n=len(data);
  nan=0;
  for index,j in enumerate(data):
      if(str(j)=='nan'):
        nan=nan+1
  if n==0:
    return True;
  if (nan/n)<threshold :
    return True
  else:
    return False;

def deleteRow(data,i):
  headers=list(data.keys());
  for header in headers:
    data[header]=np.delete(data[header], i)
  return data

def deleteColm(data,header):
  del data[header]
  return data;

def deleteRowMissing(data,threshold):
  nr=len(data[list(data.keys())[0]])
  i=0;
  while i<nr:
    #print(getDataRow(data,i)[0])
    row=getDataRow(data,i);
    if(missingFromThreshold(row,threshold)):
      data=deleteRow(data,i);
      i=i-1;
      nr=nr-1;
    i=i+1;

  return data


def deleteColumnMissing(data,threshold):
  headers=list(data.keys());
  for header in headers:
    col=data[header];
    if(missingFromThreshold(col,threshold)):
      data=deleteRow(data,i);
      deleteColm(data,header)
  return data

def trungLap(data1,data2):
  l=len(data1);
  for i in range(0,l):
    if(data1[i]!=data2[i]):
      return False;
  return True;

def xoaTrungLap(data):
  nr=len(data[list(data.keys())[0]]);
  i=0;
  while i<nr:
    row1=getDataRow(data,i);
    j=i+1;
    while j<nr:
      row2=getDataRow(data,j);
      if trungLap(row1,row2) :
        data=deleteRow(data,j);
        j=j-1;
        nr=nr-1;
      j=j+1;
    i=i+1;
  return data;

def chuanHoaMinMax(data):
  maxData=max(data);
  minData=min(data);
  
  for i in range(len(data)):
    temp=(data[i]-minData)/(maxData-minData);
    data=data.astype('float64');
    data[i]=temp
  return data

def chuanHoaZScore(data):
  var=data.var();
  mean= timMean(data);

  for i in range(len(data)):

    temp=(data[i]-mean)/var;
    data=data.astype('float64');
    data[i]=temp

  return data

def run(argv):
  if(argv[2]=='1'):
    print('Các cột bị thiếu dữ liệu: ');
    print(lietKeCotThieuDuLieu(data));
  elif(argv[2]=='2'):
    print('Số dòng bị thiếu dữ liệu');
    print(demSoDongThieuDuLieu(data)[1]);
  elif(argv[2]=='3'):
    if(argv[3]=='1'):
      data2=dienThongTinThieu(data,0);
      df=pd.DataFrame.from_dict(data2);
      df.to_csv(argv[4])
    else:
      data2=dienThongTinThieu(data,1);
      df=pd.DataFrame.from_dict(data2);
      df.to_csv(argv[4])
    print('Điền thông tin thiếu thành công')
    print('Lưu kết quả vào ',argv[4])

  elif(argv[2]=='4'):
    threshold=float(argv[3])
    data2=deleteRowMissing(data,threshold)
    df=pd.DataFrame.from_dict(data2);
    df.to_csv(argv[4])
    print('Xóa những cột dữ liệu bị thiếu dưới mức ',threshold,' thành công.')
    print('Lưu kết quả vào ',argv[4])

  elif(argv[2]=='5'):
    threshold=float(argv[3])
    data2=deleteRowMissing(data,threshold)
    df=pd.DataFrame.from_dict(data2);
    df.to_csv(argv[4])
    print('Xóa những hàng dữ liệu bị thiếu dưới mức ',threshold,' thành công.')
    print('Lưu kết quả vào ',argv[4])

  elif(argv[2]=='6'):
    data2=xoaTrungLap(data);
    df=pd.DataFrame.from_dict(data2);
    df.to_csv(argv[3])
    print('Xóa dữ liệu trùng thành công.')
    print('Lưu kết quả vào ',argv[3])

  elif(argv[2]=='7'):
    data2=data;
    if(argv[3]=='1'):
      data2[argv[4]]=chuanHoaMinMax(data[argv[4]])
      df=pd.DataFrame.from_dict(data2);
      df.to_csv(argv[4])
    elif(argv[3]=='2'):
      data[argv[4]]=chuanHoaZScore(data[argv[4]])
      df=pd.DataFrame.from_dict(data2);
      df.to_csv(argv[4])
    print('Chụẩn hóa thành công.')
    print('Lưu kết quả vào ',argv[4])




    
      

run(argv);