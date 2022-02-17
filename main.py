import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

client = discord.Client()

append_words = ["雜草是"]

append_r = [
  "xd",
  "雜草"
]

if "responding" not in db.keys():
  db["responding"] = True

eightb_words = ["g$八號球"]

eightb_r = [
  "這是必然",
  "肯定是的",
  "不用懷疑",
  "毫無疑問",
  "你能依靠它",
  "看起來不錯",
  "聽起來很不錯",
  "是的",
  "種種跡象指出「是的」",
  "回覆籠統，再試試",
  "待會再問",
  "最好現在不告訴你",
  "現在無法預測",
  "專心再問一遍",
  "想的美",
  "我的回覆是「不」",
  "我的來源說「不」",
  "前景不太好",
  "很可疑"
]

def get_quote():
  response = requests.get("http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_words(dumb_messages):
  if "words" in db.keys():
    words = db["words"]
    words.append(dumb_messages)
    db["words"] = words
  else:
    db["words"] = [dumb_messages]
  
def delete_word(index):
  words = db["words"]
  if len(words) > index:
    del words[index]
    db["words"] = words

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("g$hello"):
    await message.channel.send("Hello!")

  elif msg.startswith("屌你老母"):
    await message.channel.send("芝士漢堡")
      
  elif msg.startswith("g$inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  elif msg.startswith("g$i love you"):
    await message.channel.send("I love you too :hearts: !")

  if any(word in msg for word in eightb_words):
      await message.channel.send(random.choice(eightb_r))

  if db["responding"]:
    options = append_r
    if "words" in db.keys():
      options.extend(db["words"])

    if any(word in msg for word in append_words):
      await message.channel.send(random.choice(options))

    if msg.startswith("g$new"):
        dumb_messages = msg.split("g$new ",1)[1]
        update_words(dumb_messages)
        await message.channel.send("New quotes added")

    if msg.startswith("g$del"):
        words = []
        if "words" in db.keys():
          index = int(msg.split("g$del",1)[1])
          delete_word(index)
          words = db["words"]
        await message.channel.send(words)

    if msg.startswith("g$list"):
      words = []
      if "words" in db.keys():
        words = db["words"]
      await message.channel.send(words)

  if msg.startswith("g$responding"):
    value = msg.split("g$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("responding is off.")


os.environ['token']
keep_alive()
client.run(os.getenv('token'))