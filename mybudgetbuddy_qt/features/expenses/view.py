from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer

from features.budget.service import clean_name, match_name, parse_amount
from .service import (
    copy_expenses, delete_expenses, filter_by_category,
    total as expenses_total
)

# ----- Theme: colors and styles used by this screen -----
BURGUNDY = "#900020"
DARK_BURGUNDY = "#700018"
GOLD = "#C9A227"
CREAM = "#FFF9EC"
WHITE = "#FFFFFF"
BLACK = "#000000"
RED = "#B42318"
GRAY = "#6B6B6B"
LIGHT = "#EEEEEE"
LINE = "#D8D0BE"
FONT = "'Georgia'"


def button_style(kind="primary"):
    # (background, text, border, hover background)
    colors = {
        "primary": (BURGUNDY, WHITE, BURGUNDY, DARK_BURGUNDY),
        "secondary": (WHITE, BLACK, BLACK, LIGHT),
        "danger": (RED, WHITE, RED, "#8F1B12"),
        "gold": (GOLD, BLACK, GOLD, "#B08D1E"),
    }
    bg, fg, border, hover = colors[kind]
    return f"""
        QPushButton {{
            background:{bg};
            color:{fg};
            border:2px solid {border};
            border-radius:8px;
            font-family:{FONT};
            font-size:15px;
            font-weight:bold;
            padding:6px 14px;
        }}
        QPushButton:hover {{
            background:{hover};
            color:{fg};
        }}
        QPushButton:disabled {{
            background:#E4E0D6;
            color:#9A9A9A;
            border:2px solid #CFC9BA;
        }}
    """


def icon_button_style():
    """Small square button holding an emoji icon (eye / pencil / trash)."""
    return f"""
        QPushButton {{
            background:{WHITE};
            border:1px solid {LINE};
            border-radius:6px;
            font-size:16px;
        }}
        QPushButton:hover {{
            background:{GOLD};
            border:1px solid {BURGUNDY};
        }}
    """


def input_style(size=15):
    return f"""
        QLineEdit {{
            background:{WHITE};
            color:{BLACK};
            border:2px solid #B9B2A3;
            border-radius:6px;
            padding:4px 8px;
            font-family:{FONT};
            font-size:{size}px;
        }}
        QLineEdit:focus {{
            border:2px solid {BURGUNDY};
        }}
        QLineEdit:read-only {{
            background:#F1ECE1;
            color:#444444;
        }}
    """


def combo_style():
    return f"""
        QComboBox {{
            background:{WHITE};
            color:{BLACK};
            border:2px solid #B9B2A3;
            border-radius:6px;
            padding:4px 8px;
            font-family:{FONT};
            font-size:15px;
        }}
        QComboBox:focus {{
            border:2px solid {BURGUNDY};
        }}
        QComboBox QAbstractItemView {{
            background:{WHITE};
            color:{BLACK};
            selection-background-color:{BURGUNDY};
            selection-color:{WHITE};
        }}
    """


def scrollbar_style():
    return f"""
        QScrollBar:vertical {{
            background:#EFE8D8;
            width:12px;
            border-radius:6px;
            margin:0;
        }}
        QScrollBar::handle:vertical {{
            background:{BURGUNDY};
            border-radius:6px;
            min-height:30px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height:0;
        }}
    """


def scroll_style(background=CREAM, border=True):
    frame = f"1px solid {LINE}" if border else "none"
    return f"""
        QScrollArea {{
            border:{frame};
            border-radius:8px;
            background:{background};
        }}
        QWidget#holder {{
            background:{background};
        }}
        {scrollbar_style()}
    """


def table_style():
    return f"""
        QTableWidget {{
            background:{WHITE};
            alternate-background-color:{CREAM};
            color:{BLACK};
            gridline-color:#E2DAC8;
            font-size:15px;
            border:1px solid {LINE};
            border-radius:6px;
        }}
        QHeaderView::section {{
            background:{BURGUNDY};
            color:{WHITE};
            font-weight:bold;
            padding:8px;
            border:none;
        }}
        QTableWidget::item:selected {{
            background:#F3D9DE;
            color:{BLACK};
        }}
        {scrollbar_style()}
    """


def dialog_style():
    return f"""
        QDialog {{
            background:{WHITE};
        }}
        QLabel {{
            color:{BLACK};
            font-size:15px;
        }}
        QFrame#banner {{
            background:{BURGUNDY};
            border-bottom:4px solid {GOLD};
        }}
        QLabel#bannerTitle {{
            color:{WHITE};
            background:transparent;
            font-family:{FONT};
            font-size:26px;
            font-weight:bold;
        }}
    """


