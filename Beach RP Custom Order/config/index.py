#-*- coding: utf-8 -*-
import discord, asyncio, sqlite3, datetime, json
from discord.ext import commands

with open('./config/setting.json', 'r', encoding='utf-8') as hal:
    haley = json.load(hal)

app = commands.Bot(command_prefix = haley['prefix'], intents = discord.Intents().all())
now = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
time_temp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")

def join_sql():
    try:
        db = sqlite3.connect("./data/question.db")
        SQL = db.cursor()       
        return db, SQL
    except:
        return False, False

@app.event
async def on_ready():
    await app.change_presence(status = discord.Status.dnd, activity = discord.Game(name = haley['st']))
    print(f'{app.user} | {app.user.id} Online | Dev . ! 민성™#3784')

@app.command()
async def 도움말(ctx):
    await ctx.author.send(f'<@{ctx.author.id}>', embed = discord.Embed(title = '문의 봇 도움말', description = f"**접두사** : {haley['prefix']} \n**직원 명령어** \n`{haley['prefix']}직원 등록 <@맨션>` , `{haley['prefix']}직원 제거 <@맨션>` , `{haley['prefix']}직원 출근` , `{haley['prefix']}직원 휴식` , `{haley['prefix']}직원 복귀` , `{haley['prefix']}직원 퇴근` \n\n**문의 관련 명령어** \n`{haley['prefix']}문의 블랙 <@맨션> <사유>` , `{haley['prefix']}문의 블랙해제 <@맨션>` , `{haley['prefix']}문의 종료` \n\n문의 사항은", color = 0xeeff00))


@app.command()
async def 직원(ctx, if_text: str = None, user: discord.Member = None):
    db, SQL = join_sql()
    if db == False:
        return await ctx.send("고객센터 전산 시스템에 에러가 발생 하였습니다.")
    
    if ctx.guild.owner.id != ctx.author.id:
        return await ctx.send(f'{ctx.author.mention}님 께서는 서버 주인이 아니십니다.')

    if if_text is None:
        return await ctx.send('명령어 입력이 잘못 되었습니다.')

    if if_text in ['등록']:
        if user is None:
            return await ctx.send("유저가 지정 되지 않았습니다.")
        SQL.execute('INSERT INTO staff(user_name, user_id, open_cl, close_cl, user_st) VALUES(?,?,?,?,?)', (str(user), int(user.id), str('출근 시간'), str('퇴근 시간'), str('출근')))
        db.commit()
        await ctx.send(f"{user.mention}님 께서 직원으로 등록 되었습니다.")

    if if_text in ['제거']:
        if user is None:
            return await ctx.send("유저가 지정 되지 않았습니다.")
        SQL.execute(f"DELETE FROM staff WHERE user_id = {user.id}")
        SQL.execute(f"DELETE FROM staf WHERE user_id = {user.id}")
        db.commit()

    if if_text in ['출근']:
        SQL.execute('UPDATE staff SET open_cl = ? WHERE user_id = ?', (str(now), int(ctx.author.id)))
        SQL.execute('UPDATE staff SET user_st = ? WHERE user_id = ?', (str('출근중'), int(ctx.author.id)))
        SQL.execute('UPDATE staf SET staff_st = staff_st + 1 WHERE id = 1')
        db.commit()
        await ctx.send(f'{ctx.author.mention}님 께서 출근 하셨습니다. \n> 출근 시간 : {now}')

    if if_text in ['퇴근']:
        SQL.execute('UPDATE staff SET close_cl = ? WHERE user_id = ?', (str(now), int(ctx.author.id)))
        SQL.execute('UPDATE staff SET user_st = ? WHERE user_id = ?', (str('퇴근'), int(ctx.author.id)))
        SQL.execute('UPDATE staf SET staff_st = staff_st - 1 WHERE id = 1')
        db.commit()
        SQL.execute(f'SELECT open_cl FROM staff WHERE user_id="{ctx.author.id}"')
        result = SQL.fetchone()
        await ctx.send(f'{ctx.author.mention}님 께서 퇴근 하셨습니다. \n> 출근 시간 : {result[0]} | 퇴근 시간 : {now}')

    if if_text in ['휴식']:
        SQL.execute('UPDATE staff SET user_st = ? WHERE user_id = ?', (str('휴식중'), int(ctx.author.id)))
        SQL.execute('UPDATE staf SET staff_st = staff_st - 1 WHERE id = 1')
        await ctx.send(f'{ctx.author.mention}님 께서 휴식 하셨습니다.')

    if if_text in ['복귀']:
        SQL.execute('UPDATE staff SET user_st = ? WHERE user_id = ?', (str('충근중'), int(ctx.author.id)))
        SQL.execute('UPDATE staf SET staff_st = staff_st + 1 WHERE id = 1')
        await ctx.send(f'{ctx.author.mention}님 께서 휴식 하셨습니다.')


