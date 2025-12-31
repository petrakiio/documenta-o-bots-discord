import discord
from discord.ext import commands
import datetime
import aiohttp

intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def ola(ctx:commands.context):
    user = ctx.author
    await ctx.reply(f'E-ei! N-não é como se eu estivesse feliz em te ver ou algo assim, tá?!\nMas bem olá {user}')

@bot.command()
async def somar(ctx:commands.context,n1:float,n2:float):
    res = n1 + n2
    user = ctx.author
    await ctx.reply(f'Você não consegue somar sozinho?!\nVocê é um idiota {user},bem eu somei pra você o resultado é {res}')

@bot.command()
async def falar(ctx:commands.context,*,frase):
    await ctx.send(frase)

@bot.event
async def on_message(msg:discord.Message):
    autor = msg.author
    if autor.bot:
        return
    if "adm" in msg.content.lower():
        await msg.reply("Não fale do adm seu idiota!")
    await bot.process_commands(msg)

# Boas-vindas 
@bot.event
async def on_member_join(member: discord.Member):
    canal = bot.get_channel('mude para o seu')
    await canal.send(
        f"Hã?! Mais alguém entrou?! \n"
        f"B-bem... seja bem-vindo(a), {member.display_name}... "
        f"n-não é como se eu estivesse feliz ou algo assim! 🍰"
    )

#Saidas
@bot.event
async def on_member_remove(member:discord.Member):
    canal = bot.get_channel('mude para o seu')
    await canal.send(
        f"Hmph... então o {member.display_name} foi embora, né? 😒\n"
        f"N-não que eu me importe ou algo assim!\n"
        f"Mas... podia ter ficado pra comer cupcakes... baka. 🧁"
    )

@bot.command()
async def enviar(ctx):
    embed = discord.Embed(
        title="Ei, seu idiota!",
        description="N-não pensa que eu fiz isso porque gosto de você, tá?! 😠🧁",
        color=0xff69b4
    )
    embed.set_footer(text="— Natsuki")

    await ctx.reply(embed=embed)
@bot.command()
async def banir(ctx, membro: discord.Member, *, motivo="Ninguém mandou ser um idiota!"):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("Ei! Você não tem autoridade para banir ninguém aqui! O que pensa que está fazendo? >.<")
        return
    if membro == ctx.author:
        await ctx.send("Você quer se banir? Argh, você é mais estranho do que eu pensava...")
        return
    try:
        await membro.ban(reason=motivo)
        await ctx.send(f"Pronto! {membro.display_name} foi banido. {motivo}. Já vai tarde! 😤")
    except Exception as e:
        await ctx.send(f"E-Ei... algo deu errado. Não consegui banir esse idiota. Erro: {e}")

import datetime

@bot.command()
async def cascudo(ctx, membro: discord.Member, minutos: int = 5, *, motivo="Para de ser chato!"):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("Ei! Quem você acha que é para dar cascudo nos outros? Só eu posso ser brava aqui! >.<")
        return

    try:
        tempo = datetime.timedelta(minutes=minutos)
        await membro.timeout(tempo, reason=motivo)
        
        await ctx.send(f"Toma essa! 👊 {membro.display_name} levou um cascudo e vai ficar quietinho por {minutos} minutos. Motivo: {motivo}. Vê se aprende!")
    except Exception as e:
        await ctx.send(f"Argh! Não consegui dar o cascudo. Você configurou as permissões do meu cargo direito? Erro: {e}")

@bot.command()
async def desculpar(ctx, membro: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("Você nem deu o cascudo, então não pode tirar! Idiota!")
        return

    try:
        await membro.timeout(None)
        await ctx.send(f"Hmph. Sorte sua, {membro.display_name}. Foi perdoado... desta vez! Mas não me irrite de novo!")
    except Exception as e:
        await ctx.send(f"Não consegui perdoar... talvez ele mereça ficar assim! Erro: {e}")

@bot.command()
async def limpar(ctx, quantidade: int):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("Você não manda em mim! Não vai apagar nada! >.<")
        return

    try:
        deleted = await ctx.channel.purge(limit=quantidade + 1)
        await ctx.send(f"Pronto, seu bobo! Apaguei {len(deleted)-1} mensagens. Vê se mantém o chat limpo agora! 😤", delete_after=5)
    except Exception as e:
        await ctx.send(f"Argh, deu erro: {e}")

@bot.command()
async def pokemon(ctx, nome: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await ctx.send(f"Argh! Esse Pokémon não existe! Você escreveu certo, seu bobo? >.<")
                return
            
            data = await response.json()
            
            nome_poke = data['name'].capitalize()
            id_poke = data['id']
            tipo = data['types'][0]['type']['name']
            altura = data['height'] / 10 # converter para metros
            peso = data['weight'] / 10 # converter para kg
            sprite = data['sprites']['front_default']

            embed = discord.Embed(
                title=f"📋 Ficha do {nome_poke} (No. {id_poke})",
                color=0xFF0000
            )
            embed.set_thumbnail(url=sprite)
            embed.add_field(name="Tipo", value=tipo.capitalize(), inline=True)
            embed.add_field(name="Altura", value=f"{altura}m", inline=True)
            embed.add_field(name="Peso", value=f"{peso}kg", inline=True)
            embed.set_footer(text="Não que eu goste de Pokémon, mas esse é fofinho... só um pouco!")

            await ctx.send(embed=embed)

@bot.command()
async def calculadora(ctx:commands.context,n1:float,n2:float,opr:str):
    if opr == '+':
        n = n1 +n2
        await ctx.reply(f'Idiota,seu resultado é:{n}')
    elif opr == '-':
        n = n1 - n2
        await ctx.reply(f'Idiota,seu resultado é:{n}')
    elif opr == '/':
        n = n1 / n2
        await ctx.reply(f'Idiota,seu resultado é:{n}')
    elif opr == '*':
        n = n1 * n2
        await ctx.reply(f'Idiota,seu resultado é:{n}')
    else:
        await ctx.send('Me de uma operador decente idiota')

bot.run('Mude para o seu!')
