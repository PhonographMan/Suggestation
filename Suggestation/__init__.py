from .suggestation import Suggestation


def setup(bot):
    bot.add_cog(Suggestation(bot))