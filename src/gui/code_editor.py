"""
Code Editor with LEGv8 Assembly Syntax Highlighting
"""

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import (QTextCharFormat, QColor, QFont, QPainter, 
                         QSyntaxHighlighter, QTextDocument, QPalette)
import re


class LEGv8SyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for LEGv8 assembly language"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        # Define colors
        self.instruction_color = QColor(86, 156, 214)  # Light blue
        self.register_color = QColor(156, 220, 254)    # Cyan
        self.immediate_color = QColor(181, 206, 168)   # Light green
        self.comment_color = QColor(106, 153, 85)      # Green
        self.label_color = QColor(220, 220, 170)       # Light yellow
        self.error_color = QColor(244, 71, 71)         # Red
        
        # Define text formats
        instruction_format = QTextCharFormat()
        instruction_format.setForeground(self.instruction_color)
        instruction_format.setFontWeight(QFont.Weight.Bold)
        
        register_format = QTextCharFormat()
        register_format.setForeground(self.register_color)
        
        immediate_format = QTextCharFormat()
        immediate_format.setForeground(self.immediate_color)
        
        comment_format = QTextCharFormat()
        comment_format.setForeground(self.comment_color)
        comment_format.setFontItalic(True)
        
        # Define patterns
        instructions = [
            'ADD', 'ADDS', 'SUB', 'SUBS', 'MUL', 'SMULH', 'UMULH', 'SDIV', 'UDIV', 'AND', 'ORR', 'EOR', 'LSL', 'LSR',
            'ADDI', 'ADDIS', 'SUBI', 'SUBIS', 'ANDI', 'ORRI', 'EORI', 'MOVZ', 'MOVK',
            'LDUR', 'STUR', 'LDURW', 'STURW', 'LDURB', 'STURB',
            'CMP', 'CMPI',
            'B', 'BL', 'BR', 'CBZ', 'CBNZ'
        ]
        
        # Add highlighting rules
        for instruction in instructions:
            pattern = f'\\\\b{instruction}\\\\b'
            self.highlighting_rules.append((re.compile(pattern, re.IGNORECASE), instruction_format))
        
        # Conditional branches (B.EQ, B.NE, etc.)
        self.highlighting_rules.append((re.compile(r'\\bB\\.(EQ|NE|LT|LE|GT|GE|LO|LS|HI|HS)\\b', re.IGNORECASE), instruction_format))
        
        # Labels (word followed by colon)
        label_format = QTextCharFormat()
        label_format.setForeground(QColor(220, 220, 170))  # Light yellow
        label_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((re.compile(r'\\b[A-Za-z_][A-Za-z0-9_]*:', re.IGNORECASE), label_format))
        
        # Registers (X0-X31, SP, LR, XZR, FP)
        self.highlighting_rules.append((re.compile(r'\\bX\d{1,2}\\b', re.IGNORECASE), register_format))
        self.highlighting_rules.append((re.compile(r'\\b(SP|LR|XZR|FP)\\b', re.IGNORECASE), register_format))
        
        # Immediate values
        self.highlighting_rules.append((re.compile(r'#-?\d+'), immediate_format))
        
        # Comments
        self.highlighting_rules.append((re.compile(r'//.*'), comment_format))
        
    def highlightBlock(self, text):
        """Apply syntax highlighting to a block of text"""
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, format)


class LineNumberArea(QWidget):
    """Line number area for the code editor"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor
        
    def sizeHint(self):
        return self.code_editor.lineNumberAreaWidth()
        
    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    """Code editor with line numbers and syntax highlighting"""
    
    def __init__(self):
        super().__init__()
        
        # Setup font
        font = QFont("Consolas", 11)
        font.setFixedPitch(True)
        self.setFont(font)
        
        # Line number area
        self.line_number_area = LineNumberArea(self)
        
        # Syntax highlighter
        self.highlighter = LEGv8SyntaxHighlighter(self.document())
        
        # Setup signals
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        
        self.updateLineNumberAreaWidth(0)
        
        # Current line highlighting
        self.current_line = -1
        self.highlight_current_execution_line()
        
        # Set default text
        self.setPlainText(
            "// LEGv8 Assembly"
        )
        
    def lineNumberAreaWidth(self):
        """Calculate width needed for line numbers"""
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
        
    def updateLineNumberAreaWidth(self, newBlockCount):
        """Update the width of the line number area"""
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
        
    def updateLineNumberArea(self, rect, dy):
        """Update the line number area when scrolling"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                       self.line_number_area.width(), 
                                       rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
            
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )
        
    def lineNumberAreaPaintEvent(self, event):
        """Paint the line number area"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(240, 240, 240))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                
                # Highlight current execution line
                if block_number == self.current_line:
                    painter.fillRect(0, int(top), self.line_number_area.width(), 
                                   int(self.fontMetrics().height()), 
                                   QColor(255, 255, 0, 100))  # Yellow highlight
                
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(0, int(top), self.line_number_area.width(), 
                               int(self.fontMetrics().height()),
                               Qt.AlignmentFlag.AlignRight, number)
                               
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
            
    def highlight_current_line(self, line_number: int):
        """Highlight the current execution line"""
        self.current_line = line_number - 1  # Convert to 0-based
        self.line_number_area.update()
        
        # Also highlight in the text area
        self.highlight_current_execution_line()
        
    def highlight_current_execution_line(self):
        """Highlight the current line being executed"""
        from PyQt6.QtWidgets import QTextEdit
        extra_selections = []
        
        if self.current_line >= 0:
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(255, 255, 0, 30)  # Light yellow
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            for _ in range(self.current_line):
                cursor.movePosition(cursor.MoveOperation.Down)
            selection.cursor = cursor
            extra_selections.append(selection)
            
        self.setExtraSelections(extra_selections)
        
    def clear_highlight(self):
        """Clear current line highlighting"""
        self.current_line = -1
        self.line_number_area.update()
        self.setExtraSelections([])
