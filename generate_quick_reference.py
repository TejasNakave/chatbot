#!/usr/bin/env python3
"""
Quick Reference PDF Generator - One-page summary for the Document-Based Chatbot
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

class QuickReferenceGuide:
    def __init__(self, filename="Chatbot_Quick_Reference.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        self.setup_styles()

    def setup_styles(self):
        # Compact title
        self.title_style = ParagraphStyle(
            'CompactTitle',
            parent=self.styles['Title'],
            fontSize=20,
            spaceAfter=15,
            textColor=HexColor('#2E86AB'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Compact headings
        self.heading_style = ParagraphStyle(
            'CompactHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=8,
            textColor=HexColor('#A23B72'),
            fontName='Helvetica-Bold'
        )
        
        # Compact body
        self.body_style = ParagraphStyle(
            'CompactBody',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        
        # Command style
        self.cmd_style = ParagraphStyle(
            'CommandStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Courier-Bold',
            textColor=HexColor('#2E86AB'),
            spaceAfter=3
        )

    def generate_quick_reference(self):
        # Title
        self.story.append(Paragraph("🤖 Document Chatbot - Quick Reference", self.title_style))
        
        # Two-column layout using table
        left_content = [
            Paragraph("📋 Quick Start", self.heading_style),
            Paragraph("1. Install: <font name='Courier'>pip install -r requirements.txt</font>", self.body_style),
            Paragraph("2. Setup: Create .env with GEMINI_API_KEY", self.body_style),
            Paragraph("3. Documents: Add files to data/ folder", self.body_style),
            Paragraph("4. Run: <font name='Courier'>streamlit run streamlit_app.py</font>", self.body_style),
            
            Spacer(1, 8),
            Paragraph("🔍 Supported Formats", self.heading_style),
            Paragraph("• PDF documents (.pdf)", self.body_style),
            Paragraph("• Word documents (.docx)", self.body_style),
            Paragraph("• Text files (.txt)", self.body_style),
            
            Spacer(1, 8),
            Paragraph("💡 Example Questions", self.heading_style),
            Paragraph("• \"What is the main topic?\"", self.body_style),
            Paragraph("• \"Summarize the key points\"", self.body_style),
            Paragraph("• \"What happened in March 2021?\"", self.body_style),
            Paragraph("• \"Compare different technologies\"", self.body_style),
            
            Spacer(1, 8),
            Paragraph("🚀 Web Interface Features", self.heading_style),
            Paragraph("• Real-time chat with AI responses", self.body_style),
            Paragraph("• Document management sidebar", self.body_style),
            Paragraph("• Inline citations with sources", self.body_style),
            Paragraph("• Chat history and context", self.body_style),
        ]
        
        right_content = [
            Paragraph("⚙️ Key Technologies", self.heading_style),
            Paragraph("• Python 3.13.5 + Streamlit", self.body_style),
            Paragraph("• Google Gemini AI", self.body_style),
            Paragraph("• TF-IDF + Cosine Similarity", self.body_style),
            Paragraph("• Intelligent caching system", self.body_style),
            
            Spacer(1, 8),
            Paragraph("📖 Citation System", self.heading_style),
            Paragraph("Automatic inline citations:", self.body_style),
            Paragraph("<font name='Courier' color='#2E86AB'>\"VisionTag uses YOLOv8 [1]...\"</font>", self.body_style),
            Paragraph("<font name='Courier' color='#2E86AB'>References: [1] document.pdf</font>", self.body_style),
            
            Spacer(1, 8),
            Paragraph("🔧 CLI Commands", self.heading_style),
            Paragraph("• help - Show available commands", self.body_style),
            Paragraph("• list - List loaded documents", self.body_style),
            Paragraph("• refresh - Reload documents", self.body_style),
            Paragraph("• summarize - Generate summary", self.body_style),
            Paragraph("• clear - Clear chat history", self.body_style),
            
            Spacer(1, 8),
            Paragraph("🛠️ Troubleshooting", self.heading_style),
            Paragraph("• Check .env file for API key", self.body_style),
            Paragraph("• Verify documents in data/ folder", self.body_style),
            Paragraph("• Use refresh button after adding files", self.body_style),
            Paragraph("• Check file permissions and formats", self.body_style),
        ]
        
        # Create table for two-column layout
        content_table = Table([[left_content, right_content]], colWidths=[3.5*inch, 3.5*inch])
        content_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        self.story.append(content_table)
        
        # Footer
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=HexColor('#666666'),
            spaceBefore=15
        )
        
        footer = Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')} | "
                          f"AI-Powered Document Analysis with Inline Citations", footer_style)
        self.story.append(footer)
        
        # Build PDF
        self.doc.build(self.story)
        print(f"✅ Quick reference guide generated: {self.filename}")

if __name__ == "__main__":
    guide = QuickReferenceGuide()
    guide.generate_quick_reference()
    print(f"📄 Quick reference complete!")
