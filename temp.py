layout.addWidget(QLabel("Select Alert Type"))
        layout.addWidget(self.dropdown)
        layout.addSpacing(10)  # Add space after dropdown

        # Form layout for the fields
        db_form_layout = QFormLayout()
        db_form_layout.addRow(QLabel("Alert Name:"), self.alert_name_label)
        db_form_layout.addRow(QLabel("Alert Text:"), self.alert_text_label)
        db_form_layout.addRow(QLabel("Creator Id:"), self.creator_id_label)
        db_form_layout.addRow(QLabel("Category Code:"), self.category_code_label)