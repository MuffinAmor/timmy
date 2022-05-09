import discord
from discord.ui import InputText, Modal

from lib.Cache import servers, SomeFreeSpace
from lib.ModerationHandler import InviteValidation
from lib.setting_menu import DescriptionStuff, InviteStuff


class MyModal(Modal):
    def __init__(self, server):
        super().__init__(f"Description Setup for \n{server.name[0:20]}")
        self.server = server
        self.server_name = server.name
        self.server_id = server.id
        self.add_item(
            InputText(
                label="Description of your Server:",
                value=SomeFreeSpace(self.server_id).get_description(),
                placeholder="We are very awesome!",
                style=discord.InputTextStyle.multiline,
                min_length=50,
                max_length=800
            )
        )
        self.add_item(
            InputText(
                label="Invite for your Server:",
                value=SomeFreeSpace(self.server_id).get_invite(),
                placeholder="https://discord.gg/....",
                style=discord.InputTextStyle.short
            )

        )

    async def callback(self, interaction: discord.Interaction):
        if InviteValidation(self.children[1].value).exist(self.server):
            InviteStuff(interaction.guild_id, "").set_invite()
            await interaction.response.send_message("What are you doing?\nPlease use an invite for this server.")
        elif InviteValidation(self.children[1].value).formation():
            InviteStuff(interaction.guild_id, "").set_invite()
            await interaction.response.send_message("Please use a valid discord invite link.")
        else:
            InviteStuff(interaction.guild_id, self.children[1].value).set_invite()
            await interaction.response.send_message("The description has been changed successfully!")
        DescriptionStuff(interaction.guild_id, self.children[0].value).set_description()
        servers.cache_clear()
