from imports import *

def show_crud_form(main_window, operation, table):
    form = QWidget()
    form_layout = QFormLayout(form)

    fields = main_window.get_fields_for_table(table)
    main_window.form_fields = {}

    if operation == "Delete":
        primary_key_field = main_window.get_primary_key_field(table)
        main_window.form_fields[primary_key_field] = QLineEdit()
        form_layout.addRow(f"{primary_key_field.replace('_', ' ').title()}:", main_window.form_fields[primary_key_field])
    else:
        for label, field_name in fields:
            main_window.form_fields[field_name] = QLineEdit()
            form_layout.addRow(label + ":", main_window.form_fields[field_name])

    submit_button = QPushButton(f"Submit {operation}")
    submit_button.clicked.connect(lambda: main_window.handle_crud_action(operation, table))
    form_layout.addWidget(submit_button)

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: main_window.stacked_widget.setCurrentWidget(main_window.pages[table]))
    form_layout.addWidget(back_button)

    main_window.stacked_widget.addWidget(form)
    main_window.stacked_widget.setCurrentWidget(form)