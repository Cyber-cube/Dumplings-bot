import os
import discord
import json
import time
from discord import app_commands
from discord.ext import commands
from keep_alive import keep_alive
import discord.ui

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
  except Exception as e:
    print(e)
    print("Worked!")

@bot.tree.command(name="ping", description="Pong!")
async def ping(interaction: discord.Interaction):
  latency = round(bot.latency * 1000)
  await interaction.response.send_message(f"Pong! {latency}ms")

class ConfigEmbedModal(discord.ui.Modal, title="Embed config"):
  title_embed = discord.ui.TextInput(label="Embed Title", placeholder="Enter the title of the embed", style=discord.TextStyle.short)
  description = discord.ui.TextInput(label="Embed Description", placeholder="Enter the description of the embed (Use {banana}, and {apple} to display the value of those)", style=discord.TextStyle.long)
  color = discord.ui.TextInput(label="Embed Color", placeholder="Enter the color of the embed", style=discord.TextStyle.short)
  async def on_submit(self, interaction: discord.Interaction):
    with open("config.json") as f:
      config = json.load(f)
    config["embed"]["title"] = str(self.title_embed)
    config["embed"]["description"] = str(self.description)
    config["embed"]["color"] = str(self.color)
    with open("config.json", "w") as f:
      json.dump(config, f, indent=2)
    await interaction.response.send_message("Configuration saved!", ephemeral=True)

class ConfigValueModal(discord.ui.Modal, title="Value configuration"):
  apple = discord.ui.TextInput(label="Apple", placeholder="Enter the value of the apple", style=discord.TextStyle.short)
  banana = discord.ui.TextInput(label="Banana", placeholder="Enter the value of the banana", style=discord.TextStyle.short)
  async def on_submit(self, interaction: discord.Interaction):
    with open("config.json") as f:
      config = json.load(f)
    config["value"]["apple"] = str(self.apple)
    config["value"]["banana"] = str(self.banana)
    with open("config.json", "w") as f:
      json.dump(config, f, indent=2)
    await interaction.response.send_message("Configuration saved!", ephemeral=True)
    
class ConfigLoggingChannelID(discord.ui.Modal, title="Logging channel ID"):
  channel_id = discord.ui.TextInput(label="Channel ID", placeholder="Enter the ID of the channel", style=discord.TextStyle.short, min_length=18, max_length=18)
  async def on_submit(self, interaction: discord.Interaction):
    with open("config.json") as f:
      config = json.load(f)
    config["logging_channel_id"] = str(self.channel_id)
    with open("config.json", "w") as f:
      json.dump(config, f, indent=2)
    await interaction.response.send_message("Configuration saved!", ephemeral=True)
    
class ConfigButtonLabel(discord.ui.Modal, title="Button label"):
  apple = discord.ui.TextInput(label="Apple", placeholder="Enter the label of the apple", style=discord.TextStyle.short)
  banana = discord.ui.TextInput(label="Banana", placeholder="Enter the label of the banana", style=discord.TextStyle.short)
  async def on_submit(self, interaction: discord.Interaction):
    with open("config.json") as f:
      config = json.load(f)
    config["button_label"]["apple"] = str(self.apple)
    config["button_label"]["banana"] = str(self.banana)
    with open("config.json", "w") as f:
      json.dump(config, f, indent=2)
    await interaction.response.send_message("Configuration saved!", ephemeral=True)

@bot.tree.command(name="configure", description="A command used to configure various settings")
async def configure(interaction: discord.Interaction):
  embed = discord.Embed(title="Configure Settings", description="Press the button of the setting you want to configure")
  embed_config = discord.ui.Button(label="Embed Config", style=discord.ButtonStyle.primary)
  value_config = discord.ui.Button(label="Value Config", style=discord.ButtonStyle.primary)
  logging_channel_id = discord.ui.Button(label="Logging Channel ID", style=discord.ButtonStyle.primary)
  button_label = discord.ui.Button(label="Button Label", style=discord.ButtonStyle.primary)
  view = discord.ui.View()
  async def embed_config_callback(interaction):
    await interaction.response.send_modal(ConfigEmbedModal())
  async def value_config_callback(interaction):
    await interaction.response.send_modal(ConfigValueModal())
  async def logging_channel_id_callback(interaction):
    await interaction.response.send_modal(ConfigLoggingChannelID())
  async def button_label_callback(interaction):
    await interaction.response.send_modal(ConfigButtonLabel())
  embed_config.callback = embed_config_callback
  value_config.callback = value_config_callback
  logging_channel_id.callback = logging_channel_id_callback
  button_label.callback = button_label_callback
  view.add_item(value_config)
  view.add_item(logging_channel_id)
  view.add_item(button_label)
  view.add_item(embed_config)
  await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="settings", description="A command used to view the current settings")
