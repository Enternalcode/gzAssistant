from nicegui import ui
import sqlite3
from datetime import datetime
from nicegui import events, ui
from apps.utils.config import APPLICATION_DATA_PATH

@ui.page('/qa')
async def faq_page():
    # Connect to SQLite database, create if it doesn't exist
    db_file= f"{APPLICATION_DATA_PATH}/data/gz.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            create_time TIMESTAMP,
            update_time TIMESTAMP
        )
    ''')
    conn.commit()

    # Function to add a question and answer directly to the table
    def add_question_answer():
        question = question_input.value
        answer = answer_input.value
        if question and answer:  # Ensure both fields are filled
            create_time = datetime.now()
            update_time = datetime.now()
            
            cursor.execute('''
                INSERT INTO questions_answers (question, answer, create_time, update_time)
                VALUES (?,?,?,?)
            ''', (question, answer, create_time, update_time))
            conn.commit()
            
            # Clear input fields after submission
            question_input.value = ''
            answer_input.value = ''
            
            # Update the rows for the table
            update_table()

    # Function to update the table with the latest data
    def update_table():
        cursor.execute('SELECT * FROM questions_answers')
        rows = [{'id': row[0], 'question': row[1], 'answer': row[2],
                'create_time': row[3][:19],  # Keep only 'YYYY-MM-DD HH:MM:SS'
                'update_time': row[4][:19]}  # Keep only 'YYYY-MM-DD HH:MM:SS'
                for row in cursor.fetchall()]
        table.rows = rows  # Update the table rows

    # Function to update a record
    def update_record(e: events.GenericEventArguments):
        for row in table.rows:
            if row['id'] == e.args['id']:
                question = e.args.get('question', row['question'])
                answer = e.args.get('answer', row['answer'])
                update_time = datetime.now()
                cursor.execute('''
                    UPDATE questions_answers
                    SET question =?, answer =?, update_time =?
                    WHERE id =?
                ''', (question, answer, update_time, e.args['id']))
                conn.commit()
        ui.notify(f'Updated rows to: {table.rows}')
        update_table()

    # Function to delete a record
    def delete_record(e: events.GenericEventArguments):
        cursor.execute('DELETE FROM questions_answers WHERE id =?', (e.args['id'],))
        conn.commit()
        ui.notify(f'Deleted row with ID {e.args["id"]}')
        update_table()

    # Define table columns with Chinese labels
    columns = [
        {'name': 'id', 'label': '编号', 'field': 'id', 'align': 'left'},
        {'name': 'question', 'label': '问题', 'field': 'question'},
        {'name': 'answer', 'label': '回答', 'field': 'answer'},
        {'name': 'create_time', 'label': '创建时间', 'field': 'create_time'},
        {'name': 'update_time', 'label': '更新时间', 'field': 'update_time'},
        {'name': 'delete', 'label': '删除', 'field': 'delete'}
    ]

    # Display input fields and add button
    with ui.card():
        question_input = ui.input('问题').classes('w-full')
        answer_input = ui.input('回答').classes('w-full')
        ui.button('添加', icon='add', color='accent', on_click=add_question_answer).classes('w-full')

    # Create the table
    table = ui.table(columns=columns, rows=[], row_key='id').classes('w-90')  # Initialize with an empty list
    update_table()  # Load initial data into the table

    # Table body slots for edit and delete
    table.add_slot('body', r'''
        <q-tr :props="props">
            <q-td key="id" :props="props">
                {{ props.row.id }}  <!-- Display ID -->
            </q-td>
            <q-td key="question" :props="props">
                {{ props.row.question }}
                <q-popup-edit v-model="props.row.question" v-slot="scope"
                    @update:model-value="() => $parent.$emit('update', props.row)"
                >
                    <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="answer" :props="props">
                {{ props.row.answer }}
                <q-popup-edit v-model="props.row.answer" v-slot="scope"
                    @update:model-value="() => $parent.$emit('update', props.row)"
                >
                    <q-input v-model.number="scope.value" type="text" dense autofocus counter @keyup.enter="scope.set" />
                </q-popup-edit>
            </q-td>
            <q-td key="create_time" :props="props">
                {{ props.row.create_time }}  <!-- Display Create Time -->
            </q-td>
            <q-td key="update_time" :props="props">
                {{ props.row.update_time }}  <!-- Display Update Time -->
            </q-td>
            <q-td auto-width>
                <q-btn size="sm" color="warning" round dense icon="delete"
                    @click="() => $parent.$emit('delete', props.row)"
                />
            </q-td>
        </q-tr>
    ''')

    table.on('update', update_record)
    table.on('delete', delete_record)

