import logging
import sys
from discord.ext import commands


class Gainsworth(commands.Cog):
    def __init__(self, client):
        """
        The init function will always take a client, which represents
         the particular bot that is using the cog.
        """
        self.client = client
        self._last_member = None
        self.logger = logging.getLogger(__name__)
        self.logger.info('Gainsworth Cog instance created')

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Any listeners you add will be effectively merged with the global
         listeners, which means you can have multiple cogs listening for the
        same events and taking actions based on those events.
        """
        print("Gainsworth is ready to PUMP YOU UP!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        sys.stdout.write("Command Error: ")
        sys.stdout.write(f"{error}")
        ignored = (commands.CommandInvokeError)
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'{ctx.author.name}, I did not understand that command.'
                           ' Try typing `g!help` to see a list of available commands.')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.name}, there was an issue with that command,'
                           f' type `g!help {ctx.args[1].command.name}` to learn more'
                           ' about how to format that command')
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(f'{ctx.author.name}, there was an issue with your arguments,'
                           f' type `g!help {ctx.args[1].command.name}` to learn more'
                           ' about how to format that command')
        # It's probably better to handle these errors in their respective methods
        elif "'NoneType' object has no attribute 'reps'" in str(error):
            await ctx.send(f"I didn't find that exercise, {ctx.author.name}!"
                           " Type `g!list_exercises` to see all the exercises I'm"
                           " currently tracking.")
        elif "duplicate key" in str(error):
            await ctx.send(f'That exercise already exists for you, {ctx.author.name}!'
                           ' Type `g!list_exercises` to see all the exercises you have'
                           ' already added.')
        elif "UnmappedInstanceError" in str(error):
            await ctx.send(f"I didn't find that exercise, {ctx.author.name}!"
                           " Type `g!list_exercises` to see all the exercises I'm"
                           " currently tracking.")
        elif isinstance(error, ignored):
            return
        else:
            await ctx.send(f'{ctx.author.name}, something went wrong with your input.')

    @commands.command()
    async def hello(self, ctx):
        """Says hello"""
        print("message received")
        channel = ctx.channel
        channels = ["gym-class-heroes"]
        if ctx.author == self.client.user:
            return
        if channel.name in channels:
            member = ctx.author
            if self._last_member is None or self._last_member.id != member.id:
                # {0.name} here comes from the MessageEmbed class's "fields" attr
                await ctx.send('Hello {0.name}~'.format(member))
            else:
                await ctx.send('Hello {0.name}... Are you getting \
                               your GAINS in?'.format(member))
            self._last_member = member


def setup(client):
    """
    This setup function must exist in every cog file and will ultimately have a
    nearly identical signature and logic to what you're seeing here.
    It's ultimately what loads the Cog into the bot.
    """
    client.add_cog(Gainsworth(client))