async def settings(interaction: discord.Interaction):
  embed = discord.Embed(title="Current Settings", description="Press the buttons to preview the current settings")
  with open("config.json") as f:
    config = json.load(f)
  embed_config = discord.ui.Button(label="Embed Config", style=discord.ButtonStyle.primary)
  value_config = discord.ui.Button(label="Value Config", style=discord.ButtonStyle.primary)
  logging_channel_id = discord.ui.Button(label="Logging Channel ID", style=discord.ButtonStyle.primary)
  button_label = discord.ui.Button(label="Button Label", style=discord.ButtonStyle.primary)
  view = discord.ui.View()
  view.add_item(embed_config)
  view.add_item(value_config)
  view.add_item(logging_channel_id)
  view.add_item(button_label)
  async def embed_config_callback(interaction):
    embed = discord.Embed(title="Embed Config", description="The embed configuration")
    embed.add_field(name="Title", value=config["embed"]["title"])
    embed.add_field(name="Description", value=config["embed"]["description"])
    embed.add_field(name="Color", value=config["embed"]["color"])
    await interaction.response.send_message(embed=embed, ephemeral=True)
  async def value_config_callback(interaction):
    embed = discord.Embed(title="Value Config", description="The value configuration")
    embed.add_field(name="Apple", value=config["value"]["apple"])
    embed.add_field(name="Banana", value=config["value"]["banana"])
    await interaction.response.send_message(embed=embed, ephemeral=True)
  async def logging_channel_id_callback(interaction):
    embed = discord.Embed(title="Logging Channel ID", description="The logging channel ID")
    embed.add_field(name="Channel ID", value=config["logging_channel_id"])
    await interaction.response.send_message(embed=embed, ephemeral=True)
  async def button_label_callback(interaction):
    embed = discord.Embed(title="Button Label", description="The button label configuration")
    embed.add_field(name="Apple", value=config["button_label"]["apple"])
    embed.add_field(name="Banana", value=config["button_label"]["banana"])
    await interaction.response.send_message(embed=embed, ephemeral=True)
  embed_config.callback = embed_config_callback
  value_config.callback = value_config_callback
  logging_channel_id.callback = logging_channel_id_callback
  button_label.callback = button_label_callback
  await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="increase", description="The main command")
async def increase(interaction: discord.Interaction):
  user_id = str(interaction.user.id)
  with open("config.json") as f:
    config = json.load(f)
  logging_channel_id = str(config["logging_channel_id"])
  banana = 1
  apple = 1
  embed = discord.Embed(title=config["embed"]["title"], description=config["embed"]["description"].format(banana=banana, apple=apple), color=int(config["embed"]["color"], 16))
  view = discord.ui.View()
  increase_apple = discord.ui.Button(label=config["button_label"]["apple"], style=discord.ButtonStyle.green)
  increase_banana = discord.ui.Button(label=config["button_label"]["banana"], style=discord.ButtonStyle.green)
  view.add_item(increase_apple)
  view.add_item(increase_banana)
  await interaction.response.send_message(content="Sending...", ephemeral=True)
  msg = await interaction.followup.send(embed=embed, view=view)    
  async def increase_apple_callback(interaction):
    await interaction.response.defer()
    view2 = discord.ui.View()
    yes_button = discord.ui.Button(label="Yes", style=discord.ButtonStyle.green)
    no_button = discord.ui.Button(label="No", style=discord.ButtonStyle.red)
    view2.add_item(yes_button)
    view2.add_item(no_button)
    msg2 = await interaction.followup.send("Are you sure you want to increase the apple value?", view=view2)
    async def yes_button_callback(interaction):
      nonlocal apple
      apple += int(config["value"]["apple"])
      embed.description = config["embed"]["description"].format(banana=banana, apple=apple)
      await msg.edit(embed=embed, view=view)
      await msg2.delete()
      logging_channel = await bot.get_channel(int(logging_channel_id))
      await logging_channel.send(f"{interaction.user.mention} increased the apple value by {config['value']['apple']}\n Now the apple value is {apple}")
    async def no_button_callback(interaction):
      await interaction.response.send_message("Cancelled", ephemeral=True, delete_after=3)
      await msg2.delete()
      logging_channel = await bot.get_channel(int(logging_channel_id))
      await logging_channel.send(f"{interaction.user.mention} cancelled the increase of the apple value")
    yes_button.callback = yes_button_callback
    no_button.callback = no_button_callback
  async def increase_banana_callback(interaction):
    await interaction.response.defer()
    view2 = discord.ui.View()
    yes_button = discord.ui.Button(label="Yes", style=discord.ButtonStyle.green)
    no_button = discord.ui.Button(label="No", style=discord.ButtonStyle.red)
    view2.add_item(yes_button)
    view2.add_item(no_button)
    msg2 = await interaction.followup.send(content="Are you sure you want to increase the banana value?", view=view2, ephemeral=True)
    async def yes_button_callback(interaction):
      nonlocal banana
      banana += int(config["value"]["apple"])
      embed.description = config["embed"]["description"].format(banana=banana, apple=apple)
      await msg.edit(embed=embed, view=view)
      await msg2.delete()
      logging_channel = await bot.get_channel(int(logging_channel_id))
      await logging_channel.send(f"{interaction.user.mention} increased the apple value by {config['value']['apple']}\n Now the apple value is {apple}")
    async def no_button_callback(interaction):
      await interaction.response.send_message("Cancelled", ephemeral=True, delete_after=3)
      await msg2.delete()
      logging_channel = await bot.get_channel(int(logging_channel_id))
      await logging_channel.send(f"{interaction.user.mention} cancelled the increase of the banana value")
    yes_button.callback = yes_button_callback
    no_button.callback = no_button_callback
  increase_apple.callback = increase_apple_callback
  increase_banana.callback = increase_banana_callback

