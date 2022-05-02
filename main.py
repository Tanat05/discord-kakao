import disnake, os
import requests
import asyncio
from disnake.ext import commands
import sys
import argparse
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import cv2
import json



bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
API_URL1 = 'https://dapi.kakao.com/v2/vision/adult/detect'
API_URL2 = 'https://dapi.kakao.com/v2/vision/multitag/generate'
MYAPP_KEY = 'kakao 토큰'


@bot.event
async def on_ready():
    print(bot.user.id)
    print("ready")



@bot.slash_command(name="성인이미지판별",description="성인 이미지나 노출된 이미지 여부를 판단하여 %로 보여줍니다.")
async def adult(inter: disnake.ApplicationCommandInteraction, image_url: str):
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}
    await inter.response.send_message(f"판별중입니다\n기다려 주세요")
    try:
        data = { 'image_url' : f"{image_url}"}
        resp = requests.post(API_URL1, headers=headers, data=data)
        resp.raise_for_status()
        result = resp.json()['result']
        if result['adult'] > result['normal'] and result['adult'] > result['soft']:
            s = f"성인 이미지일 확률이 {format(float(result['adult'])*100)}% 입니다."
        elif result['soft'] > result['normal'] and result['soft'] > result['adult']:
            s = f"노출이 포함된 이미지일 확률이 {format(float(result['soft'])*100)}% 입니다."
        else :
            s = f"일반적인 이미지일 확률이 {format(float(result['normal'])*100)}% 입니다."

    except Exception as e:
        print(str(e))
        s = "검토가 실패하였습니다.\n다시 시도 하시기 바랍니다"
    await inter.channel.send(image_url)
    await inter.channel.send(s)


@bot.slash_command(name="태그생성",description="이미지를 대표하는 태그를 추출해서 출력합니다.")
async def thing(inter: disnake.ApplicationCommandInteraction, image_url: str):
    await inter.response.send_message(f"검출중입니다\n기다려 주세요")
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}

    try:
        data = { 'image_url' : f"{image_url}"}
        resp = requests.post(API_URL2, headers=headers, data=data)
        resp.raise_for_status()
        result = resp.json()['result']
        if len(result['label_kr']) > 0:
            if type(result['label_kr'][0]) != str:
                result['label_kr'] = map(lambda x: str(x.encode("utf-8")), result['label_kr'])
            s = f"이미지를 대표하는 태그는 \"{','.join(result['label_kr'])}\"입니다."
        else:
            s = "이미지로부터 태그를 생성하지 못했습니다."
    
    except Exception as e:
        print(str(e))
        s = "검토가 실패하였습니다.\n다시 시도 하시기 바랍니다"
  
    await inter.channel.send(image_url)
    await inter.channel.send(s)




bot.run("토큰")
