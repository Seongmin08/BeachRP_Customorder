import discord ,asyncio ,sqlite3 ,datetime ,json #line:2
from discord .ext import commands #line:3
with open ('./config/setting.json','r',encoding ='utf-8')as hal :#line:5
    min =json .load (hal )#line:6
app =commands .Bot (command_prefix =min ['prefix'],intents =discord .Intents ().all ())#line:8
now =datetime .datetime .now ().strftime ("%Y년 %m월 %d일 %H시 %M분")#line:9
time_temp =datetime .datetime .now ().strftime ("%Y_%m_%d_%H_%M")#line:10
def join_sql ():#line:12
    try :#line:13
        OOOO0OOOO000O0OOO =sqlite3 .connect ("./data/question.db")#line:14
        OO000OOO0OO0O00O0 =OOOO0OOOO000O0OOO .cursor ()#line:15
        return OOOO0OOOO000O0OOO ,OO000OOO0OO0O00O0 #line:16
    except :#line:17
        return False ,False #line:18
@app .event #line:20
async def on_ready ():#line:21
    await app .change_presence (status =discord .Status .dnd ,activity =discord .Game (name =min ['st']))#line:22
    print (f'{app.user} | {app.user.id} Online | Dev . ! 민성™#3784')#line:23
@app .command ()#line:25
async def 도움말 (OOOO000OOO00OOO0O ):#line:26
    await OOOO000OOO00OOO0O .author .send (f'<@{OOOO000OOO00OOO0O.author.id}>',embed =discord .Embed (title ='문의 봇 도움말',description =f"**접두사** : {min['prefix']} \n**직원 명령어** \n`{min['prefix']}직원 등록 <@맨션>` , `{min['prefix']}직원 제거 <@맨션>` , `{min['prefix']}직원 출근` , `{min['prefix']}직원 휴식` , `{min['prefix']}직원 복귀` , `{min['prefix']}직원 퇴근` \n\n**문의 관련 명령어** \n`{min['prefix']}문의 블랙 <@맨션> <사유>` , `{min['prefix']}문의 블랙해제 <@맨션>` , `{min['prefix']}문의 종료` \n\n문의 사항은",color =0xeeff00 ))#line:27
