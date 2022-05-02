import discord
from datetime import datetime, timedelta


# Class that have dict for Save all times(start, end, result)
class ResTimeline():
    def __init__(self, author):
        self.author = author

        # Dict declaration and initialization is_start_point 
        self.res_timeline = dict(start=datetime, finish=datetime, rs=timedelta)
        self.is_start_point = False

        # Open Author own txt file, and set result time
        try :
            with open('log/'+author+'.txt', 'r') as f_re:
                for_all_time = f_re.readlines()[0]
                self.res_timeline['rs'] = datetime.strptime(for_all_time, '%Y-%m-%d %H:%M:%S.%f')

        # If file not exist than creat new Author txt file 
        except Exception:
            if author != 'BOT-for-2#3970':
                default_dt = datetime(1900, 1, 1, 0, 0)
                with open('log/'+author+'.txt', 'w') as f_wr:
                    f_wr.write(str(default_dt)+'.000000')
    def get_auth():
        return self.author



class CountdownClass(discord.Client):
    async def on_ready(self):
        print("Logged on as {0}".format(self.user))
        members = self.get_all_members()

        # Set ResTimeline Classes for all Users except bot
        self.logs_rt = [ResTimeline(str(i)) for i in members]

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        author = '{0.author}'.format(message)
        
        if (author != 'BOT-for-2#3970'):

            # Get ResTimeline Class for current author
            for i in self.logs_rt:
                if i.author == author:
                    cli = i

            # !help feature
            if message.content.startswith('!help'):

                await message.channel.send('''Instructions for use:
**!start** - *Start session*
**!finish** - *Finish session*
**!current** - *Current session time*
**!alltime** - *Session for all-time*
**!reset** - *Reset all-time*
                ''')

            # !start feature
            if message.content.startswith('!start'):

                if (cli.is_start_point==False):
                    cli.res_timeline['start'] = datetime.now()

                    # Set is_start_point True
                    cli.is_start_point = True
                    send_message = 'The countdown has begun! Good luck!'
                else:
                    send_message = 'The starting point already exists.'
                await message.channel.send(send_message)

            # !finish feature
            if message.content.startswith('!finish'):

                if (cli.is_start_point==True):
                    cli.res_timeline['finish'] = datetime.now()

                    dt_result = cli.res_timeline['finish'] - cli.res_timeline['start']
                    send_message = "Work's done. Your time "+str(dt_result).split('.')[0]

                    # Set is_start_point False
                    cli.is_start_point = False

                    cli.res_timeline['rs'] = cli.res_timeline['rs'] + dt_result
                    with open('log/'+author+'.txt', 'w') as f_wr:
                        f_wr.write(str(cli.res_timeline['rs']))

                    cli.res_timeline['start'] = datetime

                else:
                    send_message = "Can't find starting point!"

                await message.channel.send(send_message)

            # !current feature
            if message.content.startswith('!current'):

                if (cli.is_start_point==True):
                    cli.res_timeline['finish'] = datetime.now()

                    dt_result = cli.res_timeline['finish'] - cli.res_timeline['start']

                    send_message = "Сurrent session lasts " + str(dt_result).split('.')[0]
                else:
                    send_message = "There is no session"
                await message.channel.send(send_message)

            # !alltimes feature
            if message.content.startswith('!alltime'):

                default_dt = datetime(1900, 1, 1, 0, 0)
                dt_result = cli.res_timeline['rs'] - default_dt
                send_message = str(dt_result).split('.')[0]

                if (cli.is_start_point==True):
                    cli.res_timeline['finish'] = datetime.now()
                    current_result = cli.res_timeline['finish'] - cli.res_timeline['start']
                    send_message = str(current_result+dt_result).split('.')[0]

                await message.channel.send("You worked "+send_message)

            # !reset feature
            if message.content.startswith('!reset'):

                default_dt = datetime(1900, 1, 1, 0, 0)
                cli.res_timeline['rs'] = default_dt

                with open('log/'+author+'.txt', 'w') as f_wr:
                    f_wr.write(str(default_dt)+'.000000')

                await message.channel.send("Time reset")


if __name__ == '__main__':

    intents = discord.Intents.default()
    intents.members = True
    with open('token.txt', 'r') as f_re:
        token = f_re.readlines()[0]
    client = CountdownClass(intents=intents)
    client.run(str(token))