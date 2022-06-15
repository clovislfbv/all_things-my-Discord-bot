import discord
from discord.ext import commands, tasks
from youtube_dl import *
import asyncio
from random import randint, choice, shuffle
import urllib.parse, urllib.request, re
from time import sleep
import logging
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import requests
import shutil
from gtts import gTTS
from time import sleep
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
import jokes
import blague

bot = commands.Bot(command_prefix="$", description = "Bot créé par Clovis!")
musics = {}
ytdl = YoutubeDL()
client = discord.Client()
url_queue = []
message_skip = 0
message_channel = 0
playing = 0
pays = {"FR" : '37i9dQZEVXbIPWwFssbupI?si=1e836528e2384a70', "UK" : "37i9dQZEVXbLnolsZ8PSNw?si=bcc5a83311b54e67", "USA" : "37i9dQZEVXbLRQDuF5jeBp?si=0b5e105bed784940",  "WORLD" : '37i9dQZEVXbMDoHDwVN2tF?si=510c4902c6ba4d80', "ES" : "37i9dQZEVXbNFJfN1Vw8d9?si=3087bda4c2df4961", "IN" : "37i9dQZEVXbLZ52XmnySJg?si=085b180ae65b4609", "PH" : "37i9dQZEVXbNBz9cRCSFkY?si=b30c3057903f4ef5", "TU" : "37i9dQZEVXbIVYVBNw9D5K?si=3f4a25f140904d2f", "JA" : "37i9dQZEVXbKXQ4mDTEBXq?si=5971ca3ffc744d15", "PB" : "37i9dQZEVXbKCF6dqVpDkS?si=0b8e08dc941e4b47", "IT" : "37i9dQZEVXbIQnj7RRhdSX?si=3d1f7cb768e14959", "RU" : "37i9dQZEVXbL8l7ra5vVdB?si=28dc400fabb8424b"}
current_music = ""
dict_words = {"Das Gen(-e)" : "le gène", "Gentechnisch" : "génétique", "Gentechnikfrei, ohne gentechnik" : "sans OGM", "Das Nachrungsmittel(-), das lebensmittel(-)" : "la nourriture", "Das Genfood" : "les aliments génétiquement modifiés", "Das Produkt(-e)" : "le produit", "Die Kennzeichnung" : "l’étiquetage", "Etwas kategorisch/vehement ablehnen" : "refuser quelque chose de catégorique", "Die Ablehnung" : "le refus", "Der/die Verbraucher/in" : "le consommateur", "Vor etwas Angst haben" : "avoir peur pour quelque chose", "Falsche ausreichende informationen verbreiten" : "diffuser de fausses informations suffisantes", "Eine Gefahr für Gesundheit und Umwelt" : "Un danger pour la santé et l'environnement", "Das Risiko" : "le risque", "Etwas verteufeln" : "diaboliser quelque chose", "Panik auslösen" : "causer la panique", "Die Antibiotikaresistenz" : "résistance aux antibiotiques", "Neue Allergie auslösen" : "déclencher une nouvelle allergie", "Zum Wohl der Menscheit und Umwelt" : "pour le bien de l'humanité et de l'environnement", "Die Nature schützen" : "protéger la nature", "Die Klimawandel" : "le changement climatique", "Die Versorgung mit Narungsmitteln" : "l'approvisionnement en nourriture", "Die Skepsis" : "le sceptisme", "Offen gegenüber etwas sein" : "être ouvert à propos de quelque chose", "Über etwas diskutieren" : "discuter de quelque chose", "Der Nachweis" : "les preuves", "Wissenschaftliche Erkenntnisse" : "les résultats scientifiques", "Die Unbedenklichkeit" : "l’absence de danger", "Unbedenklich" : "inoffensif", "Kurzfristig" : "à court terme", "Vorsichtsmaßnahmen engreifen" : "prendre des précautions", "Demonstrieren" : "démontrer", "Mehr transparenz fordern" : "demander plus de transparence", "Das klonen = die künstliche Erzeugung eines Menschen" : "le clonage", "Klonen = duplizieren" : "dupliquer", "Identische Menschen herstellen" : "créer des personnes identiques", "Der Klonversuch" : "L'expérience du clonage", "Die Genforschung" : "la recherche génétique", "Die Gentechnik" : "le génie génétique", "Die Genmanipulation" : "La manipulation génétique", "die Gene untersuchen" : "Examiner les gènes", "Neue Möglichkeiten eröffnen" : "ouvrir de nouvelles perspectives", "Genetische Fehler korrigieren" : "corriger les erreurs génétiques",  "Unheilbare Krankheiten / Erbkrankheiten / Behinderungen verhindern" : "prévention des handicaps", "Gesundheitskoten einsparen" : "réduire les coûts des soins de santé", "Die Schwangerschaft(-en)" : "la grossesse", "Der Embryo" : "l'embryon", "Gesunde / perfekte Babys herstellen" : "faire des bébés en bonne santé", "Genies reproduzieren" : "reproduire des génies", "Das Leben verlängern" : "prolonger la vie", "Die Gefahr" : "le danger", "Das Risiko" : "le risque", "Embryonen herstellen" : "créer des embryons", "Embyonen zerstören" : "détruire des embryons", "Als Organlieferant dienen" : "donneur d'organes", "Die künstliche Selektion" : "la sélection artificielle", "Lebenswerte Menschen oder Eigenschaften auswählen" : "sélectionnez les personnes ou les caractéristiques pour lesquelles il vaut la peine de vivre", "Der Eingriff in die (menschliche) Nature" : "l'intervention dans la nature", "Gott spielen" : "jouer Dieu", "Skrupellos sein" : "être sans scrupules", "Skrupel haben" : "avoir des scrupules", "Durch ein Gesetz kontrollieren" : "contrôler par la loi", "regulieren" : "réglementer", "Erlauben" : "Autoriser", "verbieten" : "interdire", "Ein ethisches Problem darstellen" : "Présenter un problème éthique"}
liste_words = []

for cle in dict_words.keys():
    liste_words.append(cle)

def my_hook(d):
    if d['status'] == 'downloading':
        print ("downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%")
    if d['status'] == 'finished':
        filename=d['filename']
        print(filename)

ydl_opts = {
    'format': 'bestvideo[width<=1080]+bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'progress_hooks': [my_hook]
}

@bot.event
async def on_ready():
    print("Ready")
    changeStatus.start()

status = ["$help", "surpasser Bomboclaat Bot", "$aide"]

'''
def messages(ctx, message):
    print(message)
    if message.content == "hello" or message.content == "hi" or message.content == "Hello" or message.content == "HELLO" or message.content == "HI":
        asyncio.run_coroutine_threadsafe(ctx.send("hello"), bot.loop)'''

allowed_channels = [796137851972485151, 697492398070300763, 796731890630787126, 631935311592554636] #["🤖・cow-bip-bop-bots", "bruh-botsandmusic", "test-bot", "général de mon propre serveur"]