CATEGORY_WIDTH = 190
AMOUNT_WIDTH = 140
REMOVE_WIDTH = 38
ACTION_WIDTH = 84

# Icon + tooltip of each page that can be opened from an Action column.
ICONS = {
    "view": ("👁️", "View Expenses"),
    "edit": ("✏️", "Edit Expenses"),
    "delete": ("🗑️", "Delete Expenses")
}


def action_buttons(go_to, index, actions):
    """Widget with one icon button per action.

    Each button is a shortcut to the matching page (View / Edit / Delete)
    for the expense at `index`: go_to(action, index) is called on click.
    """
    box = QWidget()

    layout = QHBoxLayout(box)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(6)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    for action in actions:
        icon, title = ICONS[action]

        button = QPushButton(icon)
        button.setFixedSize(34, 34)
        button.setToolTip(title)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet(icon_button_style())
        button.clicked.connect(
            lambda _=False, a=action: go_to(a, index)
        )
        layout.addWidget(button)

    return box


def column_header(removable=False, actions=False):
    """Fixed header line shown above the scrollable rows."""
    row = QHBoxLayout()
    row.setContentsMargins(20, 0, 32, 0)
    row.setSpacing(8)

    for text, width in (
        ("Category", CATEGORY_WIDTH),
        ("Description", None),
        ("Amount (₱)", AMOUNT_WIDTH)
    ):
        label = QLabel(text)
        label.setStyleSheet(
            f"color:{BLACK};font-size:15px;font-weight:bold;"
        )

        if width:
            label.setFixedWidth(width)
            row.addWidget(label)
        else:
            row.addWidget(label, 1)

    if actions:
        label = QLabel("Action")
        label.setFixedWidth(ACTION_WIDTH)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color:{BLACK};font-size:15px;font-weight:bold;"
        )
        row.addWidget(label)

    if removable:
        spacer = QWidget()
        spacer.setFixedWidth(REMOVE_WIDTH)
        row.addWidget(spacer)

    return row


class FormDialog(QDialog):
    """Base dialog: banner, hint, toolbar, body and Cancel/Close/Save.

    Subclasses fill `self.toolbar` and `self.body` and override
    has_changes(), reset() and on_save().

    Cancel -> discard unsaved changes and restore the original values
              (stays open; disabled until something changed).
    Close  -> leave the window (asks first if there are unsaved changes).
    Save   -> validate, save and close.
    """

    def __init__(self, parent, title, hint, size=(860, 640),
                 show_cancel=True, show_save=True):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setFixedSize(*size)
        self.setStyleSheet(dialog_style())

        # Set by go_to() when an Action icon asks for another page.
        self.shortcut = None

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        banner = QFrame()
        banner.setObjectName("banner")
        banner.setFixedHeight(76)

        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(25, 0, 25, 0)

        heading = QLabel(title)
        heading.setObjectName("bannerTitle")
        banner_layout.addWidget(heading)
        root.addWidget(banner)

        inner = QVBoxLayout()
        inner.setContentsMargins(25, 14, 25, 18)
        inner.setSpacing(10)
        root.addLayout(inner, 1)

        hint_label = QLabel(hint)
        hint_label.setWordWrap(True)
        hint_label.setStyleSheet(f"color:{GRAY};font-size:14px;")
        inner.addWidget(hint_label)

        self.toolbar = QHBoxLayout()
        self.toolbar.setSpacing(10)
        inner.addLayout(self.toolbar)

        self.body = QVBoxLayout()
        self.body.setSpacing(6)
        inner.addLayout(self.body, 1)

        footer = QHBoxLayout()
        footer.setSpacing(12)
        footer.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        self.cancel_button.setEnabled(False)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save)

        styles = {
            self.cancel_button: "secondary",
            self.close_button: "secondary",
            self.save_button: "primary"
        }

        for button, kind in styles.items():
            button.setFixedSize(150, 44)
            button.setStyleSheet(button_style(kind))

        self.cancel_button.setVisible(show_cancel)
        self.save_button.setVisible(show_save)

        footer.addWidget(self.cancel_button)
        footer.addWidget(self.close_button)
        footer.addWidget(self.save_button)
        footer.addStretch()
        inner.addLayout(footer)

    # ----- hooks for subclasses -----
    def has_changes(self):
        return False

    def reset(self):
        pass

    def on_save(self):
        self.accept()

    # ----- shared behaviour -----
    def changed(self, *_):
        self.cancel_button.setEnabled(self.has_changes())

    def on_cancel(self):
        if self.has_changes() and self.confirm(
            "Cancel",
            "Discard your changes and restore the original values?"
        ):
            self.reset()
            self.changed()

    def go_to(self, action, index):
        """Icon shortcut: close this window so the dashboard can open
        the View / Edit / Delete page for the expense at `index`."""
        self.shortcut = (action, index)
        self.reject()

        if self.isVisible():
            # The user chose to stay (unsaved changes), so stay here.
            self.shortcut = None

    def confirm(self, title, text):
        """Yes / No question. Returns True only when the user clicks Yes.

        Uses explicit, styled Yes and No buttons so both are always
        visible. No is the default, and Esc / the X button count as No.
        """
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle(title)
        box.setText(text)
        box.setStyleSheet(
            f"QMessageBox {{ background:{WHITE}; }}"
            f"QLabel {{ color:{BLACK}; font-size:15px; }}"
        )

        yes = box.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        no = box.addButton("No", QMessageBox.ButtonRole.NoRole)
        box.setDefaultButton(no)
        box.setEscapeButton(no)

        for button, kind in ((yes, "primary"), (no, "secondary")):
            button.setMinimumSize(90, 36)
            button.setStyleSheet(button_style(kind))

        box.exec()
        return box.clickedButton() is yes

    def warn(self, text):
        QMessageBox.warning(self, self.windowTitle(), text)

    def reject(self):
        # Used by the Close button, the Esc key and the window's X button.
        if self.has_changes() and not self.confirm(
            "Close", "You have unsaved changes. Close without saving?"
        ):
            return

        super().reject()

    def scroll_layout(self):
        """Add a scrollable area to the body and return its layout."""
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(scroll_style())
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        holder = QWidget()
        holder.setObjectName("holder")

        layout = QVBoxLayout(holder)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.scroll.setWidget(holder)
        self.body.addWidget(self.scroll, 1)

        return layout

    def scroll_to_bottom(self):
        bar = self.scroll.verticalScrollBar()
        bar.setValue(bar.maximum())


