import os
import disnake
import auraxium
import census


async def get_player(character_name):
    async with auraxium.Client(service_id=str(os.getenv('CENSUS_TOKEN'))) as client:
        character, current_world, outfit = await census.get_character(character_name, client)
        if character is None:
            return None
        faction_logo = [
            'https://census.daybreakgames.com/files/ps2/images/static/94.png',
            'https://census.daybreakgames.com/files/ps2/images/static/12.png',
            'https://census.daybreakgames.com/files/ps2/images/static/18.png',
            'https://wiki.planetside-universe.com/ps/images/3/3d/Logo_ns.png'
        ]
        faction_color = [0x440E62, 0x004B80, 0x9E0B0F, 0x5B5B5B]
        faction_id = int(character.faction_id)
        Message = disnake.Embed(
            title="__" + str(character.name) + ":__",
            color=faction_color[faction_id - 1],
            description="[Click here for Fisu Stats](https://ps2.fisu.pw/player/?name=" + str(character.name) + ")",
        )
        Message.set_thumbnail(
            url=faction_logo[faction_id - 1]
        )
        Message.add_field(
            name="Last Seen",
            value=str(character.times.last_save_date)[:16],
            inline=True
        )
        Message.add_field(
            name="Battle Rank",
            value=str(character.battle_rank.value),
            inline=False
        )
        Message.add_field(
            name="ASP",
            value=str(character.data.prestige_level),
            inline=False
        )
        Message.add_field(
            name="Created",
            value=str(character.times.creation_date)[:16],
            inline=True
        )
        Message.add_field(
            name="Playtime",
            value=str(round(character.times.minutes_played / 60)) + " Hours",
            inline=True
        )
        if outfit is not None:
            outfit_details = await client.get_by_id(auraxium.ps2.Outfit, outfit.outfit_id)
            Message.add_field(
                name="Outfit",
                value="[[" + str(outfit_details.data.alias) + "]](https://ps2.fisu.pw/outfit/?name=" +
                      str(outfit_details.data.alias_lower) + ") " + str(outfit_details.name),
                inline=False
            )
            Message.add_field(
                name="Rank",
                value=str(outfit.rank),
                inline=True
            )
            Message.add_field(
                name="Joined",
                value=str(outfit.member_since_date)[:16],
                inline=True
            )
    return Message
