import discord
from discord.ext import commands
from discord.ui import Select, View
import asyncio

# Configurar los intents para recibir eventos del servidor
intents = discord.Intents.default()
intents.message_content = True  # Permite leer el contenido de los mensajes

# Inicializar el bot con los intents y el prefijo
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Bot {bot.user} está listo y funcionando!")

# Comando para enviar el mensaje con el combo box
@bot.command()
@commands.has_role("©┃Owner")  # Solo los usuarios con este rol pueden ejecutar el comando
async def bienvenida(ctx):
    # Crear el Embed para el mensaje de bienvenida
    embed = discord.Embed(
        title="Ticket General",
        description="Abre el ticket para poder realizar una compra o consulta respecto al producto...",
        color=discord.Color.from_rgb(255, 255, 255)  # Color blanco (lo más claro posible)
    )

    # Añadir imagen y descripción del copyright
    embed.set_footer(text="Copyright © 2024 | Hyper Nova")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1318978275149873283/1319393604661280862/T3XPoezATpiDMIfK2MHPRg.png?ex=6765cc8c&is=67647b0c&hm=7ba149bcc0eb559b8296aa32a49b1dd284c7eda84430ed5fa2641ada61f2c3ef&")

    # Crear el Select (ComboBox)
    select = Select(
        placeholder="Selecciona una opción...",
        options=[
            discord.SelectOption(label="Soporte", description="Recibe asistencia de nuestro equipo", emoji="🛠️"),
            discord.SelectOption(label="Dudas", description="Resolvemos tus inquietudes", emoji="❓"),
            discord.SelectOption(label="Adquirir un Producto", description="Compra nuestros productos", emoji="🛒")
        ]
    )

    # Función para manejar la selección
    async def select_callback(interaction):
        # Obtener los roles de los que pueden ver el canal
        owner_role = discord.utils.get(ctx.guild.roles, name="©┃Owner")
        seller_role = discord.utils.get(ctx.guild.roles, name="🛒┃Seller")

        if select.values[0] == "Soporte":
            category = discord.utils.get(ctx.guild.categories, name="Soporte")
            if not category:
                category = await ctx.guild.create_category("Soporte")
            ticket_channel = await ctx.guild.create_text_channel("soporte-" + interaction.user.name, category=category)

            # Establecer permisos del canal
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)  # Evita que otros vean el canal
            await ticket_channel.set_permissions(owner_role, read_messages=True)  # Permite que el rol Owner vea el canal
            await ticket_channel.set_permissions(seller_role, read_messages=True)  # Permite que el rol Seller vea el canal
            await ticket_channel.set_permissions(interaction.user, read_messages=True)  # Permite que el usuario vea el canal

            await ticket_channel.send(f"¡Hola {interaction.user.mention}! Este es tu canal de soporte. ¿En qué podemos ayudarte?")
            await interaction.response.send_message(f"¡Se ha creado un canal de soporte para ti! {ticket_channel.mention}", ephemeral=True)
            await asyncio.sleep(1)  # Retraso de 1 segundo para evitar demasiada actividad simultánea

        elif select.values[0] == "Dudas":
            category = discord.utils.get(ctx.guild.categories, name="Dudas")
            if not category:
                category = await ctx.guild.create_category("Dudas")
            ticket_channel = await ctx.guild.create_text_channel("dudas-" + interaction.user.name, category=category)

            # Establecer permisos del canal
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)  # Evita que otros vean el canal
            await ticket_channel.set_permissions(owner_role, read_messages=True)  # Permite que el rol Owner vea el canal
            await ticket_channel.set_permissions(seller_role, read_messages=True)  # Permite que el rol Seller vea el canal
            await ticket_channel.set_permissions(interaction.user, read_messages=True)  # Permite que el usuario vea el canal

            await ticket_channel.send(f"¡Hola {interaction.user.mention}! Este es tu canal de dudas. ¿En qué podemos ayudarte?")
            await interaction.response.send_message(f"¡Se ha creado un canal de dudas para ti! {ticket_channel.mention}", ephemeral=True)
            await asyncio.sleep(1)  # Retraso de 1 segundo

        elif select.values[0] == "Adquirir un Producto":
            category = discord.utils.get(ctx.guild.categories, name="Compras")
            if not category:
                category = await ctx.guild.create_category("Compras")
            ticket_channel = await ctx.guild.create_text_channel("compra-" + interaction.user.name, category=category)

            # Establecer permisos del canal
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)  # Evita que otros vean el canal
            await ticket_channel.set_permissions(owner_role, read_messages=True)  # Permite que el rol Owner vea el canal
            await ticket_channel.set_permissions(seller_role, read_messages=True)  # Permite que el rol Seller vea el canal
            await ticket_channel.set_permissions(interaction.user, read_messages=True)  # Permite que el usuario vea el canal

            await ticket_channel.send(f"¡Hola {interaction.user.mention}! Este es tu canal de compra. ¿Qué producto deseas adquirir?")
            await interaction.response.send_message(f"¡Se ha creado un canal de compra para ti! {ticket_channel.mention}", ephemeral=True)
            await asyncio.sleep(1)  # Retraso de 1 segundo

    # Asignar el callback al select
    select.callback = select_callback

    # Crear la vista para añadir el Select al mensaje
    view = View()
    view.add_item(select)

    # Enviar el mensaje con el embed y la vista (con el ComboBox)
    await ctx.send(embed=embed, view=view)

# Manejar errores de permisos
@bienvenida.error
async def bienvenida_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("No tienes permisos💀🙏", delete_after=1)

# Token del bot (asegúrate de mantenerlo privado)
bot.run('MTI4MTY3NjM4MTk4NTQ0NDAyMw.GDlf6a.qNr3m2FKKMGv7x4s637Kz2qcqbmTD3sx5LUuOE')