from nicegui import ui
from typing import Dict

### VARIABLES

message_list = [
    {
        "role": "assistant",
        "content": "Placeholder test"
    },
    {
        "role": "user",
        "content": "Placeholder test allso"
    },
    {
        "role": "assistant",
        "content": "no way, that's what i was gonna say"
    }
]



columns = [
    {'name': 'thumbnail', 'label': 'Thumbnail', 'field': 'thumbnail'},
    {'name': 'id', 'label': 'ID', 'field': 'id'},
    {'name': 'name', 'label': 'Name', 'field': 'name'},
    {'name': 'status', 'label': 'Status', 'field': 'status'},
    {'name': 'spend', 'label': 'Spend', 'field': 'spend', 'sortable': True},
    {'name': 'email', 'label': 'Email', 'field': 'email'},
    {'name': 'phone', 'label': 'Phone', 'field': 'phone'},
    {'name': 'address', 'label': 'Address', 'field': 'address'},
    {'name': 'company', 'label': 'Company', 'field': 'company'},
    {'name': 'position', 'label': 'Position', 'field': 'position'},
    {'name': 'date_joined', 'label': 'Date Joined', 'field': 'date_joined'},
    {'name': 'new_column_1', 'label': 'New Column 1', 'field': 'new_column_1'},
    {'name': 'new_column_2', 'label': 'New Column 2', 'field': 'new_column_2'},
    {'name': 'new_column_3', 'label': 'New Column 3', 'field': 'new_column_3'},
    {'name': 'new_column_4', 'label': 'New Column 4', 'field': 'new_column_4'},
    {'name': 'new_column_5', 'label': 'New Column 5', 'field': 'new_column_5'},
    {'name': 'new_column_6', 'label': 'New Column 6', 'field': 'new_column_6'},
    {'name': 'new_column_7', 'label': 'New Column 7', 'field': 'new_column_7'},
    {'name': 'new_column_8', 'label': 'New Column 8', 'field': 'new_column_8'},
    {'name': 'new_column_9', 'label': 'New Column 9', 'field': 'new_column_9'},
    {'name': 'new_column_10', 'label': 'New Column 10', 'field': 'new_column_10'},
]



rows = [
    {'id': 'ADID67', 'name': 'Alice', 'status': 'active', "thumbnail": "https://via.placeholder.com/150"},
    {'id': 'ADID68', 'name': 'Bob', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "spend": 100},
    {'id': 'ADID70', 'name': 'pee pee poo poo', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "spend": 99},
    {'id': 'ADID69', 'name': 'Charlie', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 1", "new_column_2": "Data 2"},
    {'id': 'ADID70', 'name': 'David', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 3", "new_column_2": "Data 4"},
    {'id': 'ADID71', 'name': 'Eve', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 5", "new_column_2": "Data 6"},
    {'id': 'ADID72', 'name': 'Frank', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 7", "new_column_2": "Data 8"},
    {'id': 'ADID73', 'name': 'Grace', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 9", "new_column_2": "Data 10"},
    {'id': 'ADID74', 'name': 'Heidi', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 11", "new_column_2": "Data 12"},
    {'id': 'ADID75', 'name': 'Ivan', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 13", "new_column_2": "Data 14"},
    {'id': 'ADID76', 'name': 'Judy', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 15", "new_column_2": "Data 16"},
    {'id': 'ADID77', 'name': 'Karl', 'status': 'active', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 17", "new_column_2": "Data 18"},
    {'id': 'ADID78', 'name': 'Laura', 'status': 'inactive', "thumbnail": "https://via.placeholder.com/150", "new_column_1": "Data 19", "new_column_2": "Data 20"},
]




### FUNCTIONS

def on_click(text_input):
    user_message = text_input.value
    if user_message:
        # Append the user input to the message_list
        message_list.append({"role": "user", "content": user_message})
        # Clear the text input
        text_input.value = ''
        # Refresh the chat window
        display_chat_messages.refresh()
        # Scroll to the bottom of the chat window
        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        # Simulate sending the message to the backend and receiving a response
        response = {"role": "assistant", "content": "This is a response from the backend."}
        message_list.append(response)
        # Refresh the chat window again
        display_chat_messages.refresh()







### COMPONENTS

@ui.refreshable
def display_chat_messages():
    with ui.column().classes('w-full h-full items-stretch'):
        for message in message_list:
            if message['role'] == 'user':
                ui.label(f"{message['role']}: {message['content']}").classes('ml-auto my-2')
            else:
                ui.label(f"{message['role']}: {message['content']}").classes('mr-auto my-2')

def text_input():
    with ui.column().classes('w-full'):
        with ui.row().classes('w-full no-wrap items-center'):
            text = ui.input(placeholder='Type your message here...').props('rounded outlined input-class=mx-3') \
                .classes('flex-grow')
            ui.button('Submit', on_click=lambda: on_click(text))



def chat_window():
    with ui.column().classes('w-full h-full items-stretch'):
        ui.label('Chat Window').classes('text-center text-xl my-4')
    display_chat_messages()
    text_input()
        


def ads_table():
    def toggle(column: Dict, visible: bool) -> None:
        column['classes'] = '' if visible else 'hidden'
        column['headerClasses'] = '' if visible else 'hidden'
        table.update()

    def column_toggle_menu():
        with ui.button(icon='menu'):
            with ui.menu(), ui.column().classes('gap-0 p-2'):
                for column in columns:
                    ui.switch(column['label'], value=True, on_change=lambda e,
                            column=column: toggle(column, e.value))
        
    def table():
        table = ui.table(columns=columns, rows=rows, row_key='name')
        table.add_slot('body-cell-thumbnail', '''
            <q-td key="thumbnail" :props="props">
                <q-img :src="props.value" :ratio="1" />
            </q-td>
        ''')

    table()
    return table


def test_card():
    with ui.card():
        ui.label('Test Card')









### PAGES 
@ui.page('/')
def main():
    ui.dark_mode().enable()
    with ui.row().classes('w-full h-full items-stretch no-wrap'):
        with ui.column().classes('w-1/2 h-full'):
            chat_window()
        with ui.column().classes('w-1/2 h-full'):
            ads_table()


    # display_chat_messages()
    # text_input()


ui.run()