import subprocess
import sys

def instalar_tudo():
    bibliotecas = ['yt-dlp', 'ytmusicapi', 'discord.py', 'aiohttp', 'PyNaCl']
    for lib in bibliotecas:
        try:
            # Tenta importar para ver se já existe
            if lib == 'yt-dlp': import yt_dlp
            elif lib == 'ytmusicapi': from ytmusicapi import YTMusic
            elif lib == 'discord.py': import discord
            # Se não der erro
        except ImportError:
            print(f"Instalando {lib}... Não saia daí! >.<")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

instalar_tudo()

# imports pra hospedagem
import discord
from discord.ext import commands
import datetime
import aiohttp
import yt_dlp  
import asyncio
from ytmusicapi import YTMusic

import asyncio
from ytmusicapi import YTMusic

# Configurações do Bot
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix=".", intents=intents)

#api games
games = 'https://api.rawg.io/api/games?key=coloque sua key'


# Inicialização da API de Música
yt_music = YTMusic()

# Opções de Áudio (FFmpeg e yt-dlp)
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

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
    canal = bot.get_channel(1455999761499951215)
    await canal.send(
        f"Hã?! Mais alguém entrou?! \n"
        f"B-bem... seja bem-vindo(a), {member.display_name}... "
        f"n-não é como se eu estivesse feliz ou algo assim! 🍰"
    )

#Saidas
@bot.event
async def on_member_remove(member:discord.Member):
    canal = bot.get_channel(1456002920087683316)
    await canal.send(
        f"Hmph... então o {member.display_name} foi embora, né? 😒\n"
        f"N-não que eu me importe ou algo assim!\n"
        f"Mas... podia ter ficado pra comer cupcakes... baka. 🧁"
    )


@bot.command()
async def jogo(ctx, *, nome_do_jogo: str):
    url = f"{games}&search={nome_do_jogo}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                dados = await response.json()
                
                if dados.get('results'):
                    jogo_encontrado = dados['results'][0]
                    
                    # Pegando os dados do dicionário
                    titulo = jogo_encontrado.get('name', '???')
                    lancamento = jogo_encontrado.get('released', 'Não disponível')
                    nota = jogo_encontrado.get('metacritic', 'Sem nota')
                    imagem = jogo_encontrado.get('background_image')

                    embed = discord.Embed(title=f"🎮 {titulo}", color=0xff69b4)
                    if imagem: embed.set_image(url=imagem)
                    embed.add_field(name="📅 Lançamento", value=lancamento, inline=True)
                    embed.add_field(name="🏆 Metacritic", value=nota, inline=True)
                    embed.set_footer(text="Não que eu me importe, mas aqui está! >.<")

                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Não encontrei nada! Você inventou esse nome? 💢")



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

@bot.command()
async def hug(ctx):
    async with aiohttp.ClientSession() as session:
        # Fazendo a requisição para a API
        async with session.get('https://nekos.best/api/v2/hug') as response:
            if response.status == 200:
                data = await response.json()
                result = data['results'][0]
                
                embed = discord.Embed(
                    title=f"{ctx.author.name} deu um abraço!",
                    color=discord.Color.random()
                )
                embed.set_image(url=result['url'])
                embed.set_footer(text=f"Anime: {result['anime_name']}")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Erro ao acessar a API :(")
#musica
@bot.command()
async def tocar(ctx, *, busca: str):
    # Reação inicial da Natsuki
    await ctx.send(f"Hmph... espera um pouco, estou a procurar essa tal de '{busca}'... não é como se eu não tivesse nada mais importante para fazer! 🙄")
    
    try:
        resultado = yt_music.search(busca, filter="songs", limit=1)
        
        if not resultado:
            await ctx.reply("Argh! Não encontrei nada! Tens a certeza que isso é uma música ou acabaste de inventar? >.<")
            return
            
        musica = resultado[0]
        titulo = musica['title']
        artista = musica['artists'][0]['name']
        video_id = musica['videoId']
        link = f"https://music.youtube.com/watch?v={video_id}"

        thumbnail = musica['thumbnails'][-1]['url']

        embed = discord.Embed(
            title=f"🎵 {titulo}",
            description=f"Artista: **{artista}**\n\nN-não é como se eu quisesse ouvir isto contigo, mas aqui tens o link: [YouTube Music]({link})",
            color=0xff0000
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text="Vê se não me interrompes enquanto estou a ler o meu mangá! 🧁")

        await ctx.reply(embed=embed)
        
    except Exception as e:
        await ctx.send(f"E-Ei... algo correu mal. A culpa é tua, de certeza! Erro: {e}")
#entrar no canal de musica
bot.command()
async def entrar(ctx):
    if ctx.author.voice: # Verifica se tu estás numa call
        canal = ctx.author.voice.channel()
        await canal.connect()
        await ctx.send(f"Hmph! Já que insistes tanto, eu entrei no canal **{canal}**... mas não te habitues! 🙄")
    else:
        await ctx.send("Como é que queres que eu entre numa call se nem tu estás lá? És totó? >.<")

@bot.command()
async def play(ctx, *, busca: str):
    ID_CANAL_VOZ = 1456187955613008017
    canal = bot.get_channel(ID_CANAL_VOZ)

    # Conectar ao canal se não estiver lá
    if not ctx.voice_client:
        vc = await canal.connect()
    else:
        vc = ctx.voice_client

    # Lógica de busca e extração do áudio
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{busca}", download=False)
        url_audio = info['entries'][0]['url']
        titulo = info['entries'][0]['title']

    # Iniciar a reprodução
    vc.play(discord.FFmpegPCMAudio(url_audio, **FFMPEG_OPTIONS))
    await ctx.send(f"Hmph! Tocando **{titulo}**... baka! 🎵")

@bot.command()
async def pausar(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Pausado! ⏸️ Não penses que podes descansar para sempre, seu preguiçoso! >.<")
    else:
        await ctx.send("Mas nem sequer está a tocar nada! Estás a tentar enganar-me? 💢")
@bot.command()
async def retomar(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Finalmente! ▶️ Estava a ficar farta de esperar por ti. Vamos continuar!")
    else:
        await ctx.send("A música não está pausada, baka! Ouve com mais atenção! 🙄")

@bot.command()
async def parar(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Parou! ⏹️ Já chega de música por hoje, tenho mangás para ler! 😤")
    else:
        await ctx.send("Eu nem sequer estou no canal de voz... és totó? 😒")

@bot.command()
async def sair(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Finalmente! 😤 Não aguentava mais ficar aqui com você. Tchau! baka! 🍰")
    else:
        await ctx.send("Eu nem estou em uma call, seu idiota! 💢")


bot.run('coloque o seu')