@app.command()
async def 문의(ctx, text: str = None, user: discord.Member = None, ren: str = None):
    db, SQL = join_sql()
    if db == False:
        return await ctx.send("고객센터 전산 시스템에 에러가 발생 하였습니다.")
    
    if text is None:
        return await ctx.send(f'명령어 입력이 잘 못 되었습니다.')

    if text == '블랙':
        if user is None:
            return await ctx.send(f'유저가 지정 되지 않았습니다.')
        if ren is None:
            return await ctx.send('블랙 사유가 작성되지 않았습니다.')
        SQL.execute('INSERT INTO ansdml_black(user_name, user_id, black) VALUES(?,?,?)', (str(user), int(user.id), str('true')))
        db.commit()
        await ctx.send(f'{user.mention}님 께서 문의가 블랙 되셨습니다.')
        await user.send(embed = discord.Embed(title = '[ Candy 고객센터 ]', description = f'문의가 차단 되었습니다. \n담당자 : {ctx.author.mention}님에 의해 문의가 차단 되셨습니다. \n**사 유**\n```{ren}```', color = 0x00ccff))

    if text == '블랙해제':
        if user is None:
            return await ctx.send(f'유저가 지정 되지 않았습니다.')
        SQL.execute(f"DELETE FROM ansdml_black WHERE user_id = {user.id}")
        db.commit()
        await ctx.send(f'{user.mention}님 께서 문의가 블랙 해제 되셨습니다.')
        await user.send(embed = discord.Embed(title = '[ Candy 고객센터 ]', description = f'문의가 차단 해제 되었습니다. \n담당자 : {ctx.author.mention}님에 의해 문의 차단이 해제 되셨습니다.', color = 0xffd500))
        

