import discord
from discord.ext import commands
from discord.ui import Button, View

import config
from google_api import get_next_row, get_sheet
import asyncio
from async_timeout import timeout
from datetime import datetime
import db
import json


class StartView(View):
    def __init__(self, root_channel, bot, timeout: float | None = 180): 
        super().__init__(timeout=timeout)
        self.question_index = 0
        self.root_channel = root_channel
        self.bot = bot

        self.next_question_button = Button(
            custom_id="next",
            label="Следующий вопрос",
            style=discord.ButtonStyle.green,
        )
        self.next_question_button.callback = self.next_question_button_callback

        self.comprehension_button = Button(
            custom_id="comprehension",
            label="Спросить, все ли понятно на занятии",
            style=discord.ButtonStyle.green,
        )
        self.comprehension_button.callback = self.comprehension_button_callback

        self.final_button = Button(
            custom_id="final",
            label="Закончить занятие",
            style=discord.ButtonStyle.green,
        )
        self.final_button.callback = self.final_button_callback

        self.add_item(self.next_question_button)
        self.add_item(self.comprehension_button)
        self.add_item(self.final_button)


    async def next_question_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        sheet = get_sheet()
        question = get_next_row(sheet[0], self.question_index)

        if question is not None:
            self.question_index += 1
            if question[1]:
                time = str(datetime.now())
                answers = []
                users = set()
                button1 = Button(custom_id="1", label="1", style=discord.ButtonStyle.green)
                async def button1_callback(interaction: discord.Interaction):
                    result = 0
                    if interaction.data["custom_id"] == question[2]:
                        result = 1
                    if interaction.user.id not in users:
                        users.add(interaction.user.id)
                        result = 0
                        if interaction.data["custom_id"] == question[2]:
                            result = 1
                        answers.append({interaction.user.id: [interaction.user.name, interaction.data["custom_id"], result]})
                        await interaction.response.send_message("Ответ отправлен!", ephemeral=True)
                    else:
                        for i in range(len(answers)):
                            if list(answers[i].keys())[0] == interaction.user.id:
                                answers.pop(i)
                        answers.append({interaction.user.id: [interaction.user.name, interaction.data["custom_id"], result]})
                        await interaction.response.send_message("Вы уже ответили!", ephemeral=True)

                button1.callback = button1_callback

                button2 = Button(custom_id="2", label="2", style=discord.ButtonStyle.green)
                async def button2_callback(interaction: discord.Interaction):
                    result = 0
                    if interaction.data["custom_id"] == question[2]:
                        result = 1
                    if interaction.user.id not in users:
                        users.add(interaction.user.id)
                        result = 0
                        if interaction.data["custom_id"] == question[2]:
                            result = 1
                        answers.append({interaction.user.id: [interaction.user.name, interaction.data["custom_id"], result]})
                        await interaction.response.send_message("Ответ отправлен!", ephemeral=True)
                    else:
                        for i in range(len(answers)):
                            if list(answers[i].keys())[0] == interaction.user.id:
                                answers.pop(i)
                        answers.append({interaction.user.id: [interaction.user.name, interaction.data["custom_id"], result]})
                        await interaction.response.send_message("Вы уже ответили!", ephemeral=True)

                button2.callback = button2_callback

                button3 = Button(custom_id="3", label="3", style=discord.ButtonStyle.green)
                async def button3_callback(interaction: discord.Interaction):
                    result = 0
                    if interaction.data["custom_id"] == question[2]:
                        result = 1
                    if interaction.user.id not in users:
                        users.add(interaction.user.id)
                        result = 0
                        if interaction.data["custom_id"] == question[2]:
                            result = 1
                        answers.append({interaction.user.id: [interaction.user.name, interaction.data["custom_id"], result]})
                        await interaction.response.send_message("Ответ отправлен!", ephemeral=True)
                    else:
                        for i in range(len(answers)):
                            if list(answers[i].keys())[0] == interaction.user.id:
                                answers.pop(i)
                        answers.append({interaction.user.id: [interaction.user.name, interaction.data["custom_id"], result]})
                        await interaction.response.send_message("Вы уже ответили!", ephemeral=True)
                
                button3.callback = button3_callback

                button4 = Button(custom_id="4", label="4", style=discord.ButtonStyle.green)
                async def button4_callback(interaction: discord.Interaction):
                    result = 0
                    if interaction.data["custom_id"] == question[2]:
                        result = 1
                    if interaction.user.id not in users:
                        users.add(interaction.user.id)
                        answers.append({interaction.user.id: [interaction.user.name, interaction.data["custom_id"], result]})
                        await interaction.response.send_message("Ответ отправлен!", ephemeral=True)
                    else:
                        for i in range(len(answers)):
                            if list(answers[i].keys())[0] == interaction.user.id:
                                answers.pop(i)
                        answers.append({interaction.user.id: [interaction.user.name, interaction.data["custom_id"], result]})
                        await interaction.response.send_message("Ответ перезаписан!", ephemeral=True)

                button4.callback = button4_callback

                view = View()
                view.add_item(button1)
                view.add_item(button2)
                view.add_item(button3)
                view.add_item(button4)

                msg = await self.root_channel.send(embed=discord.Embed(
                    title=("❔ " + question[0]),
                    description=(question[1] + "\nДается 60 секунд на ответ")),
                    view=view
                    )
                await asyncio.sleep(60)
                await self.root_channel.send(f"Ответы приняты! Правильный ответ: {question[2]}")
                button1.disabled = True
                button2.disabled = True
                button3.disabled = True
                button4.disabled = True
                await msg.edit(embed=discord.Embed(
                    title=("❔ " + question[0]),
                    description=(question[1] + "\nДается 60 секунд на ответ")),
                    view=view)
                db.db_append(question[0], question[2], json.dumps(answers), time)

            else:
                time = str(datetime.now())
                answers = []
                users = set()
                await self.root_channel.send(embed=discord.Embed(title=("❔ " + question[0]), description=("Пиши ответ в чат! Дается 60 секунд на ответ")))
                await asyncio.sleep(2)
                def check(message):
                    if message.author.id not in users:
                        users.add(message.author.id)
                        result = 0
                        if message.content == question[2]:
                            result = 1
                        answers.append({message.author.id: [message.author.name, message.content, result]})
                    return True

                try:
                    async with timeout(60):
                        while True: 
                            msg = await self.bot.wait_for('message', check=check)
                            await msg.delete()
                except asyncio.TimeoutError:
                    await self.root_channel.send(f"Ответы приняты! Правильный ответ: {question[2]}")
                db.db_append(question[0], question[2], json.dumps(answers), time)

        else:
            await self.root_channel.send("Вопросы закончились!")


    async def final_button_callback(self, interaction: discord.Interaction):
        users = set()
        self.comprehension_button.disabled = True
        self.final_button.disabled = True
        self.next_question_button.disabled = True
        await interaction.response.edit_message(embed=discord.Embed(title="Выберете действие!", color=0x563196), view=self)

        rates = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        button1 = Button(custom_id="1", label="1", style=discord.ButtonStyle.green)
        async def button1_callback(interaction: discord.Interaction):
            if interaction.user.id not in users:
                users.add(interaction.user.id)
                await interaction.response.send_message("Cпасибо за участие!", ephemeral=True)
                rates["1"] += 1
            else:
                await interaction.response.send_message("Вы уже проголосовали!", ephemeral=True)
        button1.callback = button1_callback

        button2 = Button(custom_id="2", label="2", style=discord.ButtonStyle.green)
        async def button2_callback(interaction: discord.Interaction):
            if interaction.user.id not in users:
                users.add(interaction.user.id)
                await interaction.response.send_message("Cпасибо за участие!", ephemeral=True)
                rates["2"] += 1
            else:
                await interaction.response.send_message("Вы уже проголосовали!", ephemeral=True)
        button2.callback = button2_callback

        button3 = Button(custom_id="3", label="3", style=discord.ButtonStyle.green)
        async def button3_callback(interaction: discord.Interaction):
            if interaction.user.id not in users:
                users.add(interaction.user.id)
                await interaction.response.send_message("Cпасибо за участие!", ephemeral=True)
                rates["3"] += 1
            else:
                await interaction.response.send_message("Вы уже проголосовали!", ephemeral=True)
        button3.callback = button3_callback

        button4 = Button(custom_id="4", label="4", style=discord.ButtonStyle.green)
        async def button4_callback(interaction: discord.Interaction): 
            if interaction.user.id not in users:
                users.add(interaction.user.id)
                await interaction.response.send_message("Cпасибо за участие!", ephemeral=True)
                rates["4"] += 1
            else:
                await interaction.response.send_message("Вы уже проголосовали!", ephemeral=True)
        button4.callback = button4_callback

        button5 = Button(custom_id="5", label="5", style=discord.ButtonStyle.green)
        async def button5_callback(interaction: discord.Interaction):
            if interaction.user.id not in users:
                users.add(interaction.user.id)    
                await interaction.response.send_message("Cпасибо за участие!", ephemeral=True)
                rates["5"] += 1
            else:
                await interaction.response.send_message("Вы уже проголосовали!", ephemeral=True)
        button5.callback = button5_callback

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)
        msg = await self.root_channel.send(embed=discord.Embed(title="❔ Насколько вам понравилось занятие?"), view=view)
        await asyncio.sleep(10)
        button1.disabled = True
        button2.disabled = True
        button3.disabled = True
        button4.disabled = True
        button5.disabled = True
        await msg.edit(embed=discord.Embed(title="❔ Насколько вам понравилось занятие?"), view=view)
        result_grades = []
        for k, v in rates.items():    
            result_grades.append(f"{k}:{v}")
        with open(f"{datetime.now()}.txt", "w") as file:
            file.write("\n".join(result_grades))


    async def comprehension_button_callback(self, interaction: discord.Interaction):
        msg = await self.root_channel.send(embed=discord.Embed(title="❔ Все ли понятно? Голосуй с помощью эмоджи!"))
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

        await interaction.response.defer()


bot = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix=config.PREFIX,
)


@bot.event
async def on_ready():
    get_sheet()
    db.db_init()
    try:
        print("Bot is ups and ready!")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as ex:
        print(ex)


@bot.tree.command(name="start")
async def info(interaction):
    root_channel = bot.get_channel(interaction.channel_id)
    view = StartView(root_channel, bot)
    await interaction.response.send_message(embed=discord.Embed(title="Выберете действие!", color=0x563196), view=view, ephemeral=True)


bot.run(config.TOKEN)