@app .command ()#line:30
async def 직원 (OOO0OO0OOOOOOO00O ,if_text :str =None ,user :discord .Member =None ):#line:31
    O0O0OOO00OOO0OO00 ,OOO00OO00OO0000OO =join_sql ()#line:32
    if O0O0OOO00OOO0OO00 ==False :#line:33
        return await OOO0OO0OOOOOOO00O .send ("고객센터 전산 시스템에 에러가 발생 하였습니다.")#line:34
    if OOO0OO0OOOOOOO00O .guild .owner .id !=OOO0OO0OOOOOOO00O .author .id :#line:36
        return await OOO0OO0OOOOOOO00O .send (f'{OOO0OO0OOOOOOO00O.author.mention}님 께서는 서버 주인이 아니십니다.')#line:37
    if if_text is None :#line:39
        return await OOO0OO0OOOOOOO00O .send ('명령어 입력이 잘못 되었습니다.')#line:40
    if if_text in ['등록']:#line:42
        if user is None :#line:43
            return await OOO0OO0OOOOOOO00O .send ("유저가 지정 되지 않았습니다.")#line:44
        OOO00OO00OO0000OO .execute ('INSERT INTO staff(user_name, user_id, open_cl, close_cl, user_st) VALUES(?,?,?,?,?)',(str (user ),int (user .id ),str ('출근 시간'),str ('퇴근 시간'),str ('출근')))#line:45
        O0O0OOO00OOO0OO00 .commit ()#line:46
        await OOO0OO0OOOOOOO00O .send (f"{user.mention}님 께서 직원으로 등록 되었습니다.")#line:47
    if if_text in ['제거']:#line:49
        if user is None :#line:50
            return await OOO0OO0OOOOOOO00O .send ("유저가 지정 되지 않았습니다.")#line:51
        OOO00OO00OO0000OO .execute (f"DELETE FROM staff WHERE user_id = {user.id}")#line:52
        OOO00OO00OO0000OO .execute (f"DELETE FROM staf WHERE user_id = {user.id}")#line:53
        O0O0OOO00OOO0OO00 .commit ()#line:54
    if if_text in ['출근']:#line:56
        OOO00OO00OO0000OO .execute ('UPDATE staff SET open_cl = ? WHERE user_id = ?',(str (now ),int (OOO0OO0OOOOOOO00O .author .id )))#line:57
        OOO00OO00OO0000OO .execute ('UPDATE staff SET user_st = ? WHERE user_id = ?',(str ('출근중'),int (OOO0OO0OOOOOOO00O .author .id )))#line:58
        OOO00OO00OO0000OO .execute ('UPDATE staf SET staff_st = staff_st + 1 WHERE id = 1')#line:59
        O0O0OOO00OOO0OO00 .commit ()#line:60
        await OOO0OO0OOOOOOO00O .send (f'{OOO0OO0OOOOOOO00O.author.mention}님 께서 출근 하셨습니다. \n> 출근 시간 : {now}')#line:61
    if if_text in ['퇴근']:#line:63
        OOO00OO00OO0000OO .execute ('UPDATE staff SET close_cl = ? WHERE user_id = ?',(str (now ),int (OOO0OO0OOOOOOO00O .author .id )))#line:64
        OOO00OO00OO0000OO .execute ('UPDATE staff SET user_st = ? WHERE user_id = ?',(str ('퇴근'),int (OOO0OO0OOOOOOO00O .author .id )))#line:65
        OOO00OO00OO0000OO .execute ('UPDATE staf SET staff_st = staff_st - 1 WHERE id = 1')#line:66
        O0O0OOO00OOO0OO00 .commit ()#line:67
        OOO00OO00OO0000OO .execute (f'SELECT open_cl FROM staff WHERE user_id="{OOO0OO0OOOOOOO00O.author.id}"')#line:68
        O000O0O00OO0O0O00 =OOO00OO00OO0000OO .fetchone ()#line:69
        await OOO0OO0OOOOOOO00O .send (f'{OOO0OO0OOOOOOO00O.author.mention}님 께서 퇴근 하셨습니다. \n> 출근 시간 : {O000O0O00OO0O0O00[0]} | 퇴근 시간 : {now}')#line:70
    if if_text in ['휴식']:#line:72
        OOO00OO00OO0000OO .execute ('UPDATE staff SET user_st = ? WHERE user_id = ?',(str ('휴식중'),int (OOO0OO0OOOOOOO00O .author .id )))#line:73
        OOO00OO00OO0000OO .execute ('UPDATE staf SET staff_st = staff_st - 1 WHERE id = 1')#line:74
        await OOO0OO0OOOOOOO00O .send (f'{OOO0OO0OOOOOOO00O.author.mention}님 께서 휴식 하셨습니다.')#line:75
    if if_text in ['복귀']:#line:77
        OOO00OO00OO0000OO .execute ('UPDATE staff SET user_st = ? WHERE user_id = ?',(str ('충근중'),int (OOO0OO0OOOOOOO00O .author .id )))#line:78
        OOO00OO00OO0000OO .execute ('UPDATE staf SET staff_st = staff_st + 1 WHERE id = 1')#line:79
        await OOO0OO0OOOOOOO00O .send (f'{OOO0OO0OOOOOOO00O.author.mention}님 께서 휴식 하셨습니다.')#line:80