class ExpenseRow(QFrame):
    """One expense: category (pick or type a new one), description, amount."""

    def __init__(self, categories, category="", description="", amount="",
                 removable=True, on_change=None, on_remove=None,
                 action_widget=None):
        super().__init__()

        self.on_change = on_change
        self.on_remove = on_remove

        self.setObjectName("expenseRow")
        self.setStyleSheet(
            f"QFrame#expenseRow {{ background:{WHITE};"
            f"border:1px solid {LINE}; border-radius:8px; }}"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        self.category = QComboBox()
        self.category.setEditable(True)
        self.category.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.category.addItems(categories)
        self.category.setCurrentIndex(-1)
        self.category.setCurrentText(category)
        self.category.lineEdit().setPlaceholderText("Category")
        self.category.setFixedSize(CATEGORY_WIDTH, 38)
        self.category.setStyleSheet(combo_style())
        self.category.editTextChanged.connect(self.notify)
        layout.addWidget(self.category)

        self.description = QLineEdit(description)
        self.description.setPlaceholderText("What did you spend on?")
        self.description.setFixedHeight(38)
        self.description.setStyleSheet(input_style())
        self.description.textChanged.connect(self.notify)
        layout.addWidget(self.description, 1)

        self.amount = QLineEdit(amount)
        self.amount.setPlaceholderText("0.00")
        self.amount.setFixedSize(AMOUNT_WIDTH, 38)
        self.amount.setStyleSheet(input_style())
        self.amount.textChanged.connect(self.notify)
        layout.addWidget(self.amount)

        if action_widget is not None:
            action_widget.setFixedWidth(ACTION_WIDTH)
            layout.addWidget(action_widget)

        if removable:
            remove = QPushButton("✕")
            remove.setFixedSize(REMOVE_WIDTH - 2, 38)
            remove.setStyleSheet(button_style("danger"))
            remove.clicked.connect(self.remove)
            layout.addWidget(remove)

    def notify(self, *_):
        if self.on_change:
            self.on_change()

    def remove(self):
        if self.on_remove:
            self.on_remove(self)

    def values(self):
        return (
            clean_name(self.category.currentText()),
            self.description.text().strip(),
            self.amount.text().strip()
        )

    def set_values(self, category, description, amount):
        self.category.setCurrentText(category)
        self.description.setText(description)
        self.amount.setText(amount)


class ExpenseFormDialog(FormDialog):
    """Add any number of expenses, in any category."""

    START_ROWS = 3

    def __init__(self, parent, categories, title="Add Expenses"):
        super().__init__(
            parent, title,
            "Add as many expenses as you need. Pick a category from the "
            "list or type a new one."
        )

        self.categories = list(categories)
        self.rows = []
        self._expenses = []

        add_row_button = QPushButton("＋ Add Row")
        add_row_button.setFixedSize(150, 38)
        add_row_button.setStyleSheet(button_style("gold"))
        add_row_button.clicked.connect(self.add_row)
        self.toolbar.addWidget(add_row_button)
        self.toolbar.addStretch()

        self.body.addLayout(column_header(True))
        self.rows_layout = self.scroll_layout()

        self.build_rows()
        self.changed()

    def build_rows(self):
        for _ in range(self.START_ROWS):
            self.add_row(scroll=False)

    def clear_rows(self):
        for row in self.rows:
            self.rows_layout.removeWidget(row)
            row.deleteLater()

        self.rows = []

    def add_row(self, *_, scroll=True):
        row = ExpenseRow(
            self.categories,
            removable=True,
            on_change=self.changed,
            on_remove=self.remove_row
        )
        self.rows.append(row)
        self.rows_layout.addWidget(row)

        if scroll:
            row.category.setFocus()
            QTimer.singleShot(0, self.scroll_to_bottom)

        self.changed()

    def remove_row(self, row):
        # Ask Yes / No first, but only if the row has something typed in it.
        if any(row.values()) and not self.confirm(
            "Remove Row", "Remove this row?"
        ):
            return

        if len(self.rows) == 1:
            row.set_values("", "", "")
            return

        self.rows.remove(row)
        self.rows_layout.removeWidget(row)
        row.deleteLater()
        self.changed()

    def has_changes(self):
        return any(any(row.values()) for row in self.rows)

    def reset(self):
        self.clear_rows()
        self.build_rows()

    def on_save(self):
        entries = []

        for number, row in enumerate(self.rows, 1):
            category, description, amount_text = row.values()

            if not description and not amount_text:
                continue

            if not category:
                self.warn(f"Please enter a category for row {number}.")
                return

            if not description:
                self.warn(f"Please enter a description for row {number}.")
                return

            amount = parse_amount(amount_text)

            if amount is None:
                self.warn(
                    f"Please enter a valid amount for row {number} "
                    f"({description})."
                )
                return

            category = match_name(self.categories, category) or category
            entries.append((description, category, amount))

        if not entries:
            self.warn("Please enter at least one expense.")
            return

        self._expenses = entries
        self.accept()

    def values(self):
        return self._expenses


class ExpenseEditDialog(FormDialog):
    """Edit the description, category and amount of every expense."""

    def __init__(self, parent, expenses, categories, focus_index=None):
        super().__init__(
            parent, "Edit Expenses",
            "Change any description, category or amount, then click Save. "
            "You can also type a new category."
        )

        self.original = copy_expenses(expenses)
        self.categories = list(categories)
        self.rows = []
        self._result = None

        self.original_values = [
            (e["category"], e["description"], f"{e['amount']:.2f}")
            for e in self.original
        ]

        self.body.addLayout(column_header(actions=True))
        layout = self.scroll_layout()

        for index, values in enumerate(self.original_values):
            category, description, amount = values
            row = ExpenseRow(
                self.categories, category, description, amount,
                removable=False, on_change=self.changed,
                action_widget=action_buttons(
                    self.go_to, index, ("view", "delete")
                )
            )
            self.rows.append(row)
            layout.addWidget(row)

        self.changed()

        if focus_index is not None and 0 <= focus_index < len(self.rows):
            row = self.rows[focus_index]
            QTimer.singleShot(
                0,
                lambda: (
                    self.scroll.ensureWidgetVisible(row),
                    row.description.setFocus()
                )
            )

    def has_changes(self):
        return [row.values() for row in self.rows] != self.original_values

    def reset(self):
        for row, values in zip(self.rows, self.original_values):
            row.set_values(*values)

    def on_save(self):
        updated = []

        for number, row in enumerate(self.rows, 1):
            category, description, amount_text = row.values()

            if not description:
                self.warn(f"Description cannot be empty (row {number}).")
                return

            if not category:
                self.warn(f"Please enter a category for {description}.")
                return

            amount = parse_amount(amount_text)

            if amount is None:
                self.warn(f"Please enter a valid amount for {description}.")
                return

            category = match_name(self.categories, category) or category
            updated.append({
                "description": description,
                "category": category,
                "amount": amount
            })

        self._result = updated
        self.accept()

    def result_expenses(self):
        return self._result if self._result is not None else self.original


class ExpenseListDialog(FormDialog):
    """Scrollable, filterable expense table.

    mode="view"   -> read-only list with a Close button.
    mode="delete" -> select expenses, click Delete Selected, answer
                     Yes / No. Yes deletes them and closes the window.

    The Action column holds icon shortcuts to the other two pages.
    """

    def __init__(self, parent, expenses, categories, mode="view",
                 focus_index=None):
        deleting = mode == "delete"

        super().__init__(
            parent,
            "Delete Expenses" if deleting else "View Expenses",
            "Select one or more expenses and click Delete Selected. "
            "You will be asked to confirm with Yes or No."
            if deleting else
            "Browse all of your recorded expenses. Use the category "
            "filter to focus on one category.",
            size=(900, 640),
            show_cancel=False,
            show_save=False
        )

        self.mode = mode
        self.original = copy_expenses(expenses)
        self.items = copy_expenses(expenses)
        # origin[i] = position of items[i] in the saved expense list, so an
        # Action icon always refers to the right expense.
        self.origin = list(range(len(self.items)))
        self.row_index = []
        self._result = None
        self.shortcut_actions = (
            ("view", "edit") if deleting else ("edit", "delete")
        )

        # ----- toolbar: category filter, summary, delete button -----
        filter_label = QLabel("Category:")
        filter_label.setStyleSheet(
            f"color:{BLACK};font-size:15px;font-weight:bold;"
        )
        self.toolbar.addWidget(filter_label)

        self.filter = QComboBox()
        self.filter.setFixedSize(220, 38)
        self.filter.setStyleSheet(combo_style())
        self.filter.addItem("All Categories", None)

        names = list(categories)

        for expense in self.items:
            if expense["category"] not in names:
                names.append(expense["category"])

        for name in names:
            self.filter.addItem(name, name)

        self.filter.currentIndexChanged.connect(self.refresh)
        self.toolbar.addWidget(self.filter)

        self.toolbar.addStretch()

        self.info = QLabel("")
        self.info.setStyleSheet(
            f"color:{BURGUNDY};font-size:15px;font-weight:bold;"
        )
        self.toolbar.addWidget(self.info)

        if deleting:
            delete_button = QPushButton("Delete Selected")
            delete_button.setFixedSize(170, 38)
            delete_button.setStyleSheet(button_style("danger"))
            delete_button.clicked.connect(self.delete_selected)
            self.toolbar.addWidget(delete_button)

        # ----- table (scrolls automatically) -----
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Description", "Category", "Amount", "Action"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 190)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 120)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
            if deleting else
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setStyleSheet(table_style())
        self.body.addWidget(self.table, 1)

        self.refresh()

        if focus_index is not None:
            QTimer.singleShot(0, lambda: self.focus_expense(focus_index))

    def focus_expense(self, index):
        """Select and scroll to the expense at `index` (saved position)."""
        for row, position in enumerate(self.row_index):
            if self.origin[position] == index:
                self.table.selectRow(row)
                self.table.scrollToItem(self.table.item(row, 0))
                return

    def refresh(self, *_):
        category = self.filter.currentData()
        rows = filter_by_category(self.items, category)

        self.row_index = [index for index, _ in rows]
        self.table.setRowCount(len(rows))

        for row, (position, expense) in enumerate(rows):
            cells = [
                expense["description"],
                expense["category"],
                f"₱{expense['amount']:,.2f}"
            ]

            for column, text in enumerate(cells):
                item = QTableWidgetItem(text)

                if column == 2:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight |
                        Qt.AlignmentFlag.AlignVCenter
                    )

                self.table.setItem(row, column, item)

            self.table.setCellWidget(
                row, 3,
                action_buttons(
                    self.go_to, self.origin[position],
                    self.shortcut_actions
                )
            )
            self.table.setRowHeight(row, 46)

        shown_total = expenses_total([expense for _, expense in rows])
        self.info.setText(
            f"{len(rows)} expense(s)  •  ₱{shown_total:,.2f}"
        )

    def delete_selected(self):
        selected = sorted({
            index.row()
            for index in self.table.selectionModel().selectedRows()
        })

        if not selected:
            self.warn("Please select at least one expense.")
            return

        if not self.confirm(
            "Delete Expenses",
            f"Are you sure you want to delete {len(selected)} "
            "selected expense(s)?\n\nThis cannot be undone."
        ):
            return  # user clicked No: nothing is deleted

        # User clicked Yes. Convert visible table rows to positions in the
        # expense list (correct even when a category filter is active),
        # delete them, then close the window so the dashboard saves them.
        positions = [self.row_index[row] for row in selected]
        delete_expenses(self.items, positions)

        self._result = self.items
        self.accept()

    # Nothing is left pending in this window: Yes deletes immediately.
    def has_changes(self):
        return False

    def result_expenses(self):
        return self._result if self._result is not None else self.original