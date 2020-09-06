import requests
import json
from bs4 import BeautifulSoup
n=24;
path="C:\\Users\\lenovo\\Desktop\\"
def is_Chinese(word):
	for ch in word:
		if '\u4e00' <= ch <= '\u9fff':
			return True
		else:
			return False
def song():
	while True:
		header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
		find_url="https://songsearch.kugou.com/song_search_v2?callback=jQuery1124026204225629423705_1587886680855&keyword="
		word=str(input("请输入要下载的歌名:"))
		find_url+=word
		find_url +="&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1587886680857"
		r=requests.get(find_url,headers=header)
		r.encoding=r.apparent_encoding
		#json解析数据
		song_list=[]
		json_str=json.loads(r.text[43:-2])

		print("有以下版本选择：")
		try:
			for i in range(0,10):
				print("第",i,"个:  歌手:",json_str["data"]["lists"][i]["SingerName"],"      ","专辑:",json_str["data"]["lists"][i]["AlbumName"])
		except:
			print("歌名错误，请重试！！")
			continue
		# print(songHash,"   ",songAlbumName)
		

		whichSong=int(input("下载第几个(退出输入0):"))
		if whichSong==0:
			continue
		songHash=json_str["data"]["lists"][int(whichSong)-1]["FileHash"]
		songAlbumName=json_str["data"]["lists"][int(whichSong)-1]["AlbumID"]
		#解析歌曲mp3 JSON数据
		
		find_url="https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19107504082691280329_1588065387895&hash="
		find_url=find_url+str(songHash)+"&album_id="+str(songAlbumName)+"&dfid=1IVAKQ18314p0oHhlF0HgHxz&mid=7f4c879f7ea0aafdc2faaa1914d7d5ee&platid=4&_=1588065387896"
		r=requests.get(find_url,headers=header)
		r.encoding=r.apparent_encoding
		json_str=json.loads(r.text[41:-2])
		songUrl=json_str["data"]["play_url"]
		
		#读取并下载歌曲
		r=requests.get(songUrl,headers=header)
		songName=path+"track"+"0"+str(n)+".mp3"
		# songName=path+word+".mp3"
		with open(songName,'ab')as fp:
			fp.write(r.content)
			fp.flush()
			print("下载成功，请到桌面查看文件！")

		n=n+1

def qumolangma():
	header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
	album_name=str(input("请输入要搜索节目的名字:"))
	album_page=requests.get("https://www.ximalaya.com/search/"+album_name,headers=header)
	album_page.encoding=album_page.apparent_encoding
	bs=BeautifulSoup(album_page.text,"html.parser")
	print("搜索到以下专辑：————————")
	page_data=[]
	count=0
	print(bs.find_all("div",class_="d-i")[1])
	for i in bs.find_all("div",class_="d-i"):
		if count==10:break
		choose_album_name=""
		for j in str(i):
			if is_Chinese(j):
				choose_album_name=choose_album_name+j
		page_data.append(choose_album_name)
		count=count+1
	for i in range(8):
		print(i,":",page_data[i])
	choose=int(input("请选择下载第几个节目："))
	page_url=bs.find_all("a",class_="xm-album-title ellipsis-2")[choose].get("href")
	page_url="https://www.ximalaya.com"+page_url
	listen_page=requests.get(page_url,headers=header)
	bs=BeautifulSoup(listen_page.text,"html.parser")
	song_list=[]
	for i in range(int(bs.find_all("a",class_="page-link _Xo")[-2].span.string)):
		song_page=requests.get(page_url+"p"+str(i+1),headers=header)
		bs=BeautifulSoup(song_page.text,"html.parser")
		
		song_list=song_list+bs.find_all("div",class_="text _Vc")
		# for i in bs.find_all("div",class_="text _Vc"):
			# id=i.a.get("href")[-9:]
			# title=i.a.get("title")
			# song_json=requests.get("https://www.ximalaya.com/revision/play/v1/audio?id="+str(id)+"&ptype=1",headers=header)
			# song_json=json.loads(song_json.text)
			# song_url=song_json["data"]["src"]
				# download=requests.get(song_url,headers=header)
			# print("已成功下载",title)
			# with open("C:\\Users\\lenovo\\Desktop\\喜马拉雅\\"+title+".m4a","wb") as code:


	for i in range(len(song_list)):
		print(i,":",song_list[i].a.get("title"))
	choose_song=str(input("请选择下载第几个节目（全部下载填all）："))
	if choose_song=="all":
		for i in song_list:
			id=i.a.get("href")[i.a.get("href").rfind("/")+1:]
			title=i.a.get("title")
			song_json=requests.get("https://www.ximalaya.com/revision/play/v1/audio?id="+str(id)+"&ptype=1",headers=header)
			song_json=json.loads(song_json.text)
			song_url=song_json["data"]["src"]
			download=requests.get(song_url,headers=header)
			print("已成功下载",title)
			with open(path+"喜马拉雅\\"+title+".m4a","wb") as code:
				code.write(download.content)
	else:
		id=song_list[int(choose_song)].a.get("href")[song_list[int(choose_song)].a.get("href").rfind("/")+1:]
	