@app .command ()#line:83
async def 문의 (O00OOOOO0OOOO00O0 ,text :str =None ,user :discord .Member =None ,ren :str =None ):#line:84
    OOOOO0000OO00O00O ,OO0O0OOOO00OO0000 =join_sql ()#line:85
    if OOOOO0000OO00O00O ==False :#line:86
        return await O00OOOOO0OOOO00O0 .send ("고객센터 전산 시스템에 에러가 발생 하였습니다.")#line:87
    if text is None :#line:89
        return await O00OOOOO0OOOO00O0 .send (f'명령어 입력이 잘 못 되었습니다.')#line:90
    if text =='블랙':#line:92
        if user is None :#line:93
            return await O00OOOOO0OOOO00O0 .send (f'유저가 지정 되지 않았습니다.')#line:94
        if ren is None :#line:95
            return await O00OOOOO0OOOO00O0 .send ('블랙 사유가 작성되지 않았습니다.')#line:96
        OO0O0OOOO00OO0000 .execute ('INSERT INTO ansdml_black(user_name, user_id, black) VALUES(?,?,?)',(str (user ),int (user .id ),str ('true')))#line:97
        OOOOO0000OO00O00O .commit ()#line:98
        await O00OOOOO0OOOO00O0 .send (f'{user.mention}님 께서 문의가 블랙 되셨습니다.')#line:99
        await user .send (embed =discord .Embed (title ='[ Candy 고객센터 ]',description =f'문의가 차단 되었습니다. \n담당자 : {O00OOOOO0OOOO00O0.author.mention}님에 의해 문의가 차단 되셨습니다. \n**사 유**\n```{ren}```',color =0x00ccff ))#line:100
    if text =='블랙해제':#line:102
        if user is None :#line:103
            return await O00OOOOO0OOOO00O0 .send (f'유저가 지정 되지 않았습니다.')#line:104
        OO0O0OOOO00OO0000 .execute (f"DELETE FROM ansdml_black WHERE user_id = {user.id}")#line:105
        OOOOO0000OO00O00O .commit ()#line:106
        await O00OOOOO0OOOO00O0 .send (f'{user.mention}님 께서 문의가 블랙 해제 되셨습니다.')#line:107
        await user .send (embed =discord .Embed (title ='[ Candy 고객센터 ]',description =f'문의가 차단 해제 되었습니다. \n담당자 : {O00OOOOO0OOOO00O0.author.mention}님에 의해 문의 차단이 해제 되셨습니다.',color =0xffd500 ))#line:108
