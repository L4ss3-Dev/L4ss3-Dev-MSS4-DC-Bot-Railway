import discord

    if next_premium == 3:
        await ctx.send("💎 Premium JETZT verfügbar!")
    else:
        await ctx.send(f"⏳ Noch {next_premium} Spins bis Premium")


@bot.command()
async def leaderboard(ctx):

    sorted_users = sorted(
        data.items(),
        key=lambda x: x[1]["streak"],
        reverse=True
    )

    msg = "🏆 Leaderboard\n\n"

    for i, (uid, udata) in enumerate(sorted_users[:10], start=1):
        try:
            user = await bot.fetch_user(int(uid))
            msg += f"{i}. {user.name} - {udata['streak']}\n"
        except:
            continue

    await ctx.send(msg)


@bot.command()
async def giveaway(ctx, seconds: int):

    allowed_roles = ["Admin", "Moderator"]
    roles = [r.name for r in ctx.author.roles]

    if not any(r in allowed_roles for r in roles):
        await ctx.send("❌ Keine Rechte")
        return

    msg = await ctx.send(
        f"@everyone 🎉 GIVEAWAY!\n"
        f"Reagiere mit 🎉\n"
        f"⏳ {seconds}s",
        allowed_mentions=discord.AllowedMentions(everyone=True)
    )

    await msg.add_reaction("🎉")

    await asyncio.sleep(seconds)

    msg = await ctx.channel.fetch_message(msg.id)

    users = []

    for reaction in msg.reactions:
        if str(reaction.emoji) == "🎉":
            async for user in reaction.users():
                if not user.bot:
                    users.append(user)

    if not users:
        await ctx.send("❌ Niemand hat teilgenommen")
        return

    winner = random.choice(users)

    await ctx.send(f"🎉 Gewinner: {winner.mention}")


@bot.command()
async def helpme(ctx):
    await ctx.send(
        """
🎡 Button → Spin
🔥 !streak → Streak
💎 !premium → Premium Status
🏆 !leaderboard
🎁 !giveaway (Admin)
"""
    )

# ======================
# ERROR HANDLER
# ======================
@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Command Fehler: {error}")
    await ctx.send("❌ Ein Fehler ist aufgetreten")

# ======================
# START BOT
# ======================
bot.run(TOKEN, reconnect=True)
