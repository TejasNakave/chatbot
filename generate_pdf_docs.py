#!/usr/bin/env python3
"""
PDF Documentation Generator for Document-Based Chatbot
Creates a professional PDF document with project overview, technical details, and usage guide.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, blue, green, red
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class ChatbotDocumentation:
    def __init__(self, filename="Chatbot_Project_Documentation.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        self.styles = getSampleStyleSheet()
        self.story = []
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Create custom styles for the document"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2E86AB'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Heading styles
        self.heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#A23B72'),
            fontName='Helvetica-Bold'
        )
        
        self.heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            textColor=HexColor('#F18F01'),
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        
        # Code style
        self.code_style = ParagraphStyle(
            'CustomCode',
            parent=self.styles['Code'],
            fontSize=10,
            fontName='Courier',
            textColor=HexColor('#333333'),
            backColor=HexColor('#F5F5F5'),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10
        )
        
        # Feature style
        self.feature_style = ParagraphStyle(
            'FeatureStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leftIndent=20,
            fontName='Helvetica'
        )

    def add_title_page(self):
        """Create an attractive title page"""
        # Main title
        title = Paragraph("🤖 Document-Based Chatbot", self.title_style)
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=self.styles['Normal'],
            fontSize=16,
            alignment=TA_CENTER,
            textColor=HexColor('#666666'),
            spaceAfter=30
        )
        subtitle = Paragraph("AI-Powered Document Analysis with Inline Citations", subtitle_style)
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Key features box
        features_data = [
            ['🎯 Key Features'],
            ['📄 Multi-format Document Support (PDF, DOCX, TXT)'],
            ['🔍 Smart Hybrid Search with TF-IDF + Exact Matching'],
            ['📖 Automatic Inline Citations with Numbered References'],
            ['🧠 AI-Powered Responses using Google Gemini'],
            ['🌐 Professional Web Interface with Streamlit'],
            ['💾 Intelligent Caching for Optimal Performance'],
            ['🔄 Real-time Document Management']
        ]
        
        features_table = Table(features_data, colWidths=[6*inch])
        features_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F8F9FA')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#DDDDDD')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        self.story.append(features_table)
        self.story.append(Spacer(1, 1*inch))
        
        # Project info
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=HexColor('#666666')
        )
        
        date_info = Paragraph(f"Documentation Generated: {datetime.now().strftime('%B %d, %Y')}", info_style)
        self.story.append(date_info)
        
        tech_info = Paragraph("Built with Python • Streamlit • Google Gemini API • Scikit-learn", info_style)
        self.story.append(tech_info)
        
        self.story.append(PageBreak())

    def add_overview_section(self):
        """Add project overview section"""
        self.story.append(Paragraph("Project Overview", self.heading1_style))
        
        overview_text = """
        The Document-Based Chatbot is a sophisticated AI-powered application that enables users to interact 
        with their documents through natural language queries. Built with cutting-edge technologies, it 
        combines advanced document retrieval algorithms with Google's Gemini AI to provide accurate, 
        context-aware responses with proper source attribution.
        
        This system transforms static documents into an interactive knowledge base, making information 
        discovery and analysis more efficient and intuitive. Whether you're analyzing business reports, 
        research papers, or technical documentation, this chatbot provides instant, intelligent answers 
        with complete source transparency.
        """
        
        self.story.append(Paragraph(overview_text, self.body_style))
        self.story.append(Spacer(1, 0.2*inch))

    def add_technical_architecture(self):
        """Add technical architecture section"""
        self.story.append(Paragraph("Technical Architecture", self.heading1_style))
        
        # Backend Technologies
        self.story.append(Paragraph("Backend Technologies", self.heading2_style))
        
        backend_data = [
            ['Component', 'Technology', 'Purpose'],
            ['Core Language', 'Python 3.13.5', 'Main programming language'],
            ['AI Engine', 'Google Gemini API', 'Natural language processing'],
            ['Search Algorithm', 'TF-IDF Vectorization', 'Document similarity analysis'],
            ['Similarity Calculation', 'Cosine Similarity', 'Mathematical relevance scoring'],
            ['Caching System', 'Custom Implementation', 'Performance optimization'],
            ['Document Processing', 'PyPDF2, python-docx', 'Multi-format file handling']
        ]
        
        backend_table = Table(backend_data, colWidths=[1.8*inch, 2*inch, 2.2*inch])
        backend_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#DDDDDD')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F8F9FA')])
        ]))
        
        self.story.append(backend_table)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Frontend Technologies
        self.story.append(Paragraph("Frontend Technologies", self.heading2_style))
        
        frontend_data = [
            ['Component', 'Technology', 'Features'],
            ['Web Framework', 'Streamlit', 'Interactive web interface'],
            ['Styling', 'Custom CSS', 'Professional design'],
            ['Layout', 'Multi-column Design', 'Optimized user experience'],
            ['Components', 'Streamlit Widgets', 'Real-time interaction']
        ]
        
        frontend_table = Table(frontend_data, colWidths=[1.8*inch, 2*inch, 2.2*inch])
        frontend_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#A23B72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#DDDDDD')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F8F9FA')])
        ]))
        
        self.story.append(frontend_table)
        self.story.append(Spacer(1, 0.2*inch))

    def add_features_section(self):
        """Add detailed features section"""
        self.story.append(Paragraph("Advanced Features", self.heading1_style))
        
        # Inline Citations
        self.story.append(Paragraph("📖 Inline Citations System", self.heading2_style))
        citations_text = """
        The chatbot automatically includes numbered citations within responses, following academic standards. 
        Each fact, figure, or claim is properly attributed to its source document, enabling users to verify 
        information and track the origin of insights. This feature ensures transparency and builds trust 
        in the AI-generated responses.
        """
        self.story.append(Paragraph(citations_text, self.body_style))
        
        # Example citation format
        example_style = ParagraphStyle(
            'ExampleStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Courier',
            textColor=HexColor('#2E86AB'),
            backColor=HexColor('#F0F8FF'),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            spaceBefore=10
        )
        
        citation_example = """
        Example Response:
        "VisionTag is a computer vision solution for manufacturing quality inspection [1]. 
        It utilizes YOLOv8 and MobileNet models [1] with 97.3% accuracy in defect detection [1].
        
        References:
        [1] web_development.txt"
        """
        self.story.append(Paragraph(citation_example, example_style))
        
        # Smart Retrieval
        self.story.append(Paragraph("🔍 Smart Retrieval System", self.heading2_style))
        retrieval_text = """
        The hybrid search system combines multiple strategies for optimal document retrieval:
        • TF-IDF vectorization for semantic similarity
        • Exact keyword matching for precise terms
        • Question-to-keyword extraction for natural language queries
        • Multi-level fallback strategies for improved recall
        • Intelligent scoring system prioritizing relevance
        """
        self.story.append(Paragraph(retrieval_text, self.body_style))
        
        # Performance Optimization
        self.story.append(Paragraph("⚡ Performance Optimization", self.heading2_style))
        performance_text = """
        The system implements several optimization techniques:
        • Intelligent caching of TF-IDF vectors for faster reloads
        • Hash-based cache validation for automatic updates
        • Memory-efficient document processing
        • Background processing for improved responsiveness
        • Session state management for seamless user experience
        """
        self.story.append(Paragraph(performance_text, self.body_style))

    def add_installation_guide(self):
        """Add installation and setup guide"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Installation & Setup Guide", self.heading1_style))
        
        # Prerequisites
        self.story.append(Paragraph("Prerequisites", self.heading2_style))
        prereq_text = """
        • Python 3.7 or higher
        • Google Gemini API key
        • Internet connection for AI processing
        • Supported document formats: PDF, DOCX, TXT
        """
        self.story.append(Paragraph(prereq_text, self.body_style))
        
        # Step-by-step installation
        self.story.append(Paragraph("Installation Steps", self.heading2_style))
        
        install_steps = [
            "1. Clone or download the project files",
            "2. Install required packages: pip install -r requirements.txt",
            "3. Create .env file with your GEMINI_API_KEY",
            "4. Add documents to the data/ folder",
            "5. Run the application: streamlit run streamlit_app.py"
        ]
        
        for step in install_steps:
            self.story.append(Paragraph(step, self.feature_style))
        
        # Configuration
        self.story.append(Paragraph("Configuration Options", self.heading2_style))
        config_text = """
        The system offers several configuration options to optimize performance:
        • Max Documents: Number of relevant documents to retrieve (default: 3)
        • Similarity Threshold: Minimum relevance score (default: 0.05)
        • Context Length: Maximum context size for AI processing
        • Cache Settings: Enable/disable intelligent caching
        """
        self.story.append(Paragraph(config_text, self.body_style))

    def add_usage_examples(self):
        """Add usage examples and best practices"""
        self.story.append(Paragraph("Usage Examples", self.heading1_style))
        
        # Web Interface Usage
        self.story.append(Paragraph("Web Interface", self.heading2_style))
        web_usage = """
        The Streamlit web interface provides an intuitive way to interact with your documents:
        • Upload documents using the sidebar document management panel
        • Ask natural language questions in the chat interface
        • View source attribution and relevance scores
        • Generate comprehensive document summaries
        • Manage chat history and document collections
        """
        self.story.append(Paragraph(web_usage, self.body_style))
        
        # Example queries
        self.story.append(Paragraph("Example Queries", self.heading2_style))
        
        query_examples = [
            '"What is VisionTag?" - Technical product information',
            '"What happened in March 2021?" - Temporal queries',
            '"Compare the different technologies mentioned" - Comparative analysis',
            '"Summarize the key features" - Content summarization',
            '"What are the system requirements?" - Specific information retrieval'
        ]
        
        for example in query_examples:
            self.story.append(Paragraph(f"• {example}", self.feature_style))
        
        # Best practices
        self.story.append(Paragraph("Best Practices", self.heading2_style))
        best_practices = """
        To get the best results from your chatbot:
        • Use clear, specific questions for better retrieval accuracy
        • Organize documents with descriptive filenames
        • Keep document formats consistent (prefer searchable PDFs)
        • Regularly refresh the document index when adding new files
        • Use the citation numbers to verify information sources
        • Experiment with different question phrasings for comprehensive answers
        """
        self.story.append(Paragraph(best_practices, self.body_style))

    def add_technical_details(self):
        """Add detailed technical information"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Technical Implementation Details", self.heading1_style))
        
        # System Architecture
        self.story.append(Paragraph("System Architecture", self.heading2_style))
        
        architecture_data = [
            ['Layer', 'Components', 'Responsibilities'],
            ['Presentation', 'Streamlit UI, Custom CSS', 'User interface and interaction'],
            ['Application', 'Chat Logic, Session Management', 'Business logic and state management'],
            ['Processing', 'Retriever, Gemini Wrapper', 'Document search and AI processing'],
            ['Data', 'Document Loader, Cache System', 'File handling and performance optimization']
        ]
        
        arch_table = Table(architecture_data, colWidths=[1.5*inch, 2.2*inch, 2.3*inch])
        arch_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F18F01')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#DDDDDD')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F8F9FA')])
        ]))
        
        self.story.append(arch_table)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Data Flow
        self.story.append(Paragraph("Data Flow Process", self.heading2_style))
        flow_text = """
        1. Document Loading: Multi-format files are processed and text is extracted
        2. Text Processing: Content is chunked and preprocessed for optimal retrieval
        3. Indexing: TF-IDF vectors are generated and cached for efficient search
        4. Query Processing: User questions are analyzed and key terms extracted
        5. Retrieval: Relevant documents are identified using hybrid search algorithms
        6. AI Processing: Context and query are sent to Google Gemini for response generation
        7. Citation Integration: Responses are enhanced with inline citations and references
        8. Presentation: Final responses are formatted and displayed in the web interface
        """
        self.story.append(Paragraph(flow_text, self.body_style))

    def add_conclusion(self):
        """Add conclusion and future enhancements"""
        self.story.append(Paragraph("Conclusion & Future Enhancements", self.heading1_style))
        
        conclusion_text = """
        The Document-Based Chatbot represents a significant advancement in document analysis and 
        information retrieval. By combining state-of-the-art AI technology with robust document 
        processing capabilities, it provides users with an intelligent, reliable, and transparent 
        way to interact with their document collections.
        
        The implementation of inline citations ensures academic-level source attribution, while 
        the hybrid search system guarantees comprehensive information retrieval. The professional 
        web interface makes the system accessible to users of all technical backgrounds.
        """
        self.story.append(Paragraph(conclusion_text, self.body_style))
        
        # Future enhancements
        self.story.append(Paragraph("Potential Future Enhancements", self.heading2_style))
        
        enhancements = [
            "🔍 Support for additional file formats (PowerPoint, Excel, etc.)",
            "🌐 Multi-language document support and translation capabilities",
            "📊 Advanced analytics and document insight dashboards",
            "🔒 Enhanced security features for sensitive document handling",
            "📱 Mobile-responsive design and progressive web app capabilities",
            "🤖 Integration with additional AI models for specialized analysis",
            "🔗 API endpoints for third-party integrations",
            "📈 Advanced visualization of document relationships and topics"
        ]
        
        for enhancement in enhancements:
            self.story.append(Paragraph(enhancement, self.feature_style))
        
        # Contact and support
        self.story.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=HexColor('#666666')
        )
        
        footer_text = """
        For technical support, feature requests, or contributions, please refer to the 
        project repository and documentation. This system is designed to be extensible 
        and welcomes community contributions for continued improvement.
        """
        self.story.append(Paragraph(footer_text, footer_style))

    def generate_pdf(self):
        """Generate the complete PDF document"""
        print("🔄 Generating PDF documentation...")
        
        # Add all sections
        self.add_title_page()
        self.add_overview_section()
        self.add_technical_architecture()
        self.add_features_section()
        self.add_installation_guide()
        self.add_usage_examples()
        self.add_technical_details()
        self.add_conclusion()
        
        # Build the PDF
        self.doc.build(self.story)
        print(f"✅ PDF documentation generated successfully: {self.filename}")
        return self.filename

if __name__ == "__main__":
    # Generate the documentation
    doc_generator = ChatbotDocumentation()
    pdf_filename = doc_generator.generate_pdf()
    
    print(f"\n🎉 Documentation complete!")
    print(f"📄 File: {pdf_filename}")
    print(f"📍 Location: {os.path.abspath(pdf_filename)}")