def checks_in_bot_channel(channels, channel):
    global allowed_channels
    for i in range(len(allowed_channels)):
        channel_id = allowed_channels[i]
        print(channel_id, channel)
        if channel_id == channel:
            return True
    return False

@bot.command()
async def get_id_channels(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        channel = discord.utils.get(ctx.guild.channels, name= "🤖・cow-bip-bop-bots")
        channel_id = channel.id
        await ctx.send(channel_id)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

'''
@bot.event
async def on_command_error(ctx, error):
    # coding: utf-8
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Dsl mon gars, la commande que t'as écrite existe peut être dans tes rêves mais elle n'existe pas dans la réalité")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Dsl mec mais t'as pas les permissions d'utiliser cette commande.")
    elif isinstance(error.original, discord.Forbidden):
        await ctx.send("Dsl mec je peux pas exécuter ta commande pcq les admins ne m'ont pas donner les permissions pour faire cela.")'''

def play_song(ctx, client, queu, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
    global url_queue

    def next(_):
        global liste_tracks, ydl_opts, message_channel, current_music
        if len(url_queue) > 0 and len(queu) == 0:
            url = url_queue[0]
            video = Video(url)
            queu.append(video)
            print(url_queue, " ", queu)

        if len(queu) > 0:
            new_song = queu[0]
            current_music = url_queue[0]
            del queu[0]
            del url_queue[0]
            print(current_music)
            with YoutubeDL(ydl_opts) as ydl:
                title = f"%s" %(ydl.extract_info(current_music, download=False)['title'])
            asyncio.run_coroutine_threadsafe(ctx.send(f"Je lance **{title}** : {current_music}"), bot.loop)
            play_song(ctx, client, queu, new_song)
            ctx.voice_client.source.volume = 50 / 100
            print(50/100)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def eval_german(ctx):
    global liste_words, dict_words
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        for i in range(len(liste_words)):
            good_liste = []
            bad_liste = []
            shuffle(liste_words)
            await ctx.send(f"Traduis en français ce mot : {liste_words[0]}\n")

            def check(message):
                return message.author == ctx.message.author and ctx.message.channel == message.channel

            try :
                mot = await bot.wait_for("message", check = check, timeout = 10)

                print(mot, dict_words[liste_words[0]])
                if mot == dict_words[liste_words[0]]:
                    await ctx.send("Bien joué ! Tu as trouvé la bonne traduction ! :)")
                    good_liste.append(liste_words[0])
                elif mot != dict_words[liste_words[0]]:
                    await ctx.send(f"Malheureusement, tu n'as pas trouvé la bonne traduction ! :(\n Essaie encore ! L'entraînement permet de ne pas refaire les mêmes erreurs à l'examen ! \n La bonne réponse était {dict_words[liste_words[0]]}")
                    bad_liste.append(liste_words[0])
                else:
                    await ctx.send("...")
                del liste_words[0]
            except:
                await ctx.send("Dsl ! Temps Ecoulé !")
                break
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")



@bot.command()
async def start(ctx, secondes = 5):
	changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
	game = discord.Game(choice(status))
	await bot.change_presence(activity = game)

@bot.command(pass_context=True)
async def play_music(ctx, code_pays, rang):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        global url_queue, ydl_opts, current_music, pays
        if code_pays not in pays:
            await ctx.send("Dsl, mais je ne connais pas le code de ce pays. utilise la commande '$aide' pour voir tout les codes des pays disponibles et leur orthographe exacte.")
        else:
            link_pays = "spotify:user:spotifycharts:playlist:" + pays[code_pays]
            print(link_pays)
        real_liste_tracks = []
        real_liste_artists = []
        liste_tracks = []
        liste_artists = []
        client = ctx.guild.voice_client
        channel = ctx.author.voice

        if channel is None:
            return await ctx.send("Not connected to voice channel")

        with open('token_spo.txt', 'r') as token_spo:
            client_credentials_manager = SpotifyClientCredentials(client_id="358a882e0433437896ed0c77a429023b",client_secret=token_spo.read())
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        playlist_id = link_pays
        results = sp.playlist(playlist_id)
        tracks = results['tracks']
        for i, item in enumerate(tracks['items']):
            track = item['track']
            real_liste_tracks.append(track['name'])
            real_liste_artists.append(track['artists'][0]['name'])

        for i in range(26):
            liste_tracks.append(real_liste_tracks[i])
            liste_artists.append(real_liste_artists[i])

        if rang != "all":
            if int(rang) > len(liste_tracks):
                ctx.send("Mec t'a écris un nombre trop grand. Y a aucune musique à cette place.")
            else:
                music_playing = liste_tracks[int(rang) - 1] + " " + liste_artists[int(rang) - 1]
        else:
            await ctx.send("Veuillez patienter lors du chargement des musiques")
            shuffle(liste_tracks)
            music_playing = liste_tracks[0] + " " + liste_artists[0]

        query_string = urllib.parse.urlencode({
            'search_query': music_playing
        })
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?' + query_string
        )
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())

        video = 'http://www.youtube.com/watch?v=' + search_results[0]
        with YoutubeDL(ydl_opts) as ydl:
            liste = [f"1 :  %s" %(ydl.extract_info(video, download=False)["title"])]

        url = 'http://www.youtube.com/watch?v=' + search_results[0]
        print("play")

        if rang == "all":
            for i in range(1, 26):
                music_playing = liste_tracks[i] + " " + liste_artists[i]
                query_string = urllib.parse.urlencode({
                    'search_query': music_playing
                })
                htm_content = urllib.request.urlopen(
                    'https://www.youtube.com/results?' + query_string
                )
                search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())

                video = 'http://www.youtube.com/watch?v=' + search_results[0]
                url_queue.append(video)
        title = f"%s" %(ydl.extract_info(url, download=False)['title'])

        if client and client.channel:
            video = Video(url)
            url_queue.append(url)
            musics[ctx.guild].append(video)
            print("dans la file d'attente")
            await ctx.send(f"**{title}** {video.url} a été ajouté à la file d'attente")
        else:
            channel = ctx.author.voice.channel
            video = Video(url)
            musics[ctx.guild] = []
            client = await channel.connect()
            current_music = title
            msg = await ctx.send(f"Je lance **{title}** :  {video.url}")
            play_song(ctx, client, musics[ctx.guild], video)
            ctx.voice_client.source.volume = 50 / 100
            print(50/100)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def music_playing(ctx):
    global current_music
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        await ctx.send(f"La musique en train d'être joué est **{current_music}**")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command(pass_context=True, aliases=['q'])
async def queue(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        total_duration = 0
        ydl_opts = {
            'format': 'bestvideo[width<=1080]+bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [my_hook]
        }
        global url_queue
        counter = 1
        if url_queue == []:
            await ctx.send("Il n'y a aucune musique dans la file d'attente")
        else:
            await ctx.send("Veuillez patienter le temps que je cherche tout les titres dans la file d'attente")

        video = url_queue[0]
        with YoutubeDL(ydl_opts) as ydl:
            temps_chanson = ydl.extract_info(video, download=False)["duration"]
            total_duration += temps_chanson
            minutes = str((temps_chanson // 60))
            secondes = temps_chanson - (temps_chanson // 60)*60
            if secondes < 10:
                secondes = "0" + str(secondes)
            if int(minutes) >= 60:
                hours = 0
                for i in range(int(minutes)//60):
                    minutes -= 60
                    hours += 1
                if int(minutes) < 10:
                    minutes = "0" + str(minutes)
                temps_chanson = str(hours) + ":" + str(minutes) + ":" + str(secondes)
            else:
                if int(minutes) < 10:
                    minutes = "0" + str(minutes)
                temps_chanson = str(minutes) + ":" + str(secondes)
            liste = [f"1 :  %s" %(ydl.extract_info(video, download=False)["title"]) + " " + "(" + temps_chanson + ")"]
        number_of_times = len(url_queue)//25 + 1

        for i in range(1, len(url_queue)):
            video = url_queue[i]
            with YoutubeDL(ydl_opts) as ydl:
                temps_chanson = ydl.extract_info(video, download=False)["duration"]
                total_duration += temps_chanson
                minutes = str((temps_chanson // 60))
                secondes = temps_chanson - (temps_chanson // 60)*60
                if secondes < 10:
                    secondes = "0" + str(secondes)
                temps_chanson = minutes + ":" + str(secondes)
                meta = liste.append(f'{i+1} : %s' %(ydl.extract_info(video, download=False)["title"]) + " " + "(" + temps_chanson + ")")

        hours_2 = int(total_duration)//3600
        minutes_2 = int(total_duration)//60
        secondes_2 = int((total_duration / 60 - minutes_2) * 60)


        if secondes_2 > 60:
            while secondes_2 > 60:
                secondes_2 -= 60
                minutes_2 += 1
        if minutes_2 > 60:
            while minutes_2 > 60:
                minutes_2 -= 60
                hours_2 += 1

        if secondes_2 < 10:
            secondes_2= "0" + str(secondes_2)
        if minutes_2 < 10:
            minutes_2 = "0" + str(minutes_2)
        if hours_2 < 10:
            hours_2 = "0" + str(hours_2)

        total_duration = str(hours_2) + " : " + str(minutes_2) + " : " + str(secondes_2)

        for r in range(number_of_times):
            if not len(liste)-25 < 0:
                emb = discord.Embed(title= f"File d'attente ({total_duration})", description = None, color=0x3498db)
                for i in range(25):
                    print(liste)
                    field = emb.add_field(name = counter, value = liste[0])
                    del liste[0]
                    counter += 1
                await ctx.send(embed = emb)
            else:
                if number_of_times == 1:
                    emb = discord.Embed(title= f"File d'attente ({total_duration})", description = None, color=0x3498db)
                else:
                    emb = discord.Embed(title= f"File d'attente ({total_duration})", description = None, color=0x3498db)
                for i in range(len(liste)):
                    field = emb.add_field(name = counter, value = liste[0])
                    del liste[0]
                    counter += 1
                await ctx.send(embed = emb)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def our_diary(ctx):
    await ctx.send("Veuillez patientez quelques instants je suis en train de recueillir tout les informations par rapport à votre emploi du temps de cette semaine.")
    today = date.today()

    d1 = today.strftime("%d-%m-%Y")


    CHROME_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(executable_path = "Desktop/chromedriver.exe", chrome_options=chrome_options)
    driver.get(f"https://zeus.3ie.fr/home")

    boutton = driver.find_element_by_tag_name("button")
    boutton.click()

    sleep(1)

    email_bar = driver.find_element_by_name("loginfmt")
    with open('email.txt', 'r') as email:
        email_bar.send_keys(email)

    search_btn = driver.find_element_by_id("idSIButton9")
    search_btn.click()

    sleep(10)

    pass_bar = driver.find_element_by_name('Password')
    with open('mdp_epi.txt', 'r') as mdp_epi:
        pass_bar.send_keys("mdp_epi")

    search_btn = driver.find_element_by_id("submitButton")
    search_btn.click()

    sleep(0.5)

    await ctx.send("Connexion au site de zeus réussi. Veuillez attendre attendre quelques instants lors du chargements des données. Cela ne devrait prendre qu'une à 3 minutes de temps.")


    yes_btn = driver.find_element_by_id("idSIButton9")
    yes_btn.click()

    sleep(0.5)

    all_btn = driver.find_element_by_tag_name("button")
    all_btn.click()

    sleep(0.5)

    all_btn = driver.find_element_by_tag_name("mat-expansion-panel-header")
    all_btn.click()

    sleep(0.5)

    class_button = driver.find_element_by_id("filterGroup")
    class_button.send_keys("A2")

    sleep(0.5)

    yes_btn = driver.find_elements_by_tag_name("button")
    yes_btn[3].click()

    sleep(0.5)

    check_box_class = driver.find_elements_by_class_name("tree-node-checkbox")
    check_box_class[11].click()

    week_days = driver.find_element_by_class_name("cal-day-headers")
    print(week_days.text.split("\n"))
    week_days = week_days.text.split("\n")
    week_days_number = []

    for g in range(7):
        a = week_days[g]
        a = list(a)
        j = 0
        variable = ""
        nombre = ""
        for n in range(len(a)):
            if a[n] == " " and a[n+1] != "0" and a[n+1] != "1" and a[n+1] != "2" and a[n+1] != "3" and a[n+1] != "4" and a[n+1] != "5" and a[n+1] != "6" and a[n+1] != "7" and a[n+1] != "8" and a[n+1] != "9":
                nombre = a[n-2] + a[n-1]
                j = int(n) + 1
                while j != len(a):
                    variable += a[j]
                    j += 1
        j = 0


        if variable == "août":
            variable = "08/2021"
        if variable == "sept.":
            variable = "09/2021"
        if variable == "oct.":
            variable = "10/2021"
        if variable == "nov.":
            variable = "11/2021"
        if variable == "déc.":
            variable = "12/2021"
        if variable == "janv.":
            variable = "01/2022"
        if variable == "févr.":
            variable = "02/2022"
        if variable == "mars":
            variable = "03/2022"
        if variable == "avr.":
            variable = "04/2022"
        if variable == "mai":
            variable = "05/2022"
        if variable == "juin":
            variable = "06/2022"
        if variable == "juil.":
            variable = "07/2022"

        week_days_number.append(nombre + "/" + variable)

    print(week_days_number)
    title = driver.find_elements_by_class_name("event-style")
    print(title)
    subjects = []
    events = []
    liste = []
    for a in range(len(title)):
        subjects.append(title[a].text)
        title[a].click()
        sleep(1)
        matiere = "**" + driver.find_element_by_class_name("m-0").text + "**" + "\n"
        texte = driver.find_element_by_class_name("modal-body")
        sous_texte = matiere + texte.text
        events.append(sous_texte.split(" "))
        liste.append(sous_texte.split(";"))
        bouton_close = driver.find_element_by_class_name("btn-close")
        bouton_close.click()
        sleep(1)

    print("liste : ", liste)
    print("liste : ", events)

    event = []
    for c in range(len(title)):
        for b in range(len(events)):
            print(c, b)
            if events[c][b] == "début":
                event.append(events[c][b+2])

    print(event)

    await ctx.send("Voilà votre emploi du temps :")
    sleep(1)

    await ctx.send("```md\n" + "# Notre emploi du temps de la semaine"+ "\n```")
    for i in range(len(week_days_number)):
        message = ""
        await ctx.send("```cs\n # " + week_days[i] + "```")
        for j in range(len(event)):
            if week_days_number[i] == event[j]:
                message += liste[j][0]
                message += "\n\n"
                print(message)
        if message == "":
            message = "Ce jour-ci, il n'y a aucun événement."

        liste_ = list(message)
        number_of_times = len(liste_) // 2000 + 1
        print(number_of_times, len(liste_))
        for r in range(number_of_times):
            if len(liste_) - 2000 >= 0:
                list_commands = ""
                for s in range(2000):
                    list_commands += liste_[0]
                    del liste_[0]
                    print(len(liste_))
                await ctx.send(list_commands)
            else:
                list_commands = ""
                for s in range(len(liste_)):
                    list_commands += liste_[0]
                    del liste_[0]
                await ctx.send(list_commands)

@bot.command()
async def current_time(ctx, contitry):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        hours = ""
        minutes = ""
        secondes = ""
        times = [hours, minutes, secondes]
        tz = pytz.timezone(contitry)
        current_time = datetime.now(tz)
        current_time = current_time.strftime("%H:%M:%S")
        contitry = list(contitry)
        print(contitry)
        while contitry[0] != "/":
            del contitry[0]
        del contitry[0]
        contitry = "".join(contitry)
        print("Current Time =", current_time)
        temps = await ctx.send(f"Il est actuellement {current_time} à {contitry}")
        current_time = list(current_time)
        while current_time[0] != ":":
            hours += current_time[0]
            del current_time[0]
        del current_time[0]
        while current_time[0] != ":":
            minutes += current_time[0]
            del current_time[0]
        del current_time[0]
        for i in range(2):
            print(current_time)
            secondes += current_time[0]
            del current_time[0]
        hours = int(hours)
        minutes = int(minutes)
        secondes = int(secondes)

        tts = gTTS(f"Il est actuellement {hours} heures, {minutes} minutes et {secondes} secondes à {contitry}", lang="fr")
        tts.save('Desktop/bot_discord/heure/heure.mp3')
        user = ctx.message.author
        if user.voice is not None:
            channel = ctx.author.voice.channel
            client = await channel.connect()
            client.play(discord.FFmpegPCMAudio('Desktop/bot_discord/heure/heure.mp3'))
            ctx.voice_client.source.volume = 1000 / 100
            length = mutagen_length("C:/Users/gamin/Desktop/bot_discord/heure/heure.mp3")
            print("duration sec: " + str(length))
            print("duration min: " + str(int(length/60)) + ':' + str(int(length%60)))
            sleep(length)
            client = ctx.guild.voice_client
            await client.disconnect()
        else:
            await ctx.send("Stv y a une petite surprise lorsque tu te mets dans un chat vocal et que tu réexécutes cette commande.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def top(ctx, code_pays):
    global pays
    """shows actual best songs in a country on Spotify"""
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if code_pays not in pays:
            await ctx.send("Dsl, mais je ne connais pas le code de ce pays. utilise la commande '$aide' pour voir tout les codes des pays disponibles et leur orthographe exacte.")
        else:
            link_pays = "spotify:user:spotifycharts:playlist:" + pays[code_pays]
            print(link_pays)
            liste_tracks = []
            liste_artists = []
            liste_images = []
            images = ""
            with open('token_spo.txt', 'r') as token_spo:
                client_credentials_manager = SpotifyClientCredentials(client_id="358a882e0433437896ed0c77a429023b",client_secret=token_spo.read())
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            playlist_id = link_pays
            results = sp.playlist(playlist_id)
            tracks = results['tracks']
            for i, item in enumerate(tracks['items']):
                track = item['track']
                liste_tracks.append(track['name'])
                liste_images.append(track['album']['images'][2]['url'])
                liste_artists.append(track['artists'][0]['name'])
            emb = discord.Embed(title=None, description = "Top 25 - " + code_pays + " on Spotify", color=0x3498db)
            print(images)
            for i in range(25):
                field = emb.add_field(name = str(i+1), value = liste_artists[i] + " - " + liste_tracks[i])
                field.set_thumbnail(url = liste_images[0])
            print(liste_tracks)
            msg = await ctx.send(embed = emb)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")


@bot.command()
async def connect(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        channel = ctx.author.voice.channel
        client = await channel.connect()
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, *, search):
    global current_music, playing
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        message_author = ctx.message.author
        nickname = ctx.message.author.display_name
        counter = 0
        playing = 1
        ydl_opts = {
            'format': 'bestvideo[width<=1080]+bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [my_hook]
        }
        user = ctx.message.author
        if user.voice is None:
            return await ctx.send("Not connected to voice channel")
        print("music played")
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?' + query_string
        )
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())

        await ctx.send("Veuillez patienter, je dois trouver les vidéos pour que vous puissiez choisir la musique qui vous convienne.")
        video = 'http://www.youtube.com/watch?v=' + search_results[counter]
        with YoutubeDL(ydl_opts) as ydl:
            if ydl.extract_info(video, download=False)["is_live"] == True:
                while ydl.extract_info(video, download=False)["is_live"] == True:
                    counter += 1
                    video = 'http://www.youtube.com/watch?v=' + search_results[counter]
            temps_chanson = ydl.extract_info(video, download=False)["duration"]
            minutes = str((temps_chanson // 60))
            secondes = temps_chanson - (temps_chanson // 60)*60
            if secondes < 10:
                secondes = "0" + str(secondes)
            if int(minutes) >= 60:
                hours = 0
                for i in range(int(minutes)//60):
                    minutes = int(minutes) - 60
                    hours += 1
                if minutes < 10:
                    minutes = "0" + str(minutes)
                temps_chanson = str(hours) + ":" + str(minutes) + ":" + str(secondes)
            else:
                if int(minutes) < 10:
                    minutes = "0" + str(minutes)
                temps_chanson = str(minutes) + ":" + str(secondes)
            print(type(temps_chanson))
            liste = [f"1 :  %s" %(ydl.extract_info(video, download=False)["title"]) + " " + "(" + str(temps_chanson) + ")"]
        i = counter + 1
        for x in range(9):
            video = 'http://www.youtube.com/watch?v=' + search_results[i]
            print(video)
            if ydl.extract_info(video, download=False)["is_live"] == True:
                i += 1
            video = 'http://www.youtube.com/watch?v=' + search_results[i]
            with YoutubeDL(ydl_opts) as ydl:
                temps_chanson = ydl.extract_info(video, download=False)["duration"]
                minutes = str(temps_chanson // 60)
                secondes = temps_chanson - (temps_chanson // 60)*60
                if secondes < 10:
                    secondes = "0" + str(secondes)
                if int(minutes) >= 60:
                    hours = 0
                    for i in range(int(minutes)//60):
                        minutes = int(minutes) - 60
                        hours += 1
                    if minutes < 10:
                        minutes = "0" + str(minutes)
                    temps_chanson = str(hours) + ":" + str(minutes) + ":" + str(secondes)
                else:
                    if int(minutes) < 10:
                        minutes = "0" + str(minutes)
                    temps_chanson = minutes + ":" + str(secondes)
            with YoutubeDL(ydl_opts) as ydl:
                meta = liste.append(f'{x+2} : %s' %(ydl.extract_info(video, download=False)["title"]) + " " + "(" + temps_chanson + ")")
            i += 1

        emb = discord.Embed(title=None, description = f"{liste[0]} \n{liste[1]}\n{liste[2]}\n{liste[3]}\n{liste[4]}\n{liste[5]}\n{liste[6]}\n{liste[7]}\n{liste[8]}\n{liste[9]}", color=0x3498db)
        await ctx.send("Veuillez sélectionnez la vidéo de votre choix : ")
        msg = await ctx.send(embed = emb)

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for emoji in reactions:
            await msg.add_reaction(emoji)

            @bot.event
            async def on_reaction_add(reaction, user):
                global playing
                print(user)
                print(playing == 1)
                if playing == 1:
                    if not user.bot and user == message_author:
                        if reaction.emoji == '1️⃣':
                            search = search_results[0]
                        elif reaction.emoji == '2️⃣':
                            search = search_results[1]
                        elif reaction.emoji == '3️⃣':
                            search = search_results[2]
                        elif reaction.emoji == '4️⃣':
                            search = search_results[3]
                        elif reaction.emoji == '5️⃣':
                            search = search_results[4]
                        elif reaction.emoji == '6️⃣':
                            search = search_results[5]
                        elif reaction.emoji == '7️⃣':
                            search = search_results[6]
                        elif reaction.emoji == '8️⃣':
                            search = search_results[7]
                        elif reaction.emoji == '9️⃣':
                            search = search_results[8]
                        else:
                            search = search_results[9]

                        messages = await ctx.channel.history(limit = 3).flatten()
                        for message in messages:
                            await(message.delete())
                        playing = 0

                        url = 'http://www.youtube.com/watch?v=' + search
                        print("play")
                        client = ctx.guild.voice_client
                        video = Video(url)
                        with YoutubeDL(ydl_opts) as ydl:
                            title = f"%s" %(ydl.extract_info(url, download=False)['title'])

                        if client and client.channel and len(url_queue) >= 0:
                            url_queue.append(url)
                            print("dans la file d'attente")
                            await ctx.send(f"**{title}** {video.url} a été ajouté à la file d'attente par **{nickname}**")
                        else:
                            channel = ctx.author.voice.channel
                            print(channel, type(channel))
                            musics[ctx.guild] = []
                            client = await channel.connect()
                            current_music = title
                            msg = await ctx.send(f"Je lance **{title}** : {video.url} demandé par **{nickname}**")
                            play_song(ctx, client, musics[ctx.guild], video)
                            ctx.voice_client.source.volume = 50 / 100
                            print(50/100)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")


class Video:
    def __init__(self, link):
        ydl_opts = {
            'format': 'bestvideo[width<=1080]+bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [my_hook]
        }
        with YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command(pass_context=True, aliases=['v', 'vol'])
async def volume(ctx, volume: int):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if ctx.voice_client is None:
            return await ctx.send("Not connected to voice channel")

        print(volume/100)

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def est_ce_que_tu_dis_faux(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        await ctx.send("Nan je ne dis jamais faux.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def leave(ctx):
    global url_queue
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        client = ctx.guild.voice_client
        await client.disconnect()
        musics[ctx.guild] = []
        url_queue = []
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def resume(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        client = ctx.guild.voice_client
        if client.is_paused():
            client.resume()
            await ctx.send(f"Je reprends la musique là où vous en étiez.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def pause(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        client = ctx.guild.voice_client
        if not client.is_paused():
            client.pause()
            await ctx.send("La musique que vous écoutiez a bien été mis sur pause.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command(pass_context=True, aliases=['s'])
async def skip(ctx):
    global url_queue
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        client = ctx.guild.voice_client
        client.stop()
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def punch(ctx, member):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if {ctx.author.mention} == member:
            ctx.send("T'es teubé ou quoi ? Tu peux pas te donner des coups de poing à toi-même ?! Y a que toi pour être si teubé que ça !!")
        else:
            punchs = ["https://i.gifer.com/C225.gif", "https://i.gifer.com/RAKN.gif", "https://i.gifer.com/RUZS.gif", "https://i.gifer.com/HR4q.gif", "https://i.gifer.com/Tr72.gif"]
            punchy = punchs[randint(0, len(punchs)-1)]
            emb = discord.Embed(title=None, description = f"{ctx.author.mention} met un **ENORME !!!** coup de poing à {member}", color=0x3498db)
            emb.set_image(url=f"{punchy}")
            await ctx.send( embed = emb)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.command()
async def morpion(ctx, p1: discord.Member, p2: discord.Member):
    """ input : @player1 @player2"""
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        print("morpion began")
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:",
                    ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
            await ctx.send("To play you have to write the command $place and then the rank where you want to put your thing from your team")
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send("Please start a new game using the !tictactoe command.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@morpion.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

@bot.command()
async def slap(ctx, member):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if {ctx.author.mention} == member:
            ctx.send("T'es teubé ou quoi ? Tu peux pas te donner de claques à toi-même ?! Y a que toi pour être si teubé que ça !!")
        else:
            slaps = ["https://i.gifer.com/XaaW.gif", "https://i.gifer.com/2eNz.gif", "https://i.gifer.com/2Dji.gif", "https://i.gifer.com/1Vbb.gif", "https://i.gifer.com/K03.gif", "https://i.gifer.com/DjuN.gif", "https://i.gifer.com/Djw.gif", "https://i.gifer.com/4kpG.gif", "https://i.gifer.com/K02.gif"]
            slappy = slaps[randint(0, len(slaps)-1)]
            emb = discord.Embed(title=None, description = f"{ctx.author.mention} met une claque à {member}", color=0x3498db)
            emb.set_image(url=f"{slappy}")
            await ctx.send( embed = emb)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def nombre_serveurs(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        counter = 0
        names = ""
        for guild in bot.guilds:
            counter += 1
            names += guild.name
            names += ", "
        await ctx.send(f"Je suis membre dans un total de {counter} serveurs qui se nomment : {names}")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def lettre_random(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        for i in range(5):
            lettres = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
            lettre_bot = lettres[randint(0, len(lettres))]
            print(lettre_bot)
            await ctx.send("Je pense à une lettre. Essaye de la deviner")

            def check(message):
                return message.author == ctx.message.author and ctx.message.channel == message.channel

            lettre_joueur = await bot.wait_for("message", check = check)
            if lettre_joueur.content == lettre_bot:
                await ctx.send("Bien joué ! Tu as trouvé la lettre à laquelle je pensais")
            else:
                await ctx.send(f"Ta lettre : {lettre_joueur.content} \n Ma lettre : {lettre_bot} \n Dommage ! Tu as perdu !")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def togglebotchannel(ctx):
    global allowed_channels
    current_channel = ctx.message.channel.id
    allowed_channels.append(current_channel)
    await ctx.send("Cette channel est désormais un bot channel.")

@bot.command()
async def coucou(ctx, member):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if {ctx.author.mention} == member:
            ctx.send("T'es teubé ou quoi ? Tu peux pas te faire coucou à toi-même ?! Y a que toi pour être si teubé que ça !!")
        else:
            if member == "@everyone":
                member = "tout le monde"
            coucous = ["https://i.gifer.com/6ZFR.gif", "https://i.gifer.com/1UEW.gif", "https://i.gifer.com/UUP.gif", "https://i.gifer.com/Wx6B.gif", "https://i.gifer.com/WShb.gif", "https://i.gifer.com/1rO6.gif", "https://i.gifer.com/5Tz.gif", "https://i.gifer.com/CMSH.gif"]
            coocky = coucous[randint(0,len(coucous)-1)]
            emb = discord.Embed(title=None, description = f"{ctx.author.mention} fait un coucou à {member}", color=0x3498db)
            emb.set_image(url=f"{coocky}")
            await ctx.send( embed = emb)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def hug(ctx, member):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if {ctx.author.mention} == member:
            ctx.send("T'es teubé ou quoi ? Tu peux pas te faire des calins à toi-même ?! Y a que toi pour être si teubé que ça !!")
        else:
            hugs = ["https://i.gifer.com/1ak.gif", "https://i.gifer.com/2HBY.gif", "https://i.gifer.com/GAMC.gif", "https://i.gifer.com/UQOJ.gif", "https://i.gifer.com/I3M0.gif", "https://i.gifer.com/I50j.gif", "https://i.gifer.com/MMuP.gif", "https://i.gifer.com/O2pp.gif", "https://i.gifer.com/1pg.gif", "https://i.gifer.com/APS3.gif"]
            huggy = hugs[randint(0,len(hugs)-1)]
            emb = discord.Embed(title=None, description = f"{ctx.author.mention} fait un calin à {member}", color=0x3498db)
            emb.set_image(url=f"{huggy}")
            await ctx.send( embed = emb)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def kiss(ctx,*, member):
    print(member)
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if {ctx.author.mention} == member:
            ctx.send("T'es teubé ou quoi ? Tu peux pas te donner de bisous à toi-même ?! Y a que toi pour être si teubé que ça !!")
        elif member == "bot Benjamin#3840":
            await ctx.send("Oh ! Je crois que je vais rougir.")
        else:
            kisses = ["https://i.gifer.com/iJb.gif", "https://i.gifer.com/V4hX.gif", "https://i.gifer.com/g33j.gif", "https://media.giphy.com/media/NKmXVFgwd8HKw/giphy.gif", "http://31.media.tumblr.com/bfbe6acecd87db57ad96c573d0e49e97/tumblr_mt2si1aAoC1sinrido1_500.gif", "https://i.gifer.com/abb.gif", "https://www.deviantart.com/inukagome134/art/Japan-Kiss-Animated-GIF-255408766"]
            kissy = kisses[randint(0, len(kisses)-1)]
            emb = discord.Embed(title=None, description = f"{ctx.author.mention} fait un bisou à {member}", color=0x3498db)
            emb.set_image(url=f"{kissy}")
            await ctx.send( embed = emb)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

def mutagen_length(path):
    try:
        audio = MP3(path)
        length = audio.info.length
        return length
    except:
        return None

@bot.command()
async def accent(ctx, langue, *, message):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if langue == "qu":
            tts = gTTS(message, lang="fr", tld="ca")
        else:
            tts = gTTS(message, lang=langue)
        tts.save('Desktop/bot_discord/traduction.mp3')
        user = ctx.message.author
        if user.voice is None:
            return await ctx.send("Not connected to voice channel")

        channel = ctx.author.voice.channel
        client = await channel.connect()
        client.play(discord.FFmpegPCMAudio('Desktop/bot_discord/traduction.mp3'))
        ctx.voice_client.source.volume = 1000 / 100
        length = mutagen_length("C:/Users/gamin/Desktop/bot_discord/traduction.mp3")
        print("duration sec: " + str(length))
        print("duration min: " + str(int(length/60)) + ':' + str(int(length%60)))
        sleep(length)
        client = ctx.guild.voice_client
        await client.disconnect()
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def serverInfo(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        server = ctx.guild
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        serverDescription = server.description
        numberOfPerson = server.member_count
        serverName = server.name
        message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes. \n La description du serveur est {serverDescription}. \n Ce serveur possède *{numberOfTextChannels}* salons textuels ainsi que *{numberOfVoiceChannels}* salons vocaux."
        await ctx.send(message)
        await ctx.send("Si tu en as besoin tu peux écrire $aide pour avoir des explication sur toutes les commandes disponible avec ce bot.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def ping(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        await ctx.send("Pong !")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

'''
@bot.command()
async def screenshot(ctx, *name):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        name = " ".join(name)
        s = o.screenshot()
        s.save(f"Desktop\\{name}.png")
        await ctx.send(f"Ta photo a bien été prise et a été envoyé sur ton bureau sous le nom de **{name}**.png")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")'''

'''
@bot.command()
async def bonjour(ctx):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        roles = ""
        server = ctx.guild
        for r in server.roles:
            role = f"{r}"
            print(role)
            await ctx.send(role)'''

@bot.command()
async def say(ctx, chiffre, *texte):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        if int(chiffre) > 10:
            await ctx.send("dsl j'ai été patch je peux plus faire plus de 10 messages")
        else:
            for i in range(int(chiffre)):
                await ctx.send(" ".join(texte))
            await ctx.send("Si tu en as besoin tu peux écrire $aide pour avoir des explication sur toutes les commandes disponible avec ce bot.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def getInfo(ctx, text):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        server = ctx.guild
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        serverDescription = server.description
        numberOfPerson = server.member_count
        serverName = server.name
        if text == "memberCount":
            await ctx.send(numberOfPerson)
        elif text == "numberOfChannel":
            await ctx.send(numberOfTextChannels + numberOfVoiceChannels)
        elif text == "name":
            await ctx.send(serverName)
        else:
            await ctx.send("Etrange... Je ne connais pas cela")
        await ctx.send("Si tu en as besoin tu peux écrire $aide pour avoir des explication sur toutes les commandes disponible avec ce bot.")
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")


@bot.command()
async def aide(ctx):
    '''get more informations about commands'''
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        commands = "```fix\n$serverInfo```permet de connaître quelques informations sur le serveur \n\n```fix\n$say + nombre de fois + message à dire```permet de faire dire quelque chose au bot fois un nombre (par exemple, input : $say 4 coucou, output : coucou coucou coucou coucou) \n\n```fix\n$getInfo + input```permet d'avoir des infos sur l'input que vous donnez (input possible : memberCount, numberOfChannel, name) \n\n```fix\n$clear + nombre de messages précédents```efface le nombre de message précedent (exemple input : $clear 5 output : effacement des 5 précédents messages)\n\n```fix\n$ping```fait une partie de tennis de table avec moi. \n\n```fix\n$kiss + ping d'un membre du serveur```fait un bisou à la personne que tu mentionnes (l'input doit être sous la forme '$kiss @destinataire') \n\n```fix\n$slap + mention d'un membre du serveur```donne une claque au destinataire, s'écrit sous la même forme que la fonction $kiss \n\n```fix\n$coucou + mention d'un membre du serveur```permet de faire coucou au destinataire, s'écrit sous la même forme que la fonction $kiss \n\n```fix\n$punch + mention d'un membre du serveur```donne un coup de poing au destinataire, s'écrit sous la même forme que la fonction $kiss \n\n```fix\n$play + nom de la musique à jouer```joue une musique choisi par l'utilisateur dans le salon vocal où est l'utilisateur (exemple d'input : $play despacito) \n\n```fix\n$morpion + ping des deux joueurs qui veulent jouer```démarre une partie de morpion (ou tic tac toe en anglais). Pour y jouer il faut mettre en input 2 mentions de 'vraies' personnes et non des bots. De plus, pour pouvoir placer un pion sur le plateau, il faut utiliser la commande $place puis écrire en input le rang où le joueur veut poser son pion. Pour vous aider, voici le plateau avec à la place des cases leur rang pour vous aider à poser vos pions \n    1   2   3   \n   4   5   6   \n   7   8   9   \n\n```fix\n$top + code du pays```donne le top 25 actuel des meilleurs chansons du pays que vous avez indiqué sur Spotify. Voici les pays disponibles et leur code correspondant : (France : FR, Royaume-Uni : UK, Etats-Unis : USA, Monde : WORLD, Espagne : ES, Inde : IN, Philippines : PH , Turquie : TU, Japon : JA, Pays-Bas : PB, Italie : IT, Russie : RU). Je tiens à préciser que d'autres pays vont être ajouter à cette commande dans le futur. \n\n```fix\n$play_music + code classement pays dans $top + rang de la musique voulu```permet de jouer rapidement une musique du classement du pays de votre choix (vous pouvez trouvez les codes des pays disponibles dans l'aide pour la commande $top) en mettant son rang que vous pouvez retrouver grâce à la commande $top. Petite nouveauté sur cette commande : il est possible de jouer toutes les musiques dans un ordre aléatoire du $top du pays de votre choix en écrivant par exemple : $play_music FR all \n\n```fix\n$blague```lorsque vous activer cette commande je vous raconte n'importe quelle blague que je connais en français\n\n```fix\n$joke```lorsque vous écrivez cette commande je vous raconte n'importe quelle blague que je connais en anglais \n\n```fix\n$start_hangman```démarre une partie du jeu du pendu mais svp n'essayez pas cette commande car elle est en développement. Elle risque de faire crache le bot et le server. \n\n```fix\n$nombre_serveurs```donne le nombre de serveur dans lequel je suis et je donne leur nom.```fix\n$accent + code langue + message à dire``` je lis votre message avec l'accent dans la langue de votre choix. les langues disponibles sont : 'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 'bs': 'Bosnian', 'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'eo': 'Esperanto', 'es': 'Spanish', 'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French', 'gu': 'Gujarati', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'hy': 'Armenian', 'id': 'Indonesian', 'is':'Icelandic', 'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean', 'la': 'Latin', 'lv': 'Latvian', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'qu': 'Québécois', 'ro': 'Romanian', 'ru': 'Russian', 'si': 'Sinhala', 'sk': 'Slovak', 'sq': 'Albanian', 'sr': 'Serbian', 'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-CN': 'Chinese', 'zh-TW': 'Chinese (Mandarin/Taiwan)', 'zh': 'Chinese (Mandarin)' \n\n```fix\n$current_time + nom du continent en anglais/nom de la capitale en anglais``` donne l'heure actuelle dans la ville écrite en Input."
        liste = list(commands)
        number_of_times = len(liste) // 2000 + 1
        print(number_of_times, len(liste))
        for r in range(number_of_times):
            if len(liste) - 2000 >= 0:
                list_commands = ""
                for i in range(2000):
                    list_commands += liste[0]
                    del liste[0]
                    print(len(liste))
                await ctx.send(list_commands)
            else:
                list_commands = ""
                for i in range(len(liste)):
                    list_commands += liste[0]
                    del liste[0]
                await ctx.send(list_commands)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await(message.delete())

@bot.command()
async def ban(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    await ctx.send(f"{user} a été ban pour la reason suivante : {reason}.")
    print(reason)

@bot.command()
async def unban(ctx, user, *reason):
    current_channel = ctx.message.channel.id
    channels = ctx.guild.channels
    if checks_in_bot_channel(channels, current_channel) == True:
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            if i.user.name == username and i.user.id == userId:
                await ctx.guild.unban(i.user)
    else:
        await ctx.send("Désolé ! Mais vous n'êtes autorisé qu'à utiliser les bots channels qui ont été whitelisté par mon créateur.")

@bot.command()
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} a été kick pour la reason suivante : {reason}.")
    print(reason)

fin = 1
@bot.command()
async def start_hangman(ctx):
    global fin
    liste_mots_cache = ["mathematiques", "programmer", "ordinateur", "clavier", "souris", "python", "arduino", "internet", "creation", "passion", "clovis", "manuel", "anglais", "telephone", "jouer", "joueur","joueuse", "matiere", "bouteille", "calendrier", "reveil", "caserole", "fleurs", "cles", "calculatrice", "calculette", "apple", "batman", "guirlande", "stylo", "trousse", "vampire", "jour", "pont", "guitare", "flute", "violon", "radiateur", "evian", "vittel", "cristaline", "animaux", "photos", "guillaume", "hugo", "eren", "titan", "colossal", "cuirasse", "muraille","chine", "arsene","toilette","fils","tomber","courir", "ecrire", "nuit", "echec", "pendu", "numerique", "science","informatique", "mur", "maria", "rose", "rules of survival", "brawl stars", "fortnite", "hearthstone", "rubik's cube", "rocket league", "wesh", "lampe", "chewing-gum", "boire", "manger", "machouiller", "fete", "livre", "adaptateur", "casque", "pantalon", "chaise"]
    mot_a_trouver = list(liste_mots_cache[randint(0, len(liste_mots_cache))])
    mot_montré = []
    for i in range(len(mot_a_trouver)):
        if mot_a_trouver[i] == " ":
            mot_montré.append(" ")
        elif mot_a_trouver[i] == "'":
            mot_montré.append("'")
        elif mot_a_trouver[i] == "-":
            mot_montré.append("-")
        else:
            mot_montré.append("\\_")
    letters_played = []
    fautes = 0
    variable = 0
    message_channel = ctx.message.channel.id
    channel = discord.utils.get(ctx.guild.channels, name= "jeu-du-pendu")
    channel_id = channel.id
    print(channel_id, message_channel)
    if channel_id == message_channel:
        if fin == 1:
            fin = 0
            await ctx.send(mot_a_trouver)
            mot_montré = " ".join(mot_montré)
            await ctx.send(f"le mot à trouver : {mot_montré}")
            await ctx.send("Ecris une lettre pour deviner le mot")
            mot_montré = "".join(mot_montré)
            print(mot_montré)
            mot_montré = list(mot_montré)
            for l in range(len(mot_montré)-len(mot_a_trouver)):
                if mot_montré[l] == "\\":
                    del mot_montré[l]
            for e in range(len(mot_montré)-(len(mot_a_trouver)-1)):
                if mot_montré[e] == " ":
                    del mot_montré[e]
            print(mot_montré)
        else:
            await ctx.send("Une partie est déjà en cours. Veuillez la terminer pour pouvoir en commencer une nouvelle.")

        def check(message):
            #return message.author == ctx.message.author and ctx.message.channel == message.channel
            return True

        while fin != 1:
            try:
                lettre_du_joueur = await bot.wait_for("message", check = check, timeout = 360)
                lettre_du_joueur = lettre_du_joueur.content

                indexes = []
                print(letters_played)
                if lettre_du_joueur in letters_played:
                    await ctx.send("TU AS DEJA JOUÉ CETTE LETTRE !!!")
                elif lettre_du_joueur in mot_a_trouver:
                    for i in range(len(mot_a_trouver)):
                        if lettre_du_joueur == mot_a_trouver[i]:
                            indexes.append(i)
                    for r in range(len(indexes)):
                        mot_montré[indexes[r]] = lettre_du_joueur
                        variable += 1
                    letters_played.append(lettre_du_joueur)
                else:
                    if fautes != 10:
                        await ctx.send("**Dommage !!** Ce n'était pas la bonne lettre ! Essaye encore !")
                    else:
                        await ctx.send("**Perdu !!** Tu feras mieux la prochaine fois (peut-être) :)")
                    fautes += 1

                if fautes == 1:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483571204919386/1.PNG")

                if fautes == 2:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871484660058841088/2.PNG")

                if fautes == 3:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483577559285821/3.PNG")

                if fautes == 4:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483579006349372/4.PNG")

                if fautes == 5:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483580293988352/5.PNG")

                if fautes == 6:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483581929779291/6.PNG")

                if fautes == 7:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483583485849700/7.PNG")

                if fautes == 8:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483584932900874/8.PNG")

                if fautes == 9:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483586283446373/9.PNG")

                if fautes == 10:
                    emb = discord.Embed(title=None, description = "", color=0x3498db)
                    emb.set_image(url="https://cdn.discordapp.com/attachments/631935311592554636/871483590268055562/10.PNG")

                if fautes != 0:
                    await ctx.send( embed = emb)

                if mot_montré == mot_a_trouver:
                    fin += 1
                    mot_montré = " ".join(mot_montré)
                    await ctx.send(mot_montré)
                    await ctx.send("Bravo, tu as trouvé le mot caché !!")
                    mot_a_trouver = list(liste_mots_cache[randint(0, len(liste_mots_cache))])
                    mot_montré = []
                    for i in range(len(mot_a_trouver)):
                        if mot_a_trouver[i] == " ":
                            mot_montré.append(" ")
                        elif mot_a_trouver[i] == "'":
                            mot_montré.append("'")
                        elif mot_a_trouver[i] == "-":
                            mot_montré.append("-")
                        else:
                            mot_montré.append("\\_")
                    letters_played = []
                    fautes = 0
                    sol = "  \\_ \\_ \\_ \\_ \\_    "
                    tiret_haut1 = "     |       "
                    tiret_haut2 = "     |       "
                    tiret_haut3 = "     |       "
                    tiret_haut4 = "     |       "
                    tiret_haut5 = "     |       "
                    haut = ["    "]
                    for i in range(6):
                        haut.append("\\_ ")
                    haut = "".join(haut)
                    variable = 0
                elif fautes == 10:
                    fin += 1
                    await ctx.send("Malheureusement, tu n'as pas trouvé le mot caché !! Le mot à trouver était :", "".join(mot_a_trouver))
                    mot_a_trouver = list(liste_mots_cache[randint(0, len(liste_mots_cache))])
                    mot_montré = []
                    for i in range(len(mot_a_trouver)):
                        if mot_a_trouver[i] == " ":
                            mot_montré.append(" ")
                        elif mot_a_trouver[i] == "'":
                            mot_montré.append("'")
                        elif mot_a_trouver[i] == "-":
                            mot_montré.append("-")
                        else:
                            mot_montré.append("\\_")
                    letters_played = []
                    fautes = 0
                    for i in range(6):
                        haut.append("\\_ ")
                    haut = "".join(haut)
                    variable = 0
                else:
                    for z in range(len(mot_montré)):
                        if mot_montré[z] == "_":
                            mot_montré[z] = "\\_"
                    mot_montré = " ".join(mot_montré)
                    await ctx.send(f"le mot à trouver : {mot_montré}")
                    await ctx.send("Ecris une lettre pour deviner le mot ")
                    mot_montré = "".join(mot_montré)
                    print(mot_montré)
                    mot_montré = list(mot_montré)
                    for l in range(len(mot_montré)-(len(mot_a_trouver) - variable)):
                        if mot_montré[l] == "\\":
                            del mot_montré[l]
                    for e in range(len(mot_montré)-(len(mot_a_trouver) - variable)):
                        if mot_montré[e] == " ":
                            del mot_montré[e]
                    print(mot_montré)
            except:
                await ctx.send("**Ta partie de hangman a été annulé car tu as mis trop de temps à répondre.**")
                fin = 1
                break
    else:
        await ctx.send("Tu n'est pas sur le bon channel. Pour jouer à ce jeu, il faut te rendre sur le channel 'jeu-du-pendu' du serveur Las Vacas Aerodinamicas ou alors contacter mon créateur pour plus d'infos.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def end_hangman(ctx):
    global fin
    fin = 1
    await ctx.send("La partie de pendu a été terminé manuellement. Tu peux en redémarrer une nouvelle avec la commande $start_hangman.")

bot.add_cog(jokes.CogOwner(bot))
bot.add_cog(blague.CogOwner(bot))
with open('token_bot.txt', 'r') as token:
    bot.run(token.read())
