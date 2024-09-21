from netbox.plugins import PluginMenuButton, PluginMenuItem

staticroute_buttons = [
    PluginMenuButton(
        link='plugins:netbox_static_routes:staticroute_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_static_routes:staticroute_list',
        link_text='Static Routes',
    ),
)
