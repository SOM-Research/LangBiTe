ui_schema = {
    "ui:spacing": 3,
    "requirements": {
        "ui:options": {
            "addable": True,
            "removable": True,
            "orderable": False,
            "addableText": "Add New Requirement"
        },
        "items": {
            "ui:classNames": "card p-3 mb-3 border-primary shadow-sm",
            "languages": {
                "ui:widget": "hidden"
            },
            "inputs": {
                "ui:widget": "checkboxes"
            },
            "reflections": {
                "ui:widget": "checkboxes"
            },
            "rationale": {
                "ui:widget": "textarea",
                "ui:rows": 2
            },
            "communities": {
                "ui:options": {
                    "addable": True,
                    "removable": True,
                    "orderable": False,
                    "addableText": "Add New Community"
                },
                "items": {
                    "ui:classNames": "card p-3 mb-3 border-primary shadow-sm",
                }
            }
        }
    }
}