@bot.command()
async def increase(ctx):
  user_id = str(ctx.message.author.id)
  await ctx.message.delete()
  with open("config.json") as f:
    config = json.load(f)
  banana = 1
  apple = 1
  embed = discord.Embed(title=config["embed"]["title"], description=config["embed"]["description"].format(banana=banana, apple=apple), color=int(config["embed"]["color"], 16))
  view = discord.ui.View()
  increase_apple = discord.ui.Button(label=config["button_label"]["apple"], style=discord.ButtonStyle.green)
  increase_banana = discord.ui.Button(label=config["button_label"]["banana"], style=discord.ButtonStyle.green)
  view.add_item(increase_apple)
  view.add_item(increase_banana)
  msg = await ctx.send(embed=embed, view=view)    
  
  async def increase_apple_callback(interaction):
    await interaction.response.defer()
    view2 = discord.ui.View()
    yes_button = discord.ui.Button(label="Yes", style=discord.ButtonStyle.green)
    no_button = discord.ui.Button(label="No", style=discord.ButtonStyle.red)
    view2.add_item(yes_button)
    view2.add_item(no_button)
    msg2 = await interaction.followup.send(content="Are you sure you want to increase the apple value?", view=view2, ephemeral=True)
    async def yes_button_callback(interaction):
      nonlocal apple
      apple += int(config["value"]["apple"])
      embed.description = config["embed"]["description"].format(banana=banana, apple=apple)
      await msg.edit(embed=embed, view=view)
      await msg2.delete()
    async def no_button_callback(interaction): 
      interaction.response.send_message("Cancelled", ephemeral=True)
      msg2.delete()
    yes_button.callback = yes_button_callback
    no_button.callback = no_button_callback
  async def increase_banana_callback(interaction):
    view2 = discord.ui.View()
    yes_button = discord.ui.Button(label="Yes", style=discord.ButtonStyle.green)
    no_button = discord.ui.Button(label="No", style=discord.ButtonStyle.red)
    view2.add_item(yes_button)
    view2.add_item(no_button)
    msg2 = await interaction.followup.send(content="Are you sure you want to increase the banana value?", view=view2, ephemeral=True)
    async def yes_button_callback(interaction):
      nonlocal banana
      banana += int(config["value"]["apple"])
      embed.description = config["embed"]["description"].format(banana=banana, apple=apple)
      await msg.edit(embed=embed, view=view)
      await msg2.delete()
    async def no_button_callback(interaction): 
      interaction.response.send_message("Cancelled", ephemeral=True)
      await msg2.delete()
    yes_button.callback = yes_button_callback
    no_button.callback = no_button_callback
  increase_apple.callback = increase_apple_callback
  increase_banana.callback = increase_banana_callback

  
keep_alive()
bot.run(str(os.environ['TOKEN']))