@app.event
async def on_message(message):
    db, SQL = join_sql()
    guild = app.get_guild(int(haley['guild_id']))
    category_channel = guild.get_channel(int(haley['category_id']))
    if db == False:
        return await message.channel.send("고객센터 전산 시스템에 에러가 발생 하였습니다.")
    author = message.author
    USER_NAME = str(message.author)
    USER_ID = author.id
    if message.author.bot:
        return
    if message.content.startswith("#"):
        return
    SQL.execute(f'SELECT * FROM ansdml_black WHERE user_id="{author.id}"')
    ansdml_black = SQL.fetchone()
    SQL.execute(f'SELECT * FROM staf WHERE id = 1')
    staff_st = SQL.fetchone()
    if str(message.channel.type) == "private":
        if ansdml_black:
            if ansdml_black[2] != 'ture':
                return await author.send(embed = discord.Embed(title = f'[ Candy 고객센터 ]', description= f'**{author.name} 님은 현재 "차단" 상태 입니다 \n \n 해당 문의사항 전송을 실패했습니다.**', color = 0x00D8FF))
        if staff_st[1] == 0:
            return await author.send('직원이 모두 퇴근중이어서 문의가 불가능 합니다. \n> 직원 출근 후 문의 바랍니다.')
        SQL.execute(f'SELECT * FROM question WHERE user_id="{author.id}"')
        result = SQL.fetchall()
        result2 = str(result).replace("(", "").replace(")", "").replace("[", "").replace("]", "")
        if result2 == "" or result2 == '':
            embed = discord.Embed(title = f'{message.author.name}님 아래의 문의 카테고리를 확인해 주세요.', description= f'1️⃣ 서버 문의 \n2️⃣ 유저 신고\n3️⃣ 기타 문의\n❌ 문의 취소', color = 0x00b3ff).set_footer(text='60초 동안 아무 반응이 없을시 자동으로 문의가 종료 됩니다.')
            hal = await author.send(embed=embed)
            await hal.add_reaction('1️⃣')
            await hal.add_reaction('2️⃣')
            await hal.add_reaction('3️⃣')
            await hal.add_reaction('❌')
            try:
                reaction, message.author = await app.wait_for('reaction_add', timeout = 60, check = lambda reaction, author: author == message.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '❌'])
            except asyncio.TimeoutError:
                await hal.edit(embed = discord.Embed(title = f'[ Candy 고객센터 ]', description= f'시간이 초과되어 자동으로 문의가 종료 되었습니다.', color = 0x00D8FF))
            else:
                if str(reaction.emoji) == "1️⃣":
                    await hal.edit(embed = discord.Embed(title = f'{author.name}님의 문의가 접수 되었습니다.', description= f'**`서버문의`**의 문의 분류로 문의가 접수 되었습니다.', color = 0x00ff40))
                    ch = await guild.create_text_channel(f'서버문의-{author.name}', category = category_channel)
                    SQL.execute('CREATE TABLE IF NOT EXISTS question("user_name" TEXT, "user_id" integer not null, "ch_id" integer)')
                    SQL.execute('INSERT INTO question(user_name, user_id, ch_id) VALUES(?,?,?)', (USER_NAME, USER_ID, ch.id))
                    db.commit()
                    SQL.execute(f'SELECT * FROM question WHERE user_id="{author.id}"')
                    hal = SQL.fetchone()    
                    await ch.send(f"> <@&{haley['role_id']}]> **문의가 접수 되었습니다.** \n문의가 접수 되었습니다. `문의분류 : 서버문의`")
                    if message.attachments:
                        await ch.send(f'[ 문의자 : <@{hal[1]}> ( {hal[1]} ) ] 님께서 첨부파일을 보내셨습니다.')
                        await ch.send(message.attachments[0].url)
                    else:
                        await ch.send(f'[ 문의자 : <@{hal[1]}> ( {hal[1]} ) ] \n\n문의 내용 : {message.content}')
                
                elif str(reaction.emoji) == "2️⃣":
                    await hal.edit(embed = discord.Embed(title = f'{author.name}님의 문의가 접수 되었습니다.', description= f'**`유저신고`**의 문의 분류로 문의가 접수 되었습니다.', color = 0x00ff40))
                    ch = await guild.create_text_channel(f'유저신고-{author.name}', category = category_channel)
                    SQL.execute('create table if not exists question("user_name" text, "user_id" integer not null, "ch_id" integer)')
                    SQL.execute('INSERT INTO question(user_name, user_id, ch_id) VALUES(?,?,?)', (USER_NAME, USER_ID, ch.id))
                    db.commit()
                    SQL.execute(f'SELECT * FROM question WHERE user_id="{author.id}"')
                    hal = SQL.fetchone()
                    await ch.send(f"> <@&{haley['role_id']}> **문의가 접수 되었습니다.** \n문의가 접수 되었습니다. `문의분류 : 유저신고`")
                    if message.attachments:
                        await ch.send(f'[ 문의자 : <@{hal[1]}> ( {hal[1]} ) ] 님께서 첨부파일을 보내셨습니다.')
                        await ch.send(message.attachments[0].url)
                    else:
                        await ch.send(f'[ 문의자 : <@{hal[1]}> ( {hal[1]} ) ] \n\n문의 내용 : {message.content}')

                elif str(reaction.emoji) == "3️⃣":
                    await hal.edit(embed = discord.Embed(title = f'{author.name}님의 문의가 접수 되었습니다.', description= f'**`기타문의`**의 문의 분류로 문의가 접수 되었습니다.', color = 0x00ff40))
                    ch = await guild.create_text_channel(f'기타문의-{author.name}', category = category_channel)
                    SQL.execute('CREATE TABLE IF NOT EXISTS question("user_name" TEXT, "user_id" integer not null, "ch_id" integer)')
                    SQL.execute('INSERT INTO question(user_name, user_id, ch_id) VALUES(?,?,?)', (USER_NAME, USER_ID, ch.id))
                    db.commit()
                    SQL.execute(f'SELECT * FROM question WHERE user_id="{author.id}"')
                    hal = SQL.fetchone()
                    await ch.send(f"> <@&{haley['role_id']}> **문의가 접수 되었습니다.** \n문의가 접수 되었습니다. `문의분류 : 기타문의`")
                    if message.attachments:
                        await ch.send(f'[ 문의자 : <@{hal[1]}> ( {hal[1]} ) ] 님께서 첨부파일을 보내셨습니다.')
                        await ch.send(message.attachments[0].url)
                    else:
                        await ch.send(f'[ 문의자 : <@{hal[1]}> ( {hal[1]} ) ] \n\n문의 내용 : {message.content}')

                elif str(reaction.emoji) == "❌":
                    await hal.edit(embed = discord.Embed(title = f'{author.name}님 문의를 취소하였습니다.', description= f'문의가 취소 됩니다', color = 0x00D8FF))
        else:
            SQL.execute(f'SELECT * FROM question WHERE user_id="{author.id}"')
            hal = SQL.fetchone()
            ch = app.get_channel(hal[2])
            if message.attachments:
                await ch.send(f'[ 문의자 : <@{hal[1]}> ( {hal[1]} ) ] 님께서 첨부파일을 보내셨습니다.')
                await ch.send(message.attachments[0].url)
            else:
                await ch.send(f'[ 문의자 : <@{hal[1]}> ( {hal[1]} ) ] \n\n문의 내용 : {message.content}')
    
    await app.process_commands(message)

    if message.author.bot:
        return

    if not str(message.channel.type) == "private":
        try:
            if message.channel.category.id == int(haley['category_id']):
                if message.channel.id == int(haley['channel_id']):
                    return
                ch = message.channel
                SQL.execute(f'SELECT * FROM question WHERE ch_id="{ch.id}"')
                hal = SQL.fetchone()
                if message.content == f'{haley["prefix"]}문의 종료':
                    await (await app.fetch_user(int(hal[1]))).send(embed = discord.Embed(title = '[ Candy 고객센터 ]', description = f'문의가 종료되었습니다. \n\n> 다시 문의하고 싶으신 경우에만 메시지를 다시 보내주세요\n\n > 앞으로 더욱 나아가는 Candy 서버가 되겠습니다 :)', color = 0x00D8FF))
                    with open(f'./Log/{time_temp} - {message.channel.name}.txt', "w", encoding = 'utf-8') as file:
                        async for msg in message.channel.history(limit = None):
                            file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n")
                    await message.channel.send(f'> **The inquiry will be closed after {int(haley["close_s"])} seconds.**')
                    await asyncio.sleep(int(haley['close_s']))
                    await ch.delete()
                    SQL.execute(f"DELETE FROM question WHERE ch_id = {ch.id}")
                    db.commit()
                    with open(f'./Log/{time_temp} - {message.channel.name}.txt', "rb") as file:
                        await app.get_channel(int(haley['channel_id'])).send(file = discord.File(file, f"./Log/{time_temp} - {message.channel.name}.txt"))
                    return
                if message.attachments:
                    await (await app.fetch_user(int(hal[1]))).send(f'[ Candy 고객센터 ] 님께서 첨부파일을 보내셨습니다.')
                    await (await app.fetch_user(int(hal[1]))).send(message.attachments[0].url)
                else:
                    await (await app.fetch_user(int(hal[1]))).send(f'[ Candy 고객센터 ] : {message.content}')
        except:
            pass
    await app.process_commands(message)


app.run(haley['token'])