@app .event #line:111
async def on_message (O0OOO000O00OOO0OO ):#line:112
    OO0O0OO0000OO0000 ,O0OOOOO0000OOOOOO =join_sql ()#line:113
    OO000OOOOOO000000 =app .get_guild (int (min ['guild_id']))#line:114
    OOOOO00O00OOO0O0O =OO000OOOOOO000000 .get_channel (int (min ['category_id']))#line:115
    if OO0O0OO0000OO0000 ==False :#line:116
        return await O0OOO000O00OOO0OO .channel .send ("고객센터 전산 시스템에 에러가 발생 하였습니다.")#line:117
    O0O000OOO0O000O0O =O0OOO000O00OOO0OO .author #line:118
    OO0O0000OOO00O000 =str (O0OOO000O00OOO0OO .author )#line:119
    OOO00O0O0O0OOOOO0 =O0O000OOO0O000O0O .id #line:120
    if O0OOO000O00OOO0OO .author .bot :#line:121
        return #line:122
    if O0OOO000O00OOO0OO .content .startswith ("#"):#line:123
        return #line:124
    O0OOOOO0000OOOOOO .execute (f'SELECT * FROM ansdml_black WHERE user_id="{O0O000OOO0O000O0O.id}"')#line:125
    O0O00OO0O0O00O000 =O0OOOOO0000OOOOOO .fetchone ()#line:126
    O0OOOOO0000OOOOOO .execute (f'SELECT * FROM staf WHERE id = 1')#line:127
    OOOOOO0000OO00000 =O0OOOOO0000OOOOOO .fetchone ()#line:128
    if str (O0OOO000O00OOO0OO .channel .type )=="private":#line:129
        if O0O00OO0O0O00O000 :#line:130
            if O0O00OO0O0O00O000 [2 ]!='ture':#line:131
                return await O0O000OOO0O000O0O .send (embed =discord .Embed (title =f'[ Candy 고객센터 ]',description =f'**{O0O000OOO0O000O0O.name} 님은 현재 "차단" 상태 입니다 \n \n 해당 문의사항 전송을 실패했습니다.**',color =0x00D8FF ))#line:132
        if OOOOOO0000OO00000 [1 ]==0 :#line:133
            return await O0O000OOO0O000O0O .send ('직원이 모두 퇴근중이어서 문의가 불가능 합니다. \n> 직원 출근 후 문의 바랍니다.')#line:134
        O0OOOOO0000OOOOOO .execute (f'SELECT * FROM question WHERE user_id="{O0O000OOO0O000O0O.id}"')#line:135
        O00OOO00O00O0O0OO =O0OOOOO0000OOOOOO .fetchall ()#line:136
        OOOO00000OOO000O0 =str (O00OOO00O00O0O0OO ).replace ("(","").replace (")","").replace ("[","").replace ("]","")#line:137
        if OOOO00000OOO000O0 ==""or OOOO00000OOO000O0 =='':#line:138
            O00O0O0OOO0O0OOOO =discord .Embed (title =f'{O0OOO000O00OOO0OO.author.name}님 아래의 문의 카테고리를 확인해 주세요.',description =f'1️⃣ 서버 문의 \n2️⃣ 유저 신고\n3️⃣ 기타 문의\n❌ 문의 취소',color =0x00b3ff ).set_footer (text ='60초 동안 아무 반응이 없을시 자동으로 문의가 종료 됩니다.')#line:139
            OOOO0O0OOOO0OOO0O =await O0O000OOO0O000O0O .send (embed =O00O0O0OOO0O0OOOO )#line:140
            await OOOO0O0OOOO0OOO0O .add_reaction ('1️⃣')#line:141
            await OOOO0O0OOOO0OOO0O .add_reaction ('2️⃣')#line:142
            await OOOO0O0OOOO0OOO0O .add_reaction ('3️⃣')#line:143
            await OOOO0O0OOOO0OOO0O .add_reaction ('❌')#line:144
            try :#line:145
                OOOOO00OOOOOOOOO0 ,O0OOO000O00OOO0OO .author =await app .wait_for ('reaction_add',timeout =60 ,check =lambda O0O00OOOOO000OO00 ,OO00OO00OO0O00O00 :OO00OO00OO0O00O00 ==O0OOO000O00OOO0OO .author and str (O0O00OOOOO000OO00 .emoji )in ['1️⃣','2️⃣','3️⃣','❌'])#line:146
            except asyncio .TimeoutError :#line:147
                await OOOO0O0OOOO0OOO0O .edit (embed =discord .Embed (title =f'[ Candy 고객센터 ]',description =f'시간이 초과되어 자동으로 문의가 종료 되었습니다.',color =0x00D8FF ))#line:148
            else :#line:149
                if str (OOOOO00OOOOOOOOO0 .emoji )=="1️⃣":#line:150
                    await OOOO0O0OOOO0OOO0O .edit (embed =discord .Embed (title =f'{O0O000OOO0O000O0O.name}님의 문의가 접수 되었습니다.',description =f'**`서버문의`**의 문의 분류로 문의가 접수 되었습니다.',color =0x00ff40 ))#line:151
                    O0O00OO0000O0O0O0 =await OO000OOOOOO000000 .create_text_channel (f'서버문의-{O0O000OOO0O000O0O.name}',category =OOOOO00O00OOO0O0O )#line:152
                    O0OOOOO0000OOOOOO .execute ('CREATE TABLE IF NOT EXISTS question("user_name" TEXT, "user_id" integer not null, "ch_id" integer)')#line:153
                    O0OOOOO0000OOOOOO .execute ('INSERT INTO question(user_name, user_id, ch_id) VALUES(?,?,?)',(OO0O0000OOO00O000 ,OOO00O0O0O0OOOOO0 ,O0O00OO0000O0O0O0 .id ))#line:154
                    OO0O0OO0000OO0000 .commit ()#line:155
                    O0OOOOO0000OOOOOO .execute (f'SELECT * FROM question WHERE user_id="{O0O000OOO0O000O0O.id}"')#line:156
                    OOOO0O0OOOO0OOO0O =O0OOOOO0000OOOOOO .fetchone ()#line:157
                    await O0O00OO0000O0O0O0 .send (f"> <@&{min['role_id']}]> **문의가 접수 되었습니다.** \n문의가 접수 되었습니다. `문의분류 : 서버문의`")#line:158
                    if O0OOO000O00OOO0OO .attachments :#line:159
                        await O0O00OO0000O0O0O0 .send (f'[ 문의자 : <@{OOOO0O0OOOO0OOO0O[1]}> ( {hal[1]} ) ] 님께서 첨부파일을 보내셨습니다.')#line:160
                        await O0O00OO0000O0O0O0 .send (O0OOO000O00OOO0OO .attachments [0 ].url )#line:161
                    else :#line:162
                        await O0O00OO0000O0O0O0 .send (f'[ 문의자 : <@{OOOO0O0OOOO0OOO0O[1]}> ( {hal[1]} ) ] \n\n문의 내용 : {O0OOO000O00OOO0OO.content}')#line:163
                elif str (OOOOO00OOOOOOOOO0 .emoji )=="2️⃣":#line:165
                    await OOOO0O0OOOO0OOO0O .edit (embed =discord .Embed (title =f'{O0O000OOO0O000O0O.name}님의 문의가 접수 되었습니다.',description =f'**`유저신고`**의 문의 분류로 문의가 접수 되었습니다.',color =0x00ff40 ))#line:166
                    O0O00OO0000O0O0O0 =await OO000OOOOOO000000 .create_text_channel (f'유저신고-{O0O000OOO0O000O0O.name}',category =OOOOO00O00OOO0O0O )#line:167
                    O0OOOOO0000OOOOOO .execute ('create table if not exists question("user_name" text, "user_id" integer not null, "ch_id" integer)')#line:168
                    O0OOOOO0000OOOOOO .execute ('INSERT INTO question(user_name, user_id, ch_id) VALUES(?,?,?)',(OO0O0000OOO00O000 ,OOO00O0O0O0OOOOO0 ,O0O00OO0000O0O0O0 .id ))#line:169
                    OO0O0OO0000OO0000 .commit ()#line:170
                    O0OOOOO0000OOOOOO .execute (f'SELECT * FROM question WHERE user_id="{O0O000OOO0O000O0O.id}"')#line:171
                    OOOO0O0OOOO0OOO0O =O0OOOOO0000OOOOOO .fetchone ()#line:172
                    await O0O00OO0000O0O0O0 .send (f"> <@&{min['role_id']}> **문의가 접수 되었습니다.** \n문의가 접수 되었습니다. `문의분류 : 유저신고`")#line:173
                    if O0OOO000O00OOO0OO .attachments :#line:174
                        await O0O00OO0000O0O0O0 .send (f'[ 문의자 : <@{OOOO0O0OOOO0OOO0O[1]}> ( {hal[1]} ) ] 님께서 첨부파일을 보내셨습니다.')#line:175
                        await O0O00OO0000O0O0O0 .send (O0OOO000O00OOO0OO .attachments [0 ].url )#line:176
                    else :#line:177
                        await O0O00OO0000O0O0O0 .send (f'[ 문의자 : <@{OOOO0O0OOOO0OOO0O[1]}> ( {hal[1]} ) ] \n\n문의 내용 : {O0OOO000O00OOO0OO.content}')#line:178
                elif str (OOOOO00OOOOOOOOO0 .emoji )=="3️⃣":#line:180
                    await OOOO0O0OOOO0OOO0O .edit (embed =discord .Embed (title =f'{O0O000OOO0O000O0O.name}님의 문의가 접수 되었습니다.',description =f'**`기타문의`**의 문의 분류로 문의가 접수 되었습니다.',color =0x00ff40 ))#line:181
                    O0O00OO0000O0O0O0 =await OO000OOOOOO000000 .create_text_channel (f'기타문의-{O0O000OOO0O000O0O.name}',category =OOOOO00O00OOO0O0O )#line:182
                    O0OOOOO0000OOOOOO .execute ('CREATE TABLE IF NOT EXISTS question("user_name" TEXT, "user_id" integer not null, "ch_id" integer)')#line:183
                    O0OOOOO0000OOOOOO .execute ('INSERT INTO question(user_name, user_id, ch_id) VALUES(?,?,?)',(OO0O0000OOO00O000 ,OOO00O0O0O0OOOOO0 ,O0O00OO0000O0O0O0 .id ))#line:184
                    OO0O0OO0000OO0000 .commit ()#line:185
                    O0OOOOO0000OOOOOO .execute (f'SELECT * FROM question WHERE user_id="{O0O000OOO0O000O0O.id}"')#line:186
                    OOOO0O0OOOO0OOO0O =O0OOOOO0000OOOOOO .fetchone ()#line:187
                    await O0O00OO0000O0O0O0 .send (f"> <@&{min['role_id']}> **문의가 접수 되었습니다.** \n문의가 접수 되었습니다. `문의분류 : 기타문의`")#line:188
                    if O0OOO000O00OOO0OO .attachments :#line:189
                        await O0O00OO0000O0O0O0 .send (f'[ 문의자 : <@{OOOO0O0OOOO0OOO0O[1]}> ( {hal[1]} ) ] 님께서 첨부파일을 보내셨습니다.')#line:190
                        await O0O00OO0000O0O0O0 .send (O0OOO000O00OOO0OO .attachments [0 ].url )#line:191
                    else :#line:192
                        await O0O00OO0000O0O0O0 .send (f'[ 문의자 : <@{OOOO0O0OOOO0OOO0O[1]}> ( {hal[1]} ) ] \n\n문의 내용 : {O0OOO000O00OOO0OO.content}')#line:193
                elif str (OOOOO00OOOOOOOOO0 .emoji )=="❌":#line:195
                    await OOOO0O0OOOO0OOO0O .edit (embed =discord .Embed (title =f'{O0O000OOO0O000O0O.name}님 문의를 취소하였습니다.',description =f'문의가 취소 됩니다',color =0x00D8FF ))#line:196
        else :#line:197
            O0OOOOO0000OOOOOO .execute (f'SELECT * FROM question WHERE user_id="{O0O000OOO0O000O0O.id}"')#line:198
            OOOO0O0OOOO0OOO0O =O0OOOOO0000OOOOOO .fetchone ()#line:199
            O0O00OO0000O0O0O0 =app .get_channel (OOOO0O0OOOO0OOO0O [2 ])#line:200
            if O0OOO000O00OOO0OO .attachments :#line:201
                await O0O00OO0000O0O0O0 .send (f'[ 문의자 : <@{OOOO0O0OOOO0OOO0O[1]}> ( {hal[1]} ) ] 님께서 첨부파일을 보내셨습니다.')#line:202
                await O0O00OO0000O0O0O0 .send (O0OOO000O00OOO0OO .attachments [0 ].url )#line:203
            else :#line:204
                await O0O00OO0000O0O0O0 .send (f'[ 문의자 : <@{OOOO0O0OOOO0OOO0O[1]}> ( {hal[1]} ) ] \n\n문의 내용 : {O0OOO000O00OOO0OO.content}')#line:205
    await app .process_commands (O0OOO000O00OOO0OO )#line:207
    if O0OOO000O00OOO0OO .author .bot :#line:209
        return #line:210
    if not str (O0OOO000O00OOO0OO .channel .type )=="private":#line:212
        try :#line:213
            if O0OOO000O00OOO0OO .channel .category .id ==int (min ['category_id']):#line:214
                if O0OOO000O00OOO0OO .channel .id ==int (min ['channel_id']):#line:215
                    return #line:216
                O0O00OO0000O0O0O0 =O0OOO000O00OOO0OO .channel #line:217
                O0OOOOO0000OOOOOO .execute (f'SELECT * FROM question WHERE ch_id="{O0O00OO0000O0O0O0.id}"')#line:218
                OOOO0O0OOOO0OOO0O =O0OOOOO0000OOOOOO .fetchone ()#line:219
                if O0OOO000O00OOO0OO .content ==f'{min["prefix"]}문의 종료':#line:220
                    await (await app .fetch_user (int (OOOO0O0OOOO0OOO0O [1 ]))).send (embed =discord .Embed (title ='[ Candy 고객센터 ]',description =f'문의가 종료되었습니다. \n\n> 다시 문의하고 싶으신 경우에만 메시지를 다시 보내주세요\n\n > 앞으로 더욱 나아가는 Candy 서버가 되겠습니다 :)',color =0x00D8FF ))#line:221
                    with open (f'./Log/{time_temp} - {O0OOO000O00OOO0OO.channel.name}.txt',"w",encoding ='utf-8')as OO00O00O0O0000OOO :#line:222
                        async for OO00000OO0OOO0OO0 in O0OOO000O00OOO0OO .channel .history (limit =None ):#line:223
                            OO00O00O0O0000OOO .write (f"{OO00000OO0OOO0OO0.created_at} - {OO00000OO0OOO0OO0.author.display_name}: {OO00000OO0OOO0OO0.clean_content}\n")#line:224
                    await O0OOO000O00OOO0OO .channel .send (f'> **The inquiry will be closed after {int(min["close_s"])} seconds.**')#line:225
                    await asyncio .sleep (int (min ['close_s']))#line:226
                    await O0O00OO0000O0O0O0 .delete ()#line:227
                    O0OOOOO0000OOOOOO .execute (f"DELETE FROM question WHERE ch_id = {O0O00OO0000O0O0O0.id}")#line:228
                    OO0O0OO0000OO0000 .commit ()#line:229
                    with open (f'./Log/{time_temp} - {O0OOO000O00OOO0OO.channel.name}.txt',"rb")as OO00O00O0O0000OOO :#line:230
                        await app .get_channel (int (min ['channel_id'])).send (file =discord .File (OO00O00O0O0000OOO ,f"./Log/{time_temp} - {O0OOO000O00OOO0OO.channel.name}.txt"))#line:231
                    return #line:232
                if O0OOO000O00OOO0OO .attachments :#line:233
                    await (await app .fetch_user (int (OOOO0O0OOOO0OOO0O [1 ]))).send (f'[ Candy 고객센터 ] 님께서 첨부파일을 보내셨습니다.')#line:234
                    await (await app .fetch_user (int (OOOO0O0OOOO0OOO0O [1 ]))).send (O0OOO000O00OOO0OO .attachments [0 ].url )#line:235
                else :#line:236
                    await (await app .fetch_user (int (OOOO0O0OOOO0OOO0O [1 ]))).send (f'[ Candy 고객센터 ] : {O0OOO000O00OOO0OO.content}')#line:237
        except :#line:238
            pass #line:239
    await app .process_commands (O0OOO000O00OOO0OO )#line:240
app .run (min ['token'])#line:243
