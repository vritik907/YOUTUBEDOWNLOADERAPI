from pytube import YouTube
from aiohttp import web  
import ffmpeg ,json
import subprocess
import os , random , string


# init yt itags 
# itags = {"144p":{"mp4":160,"3gp":17,"webm":219},"180p":{"3pg":36,},"240":{"flv":5,"hls":92,"mp4":133,"webm":242},"270p":{"flv":6,""},"360":{"mp4":18,"flv":34,"webm":43,"hls":93,},"480p":,"720p":,"1080p":,"1440p":,"2160p":,"3072p":}
# itags60fps = {"144p":{"webm":330},"240":{"webm"331},"360":43,"480p":,"720p":,"1080p":,"1440p":,"2160p":,"3072p":}

# random yt video url https://www.youtube.com/shorts/0L7f38nqFXc
def randomString():
	return random.choices(string.ascii_uppercase + string.ascii_lowercase,k=5)



	
routes = web.RouteTableDef()
@routes.get("/")
async def ytDownload(request):
	try:
		if not os.path.exists("./downloads"):
			os.makedirs("./downloads")
		else:
			pass
		# removing all unwanted videos 
		if len(os.listdir("./downloads")) > 3:
			for dfile in os.listdir("./downloads"):
				try:
					with open(f"./downloads/{dfile}" , "r") as datafile:
						os.remove(f"./downloads/{dfile}")
				except IOError:
					pass
		else:
			pass
		# getting requited data 
		video_url = request.query["url"]
		res = request.query["format"]
		# main section
		yt = YouTube(video_url)
		if res == "audio":
			stream = yt.streams.filter(only_audio = True).first()
			# making stream file name without space
			stream_name = "".join(randomString()) + stream.default_filename.replace(" ","")
			stream.download("./downloads" ,filename=stream_name)
			output_fileName = stream_name.split(".")[0] + ".mp3"
			subprocess.run(f"ffmpeg -i ./downloads/{stream_name} ./downloads/{output_fileName} -y",shell=True)
			os.remove(f"./downloads/{stream_name}")
			afile = open(f"./downloads/{output_fileName}" , "rb")
			return web.Response( body=afile, status=200, reason="audio stream found",headers=None, )

		else:
			for stream in yt.streams:
				if stream.resolution == res:
					stream_name = "".join(randomString()) + stream.default_filename.replace(" ","")
					# progressive streams means sutable of one screen size but here it is reffered for low quality and with both audio and video containing streams 
					if stream.is_progressive:
						stream.download("./downloads",filename=stream_name)
						outfile_name = stream_name
					else:
						# if we got video without audio so we have to merge them after download
						# downloading video 
						stream.download('./downloads',filename=stream_name) 
						# downloading audio 
						audio_file  = yt.streams.filter(only_audio = True).first()
						audio_name = "".join(randomString()) + audio_file.default_filename.replace(" ","")
						audio_file.download("./downloads",filename=audio_name)

						input_video = ffmpeg.input(f'./downloads/{stream_name}')
						input_audio = ffmpeg.input(f'./downloads/{audio_name}')
						outfile_name = "adaptive"+stream_name.split(".")[0] + ".mp4"
						ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'./downloads/{outfile_name}').run(cmd=['ffmpeg',"-y"])
						# deleting audio and vidiows seprate files 
						os.remove(f"./downloads/{stream_name}")
						os.remove(f"./downloads/{audio_name}")

					f = open(f"./downloads/{outfile_name}" , "rb")
					return web.Response( body=f, status=200, reason="stream found",headers=None)

				
				

		data= {
			'status':False,
			'reason':"stream not found"
		}
		return web.json_response(data, text=None, body=None, status=400, reason="stream not found",
              headers=None, content_type='application/json', dumps=json.dumps)
	except:
		data = {
			"status":"running"
		}
		return web.json_response(data, text=None, body=None, status=400, reason="no proper parameters",
              headers=None, content_type='application/json', dumps=json.dumps)




@routes.get("/details")
async def ytDetails(request):
	try:
		video_url = request.query["url"]
		yt = YouTube(video_url)
		data = {
			"status":True,
			"title": yt.title,
			"thumbnail_url": yt.thumbnail_url
		}
		return web.json_response(data, text=None, body=None, status=200, reason="get proper YouTube url",
              headers=None, content_type='application/json', dumps=json.dumps)

	except:
		data = {
			"status":False,
			"resion":"may be url is wrong and not supported"
		}
		return web.json_response(data, text=None, body=None, status=400, reason="no proper url",
              headers=None, content_type='application/json', dumps=json.dumps)



async def create_app():
	app = web.Application()
	app.add_routes(routes)
	return app


if __name__ == "__main__":
	# initilizing downloads directory
	port = int(os.environ.get('PORT', 8000))
	web.run_app(create_app() ,port=port)





